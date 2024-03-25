from flask import Flask, jsonify, request
from models import User, Role, Device
from database import session

app = Flask(__name__)

# Route to register a new user
@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    user = User(username=data['username'])
    session.add(user)
    session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# Route to assign roles to users
@app.route('/users/<int:user_id>/roles', methods=['POST'])
def assign_role(user_id):
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    for role_name in data['roles']:
        role = session.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
        user.roles.append(role)
    session.commit()
    return jsonify({"message": "Roles assigned successfully"}), 200

# Route to list all devices
@app.route('/devices', methods=['GET'])
def list_devices():
    devices = session.query(Device).all()
    return jsonify([{"id": device.id, "type": device.type, "is_enabled": device.is_enabled} for device in devices]), 200

# Route to enable or disable a device
@app.route('/devices/<int:device_id>/toggle', methods=['POST'])
def toggle_device(device_id):
    device = session.query(Device).get(device_id)
    if not device:
        return jsonify({"message": "Device not found"}), 404

    device.is_enabled = not device.is_enabled
    session.commit()
    return jsonify({"message": "Device toggled successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
