from flask import Flask, render_template, request, jsonify
import stripe

app = Flask(__name__)

stripe.api_key = "sk_test_51N0g1kL8J3z5Q6"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        total_price = int(data.get('price', 29))
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'SaaSify Subscription (Dynamic)',
                    },
                    'unit_amount': total_price * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5001/?success=true',
            cancel_url='http://localhost:5001/?canceled=true',
        )
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)