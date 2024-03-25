from flask import Flask, jsonify, request
from models import User, Role, Device, DeviceData, MedicalRecord, Appointment, Alert, Message
from database import session
import datetime

app = Flask(__name__)

# User Management
@app.route('/users/register', methods=['POST'])
def register_user():
    data = request.json
    user = User(username=data['username'])
    session.add(user)
    session.commit()
    return jsonify({"message": "User registered successfully"}), 201

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

# Device Integration
@app.route('/devices/register', methods=['POST'])
def register_device():
    data = request.json
    new_device = Device(type=data['type'], is_enabled=True)
    session.add(new_device)
    session.commit()
    return jsonify({"message": "Device registered successfully", "device_id": new_device.id}), 201

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

@app.route('/admin/devices/<int:device_id>/toggle', methods=['POST'])
def admin_toggle_device(device_id):
    device = session.query(Device).get(device_id)
    if not device:
        return jsonify({"message": "Device not found"}), 404

    device.is_enabled = not device.is_enabled
    session.commit()
    return jsonify({"message": "Device integration toggled successfully", "status": device.is_enabled}), 200

# Patient Care Management
@app.route('/patients/<int:patient_id>/medical_record', methods=['POST'])
def update_medical_record(patient_id):
    data = request.json
    record = session.query(MedicalRecord).filter_by(patient_id=patient_id).first()
    if record is None:
        record = MedicalRecord(patient_id=patient_id, record=data['record'])
        session.add(record)
    else:
        record.record = data['record']
    session.commit()
    return jsonify({"message": "Medical record updated successfully"}), 200

@app.route('/appointments/schedule', methods=['POST'])
def schedule_appointment():
    data = request.json
    new_appointment = Appointment(
        patient_id=data['patient_id'],
        professional_id=data['professional_id'],
        scheduled_time=datetime.datetime.fromisoformat(data['scheduled_time']),
        description=data['description']
    )
    session.add(new_appointment)
    session.commit()
    return jsonify({"message": "Appointment scheduled successfully"}), 201

@app.route('/alerts/setup', methods=['POST'])
def setup_alert():
    data = request.json
    new_alert = Alert(
        patient_id=data['patient_id'],
        condition=data['condition'],
        threshold=data['threshold'],
        message=data['message']
    )
    session.add(new_alert)
    session.commit()
    return jsonify({"message": "Alert set up successfully"}), 200

@app.route('/professional/<int:professional_id>/appointments', methods=['GET'])
def list_appointments(professional_id):
    appointments = session.query(Appointment).filter_by(professional_id=professional_id).all()
    return jsonify([
        {"patient_id": appointment.patient_id, "scheduled_time": appointment.scheduled_time.isoformat(), "description": appointment.description}
        for appointment in appointments
    ]), 200

# Communication Module
@app.route('/messages/send', methods=['POST'])
def send_message():
    data = request.json
    new_message = Message(
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        content=data['content'],
        timestamp=datetime.datetime.now()
    )
    session.add(new_message)
    session.commit()
    return jsonify({"message": "Message sent successfully"}), 200

@app.route('/messages/<int:user1_id>/<int:user2_id>', methods=['GET'])
def list_messages(user1_id, user2_id):
    messages = session.query(Message).filter(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) | 
        ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    ).order_by(Message.timestamp.asc()).all()
    return jsonify([
        {"sender_id": message.sender_id, "receiver_id": message.receiver_id, "content": message.content, "timestamp": message.timestamp.isoformat()}
        for message in messages
    ]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
