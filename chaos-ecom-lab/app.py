from flask import Flask, request, jsonify
import sqlite3
import os
import requests
import time
from datetime import datetime

DB_PATH = '/data/orders.db'
PAYMENT_URL = os.environ.get('PAYMENT_URL', 'http://payment-mock:5001/pay')
app = Flask(__name__)

# --- Initialize DB once ---
def init_db():
    os.makedirs('/data', exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, amount REAL, status TEXT, created TEXT)')
    con.commit()
    con.close()
    print("✅ Database initialized.")

# Instead of before_first_request (removed in Flask 3.x)
@app.before_request
def ensure_db():
    if not hasattr(app, "db_initialized"):
        init_db()
        app.db_initialized = True

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'time': datetime.utcnow().isoformat()}), 200

# --- Retry-enabled purchase endpoint ---
@app.route('/purchase', methods=['POST'])
def purchase():
    data = request.json or {}
    item = data.get('item', 'unknown')
    amount = float(data.get('amount', 0.0))
    status = 'payment_error'

    max_retries = int(os.environ.get('RETRY_COUNT', 3))
    base_delay = int(os.environ.get('RETRY_DELAY', 1))

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[RETRY {attempt}] Calling payment service for item={item}, amount={amount}")
            resp = requests.post(PAYMENT_URL, json={'amount': amount, 'item': item}, timeout=3)
            resp.raise_for_status()
            payment_result = resp.json()

            if payment_result.get('status') == 'success':
                status = 'completed'
                print(f"✅ Payment succeeded on attempt {attempt}")
                break
            else:
                print(f"⚠️ Payment declined (attempt {attempt}): {payment_result}")
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
        time.sleep(base_delay * (2 ** (attempt - 1)))  # exponential backoff (1s, 2s, 4s...)

    # --- Record result in DB ---
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('INSERT INTO orders (item, amount, status, created) VALUES (?, ?, ?, ?)',
                (item, amount, status, datetime.utcnow().isoformat()))
    con.commit()
    order_id = cur.lastrowid
    con.close()

    print(f"📦 Order {order_id} recorded with status={status}")
    return jsonify({'order_id': order_id, 'status': status}), 200 if status == 'completed' else 502

@app.route('/return', methods=['POST'])
def do_return():
    data = request.json or {}
    order_id = int(data.get('order_id', 0))
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id, status FROM orders WHERE id=?', (order_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({'error': 'order_not_found'}), 404
    cur.execute('UPDATE orders SET status=? WHERE id=?', ('returned', order_id))
    con.commit()
    con.close()
    return jsonify({'order_id': order_id, 'status': 'returned'}), 200

@app.route('/orders', methods=['GET'])
def list_orders():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id, item, amount, status, created FROM orders ORDER BY id DESC LIMIT 50')
    rows = cur.fetchall()
    con.close()
    orders = [{'id': r[0], 'item': r[1], 'amount': r[2], 'status': r[3], 'created': r[4]} for r in rows]
    return jsonify({'orders': orders})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
