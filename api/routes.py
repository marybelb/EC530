from flask import Flask, jsonify, request
from models import User, Appointment, MedicalRecord, Alert
from database import session
import datetime

app = Flask(__name__)

# Route to add or update a medical record for a patient
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

# Route to schedule an appointment
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

# Route to set up an alert for a patient
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

# Route to list appointments for a medical professional
@app.route('/professional/<int:professional_id>/appointments', methods=['GET'])
def list_appointments(professional_id):
    appointments = session.query(Appointment).filter_by(professional_id=professional_id).all()
    return jsonify([
        {"patient_id": appointment.patient_id, "scheduled_time": appointment.scheduled_time.isoformat(), "description": appointment.description}
        for appointment in appointments
    ]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
