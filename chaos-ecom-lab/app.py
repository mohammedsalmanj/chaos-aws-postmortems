from flask import Flask, request, jsonify
import sqlite3, os, time, redis, json
from datetime import datetime

DB_PATH = '/data/orders.db'
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'payment_queue')

app = Flask(__name__)

# --- Redis connection ---
r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

# --- DB setup ---
def init_db():
    os.makedirs('/data', exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, amount REAL, status TEXT, created TEXT)')
    con.commit()
    con.close()
    print("✅ Database ready.")

@app.before_request
def ensure_db():
    if not hasattr(app, "db_initialized"):
        init_db()
        app.db_initialized = True

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'time': datetime.utcnow().isoformat()}), 200

# --- Publish order to queue ---
@app.route('/purchase', methods=['POST'])
def purchase():
    data = request.json or {}
    item = data.get('item', 'unknown')
    amount = float(data.get('amount', 0.0))
    created = datetime.utcnow().isoformat()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('INSERT INTO orders (item, amount, status, created) VALUES (?, ?, ?, ?)', (item, amount, 'queued', created))
    con.commit()
    order_id = cur.lastrowid
    con.close()

    msg = {'order_id': order_id, 'item': item, 'amount': amount, 'created': created}
    r.lpush(QUEUE_NAME, json.dumps(msg))
    print(f"📨 Queued order {order_id} for payment processing.")

    return jsonify({'order_id': order_id, 'status': 'queued'}), 200

@app.route('/orders', methods=['GET'])
def list_orders():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id, item, amount, status, created FROM orders ORDER BY id DESC LIMIT 50')
    rows = cur.fetchall()
    con.close()
    return jsonify({'orders': [{'id': r[0], 'item': r[1], 'amount': r[2], 'status': r[3], 'created': r[4]} for r in rows]})

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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
