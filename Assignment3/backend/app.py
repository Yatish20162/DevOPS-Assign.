from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Flask Backend',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/process', methods=['POST'])
def process_form():
    try:
        # Get JSON data from request
        data = request.get_json()

        print(data)
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'age', 'city', 'hobby']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Process the data (you can add your custom logic here)
        processed_data = {
            'name': data['name'].strip().title(),
            'email': data['email'].strip().lower(),
            'age': int(data['age']),
            'city': data['city'].strip().title(),
            'hobby': data['hobby'].strip().lower()
        }
        
        # Validate age
        if processed_data['age'] < 1 or processed_data['age'] > 120:
            return jsonify({
                'error': 'Age must be between 1 and 120'
            }), 400
        
        # Create response
        response = {
            'message': f'Hello {processed_data["name"]}! Your form has been processed successfully.',
            'data': processed_data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success'
        }
        
        # Log the processed data (in production, use proper logging)
        print(f"Processed form data: {processed_data}")
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid data format',
            'details': str(e)
        }), 400
        
    except Exception as e:
        print(e)
        print(f"Error processing form: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])