from flask import Flask, jsonify, request
from models import Device, DeviceData
from database import session
import datetime

app = Flask(__name__)

# Route to register a new device
@app.route('/devices/register', methods=['POST'])
def register_device():
    data = request.json
    new_device = Device(type=data['type'], is_enabled=True)
    session.add(new_device)
    session.commit()
    return jsonify({"message": "Device registered successfully", "device_id": new_device.id}), 201

# Route for devices to send data
@app.route('/devices/<int:device_id>/data', methods=['POST'])
def receive_device_data(device_id):
    device = session.query(Device).get(device_id)
    if not device or not device.is_enabled:
        return jsonify({"message": "Device not found or not enabled"}), 404
    
    data = request.json
    device_data = DeviceData(device_id=device_id, data=data['data'], timestamp=datetime.datetime.now())
    session.add(device_data)
    session.commit()
    return jsonify({"message": "Data received successfully"}), 200

# Administrator route to enable or disable a device integration
@app.route('/admin/devices/<int:device_id>/toggle', methods=['POST'])
def admin_toggle_device(device_id):
    device = session.query(Device).get(device_id)
    if not device:
        return jsonify({"message": "Device not found"}), 404

    device.is_enabled = not device.is_enabled
    session.commit()
    return jsonify({"message": "Device integration toggled successfully", "status": device.is_enabled}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
