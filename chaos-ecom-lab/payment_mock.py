from flask import Flask, request, jsonify
import os
import random
app = Flask(__name__)

# By default this mock returns success. Toggle FAIL_MODE env var to '1' to simulate gateway outage/failures.
@app.route('/pay', methods=['POST'])
def pay():
    if os.environ.get('FAIL_MODE','0') == '1':
        # Simulate timeout or error
        return jsonify({'status': 'error', 'reason': 'payment_gateway_unavailable'}), 502
    data = request.json or {}
    amount = data.get('amount', 0)
    # simulate occasional random failure
    if random.random() < 0.05:
        return jsonify({'status':'error','reason':'random_decline'}), 402
    return jsonify({'status':'success','amount': amount}), 200

@app.route('/health')
def health():
    return jsonify({'service':'payment-mock', 'ok': os.environ.get('FAIL_MODE','0')=='0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
