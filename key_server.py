from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LICENSE_FILE = 'licenses.json'

# Ensure the license file exists
if not os.path.exists(LICENSE_FILE):
    with open(LICENSE_FILE, 'w') as f:
        json.dump({"ABC-123-DEF": True}, f)

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json() or {}
    license_key = data.get('license_key', '').strip()
    
    with open(LICENSE_FILE, 'r') as f:
        licenses = json.load(f)
    
    if licenses.get(license_key):
        return jsonify({'valid': True}), 200
    return jsonify({'valid': False, 'message': 'Invalid or expired key.'}), 403

@app.route('/add_key', methods=['POST'])
def add_key():
    data = request.get_json() or {}
    admin_secret = data.get('admin_secret')
    new_key = data.get('new_key')

    # Replace with your own admin secret for security
    if admin_secret != 'YOUR_ADMIN_SECRET':
        return jsonify({'error': 'Unauthorized'}), 401

    with open(LICENSE_FILE, 'r+') as f:
        data = json.load(f)
        data[new_key] = True
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    return jsonify({'success': True, 'message': f'Key {new_key} added.'}), 200

if __name__ == '__main__':
    # Run with: gunicorn key_server:app
    app.run(host='0.0.0.0', port=5000)  # fallback for local testing


