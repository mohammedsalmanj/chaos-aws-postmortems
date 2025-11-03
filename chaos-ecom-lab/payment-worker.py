import os, json, time, redis, requests, sqlite3
from datetime import datetime

DB_PATH = '/data/orders.db'
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
QUEUE_NAME = os.environ.get('QUEUE_NAME', 'payment_queue')
PAYMENT_URL = os.environ.get('PAYMENT_URL', 'http://payment-mock:5001/pay')

r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

def init_db():
    os.makedirs('/data', exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, amount REAL, status TEXT, created TEXT)')
    con.commit()
    con.close()

def process_message(msg):
    try:
        data = json.loads(msg)
        order_id, item, amount = data['order_id'], data['item'], data['amount']
        print(f"🔁 Processing order {order_id}...")

        # Try payment (simulate DNS failure safe)
        try:
            resp = requests.post(PAYMENT_URL, json={'amount': amount, 'item': item}, timeout=3)
            resp.raise_for_status()
            result = resp.json()
            if result.get('status') == 'success':
                update_order(order_id, 'completed')
                print(f"✅ Order {order_id} completed successfully.")
            else:
                update_order(order_id, 'failed')
        except Exception as e:
            print(f"⚠️ Payment error for order {order_id}: {e}")
            # Requeue for retry later
            r.rpush(QUEUE_NAME, msg)
            time.sleep(2)

    except Exception as e:
        print(f"❌ Message processing failed: {e}")

def update_order(order_id, status):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('UPDATE orders SET status=? WHERE id=?', (status, order_id))
    con.commit()
    con.close()

if __name__ == "__main__":
    init_db()
    print("🚀 Payment worker started, waiting for messages...")
    while True:
        msg = r.brpop(QUEUE_NAME, timeout=5)
        if msg:
            _, data = msg
            process_message(data.decode())
        else:
            time.sleep(1)
