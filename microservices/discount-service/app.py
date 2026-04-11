from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

promocodes = {
    'CHAK10': 10,
    'CHAK20': 20,
    'TASTY50': 50,
    'WELCOME': 15,
    'NEWYEAR': 25
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'discount-service'}), 200

@app.route('/discount', methods=['POST'])
def calculate_discount():
    data = request.get_json()
    promocode = data.get('promocode', '').upper()
    order_amount = data.get('amount', 0)
    
    if promocode in promocodes:
        discount_percent = promocodes[promocode]
        discount_amount = order_amount * discount_percent / 100
        final_amount = order_amount - discount_amount
        
        return jsonify({
            'status': 'success',
            'promocode': promocode,
            'discount_percent': discount_percent,
            'discount_amount': round(discount_amount, 2),
            'original_amount': order_amount,
            'final_amount': round(final_amount, 2)
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': f'Промокод "{promocode}" не найден'
        }), 404

@app.route('/promocodes', methods=['GET'])
def get_promocodes():
    return jsonify({
        'promocodes': [
            {'code': code, 'discount_percent': percent}
            for code, percent in promocodes.items()
        ]
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)