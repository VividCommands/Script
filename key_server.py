from flask import Flask, request, jsonify
import json
import os
import time

app = Flask(__name__)
LICENSE_FILE = 'licenses.json'
LICENSE_DURATION = 7 * 24 * 60 * 60  # 7 days

# Create file if it doesn't exist
if not os.path.exists(LICENSE_FILE):
    with open(LICENSE_FILE, 'w') as f:
        json.dump({}, f)

def load_licenses():
    with open(LICENSE_FILE, 'r') as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json() or {}
    license_key = data.get('license_key', '').strip()
    licenses = load_licenses()
    license_data = licenses.get(license_key)

    if license_data:
        created_at = license_data.get('created_at', 0)
        if time.time() - created_at <= LICENSE_DURATION:
            return jsonify({'valid': True}), 200
        else:
            return jsonify({'valid': False, 'message': 'License expired.'}), 403
    return jsonify({'valid': False, 'message': 'Invalid key.'}), 403

@app.route('/add_key', methods=['POST'])
def add_key():
    data = request.get_json() or {}
    new_key = data.get('new_key', '').strip()
    if not new_key:
        return jsonify({'error': 'Missing key.'}), 400
    licenses = load_licenses()
    licenses[new_key] = {'created_at': time.time()}
    save_licenses(licenses)
    return jsonify({'success': True, 'message': f'Key {new_key} added.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
