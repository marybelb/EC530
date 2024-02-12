# EC530
## Health Monitoring System
### Platform to monitor patients at home or in the hospitals
  * Users:
    * Patients
    * Medical Professionals (Nurses and Doctors)
    * Administrators
    * Developers:
      * Application developers 
      * Device integrators
      * Machine Learning Scientists
### Administrator User Stories
  * Add users to the system:
    * Users should be added to the system and cannot register before being added to the system
  * Assign and Change Roles to users
    * Patient
    * Nurse
    * Doctor
    * Admin
    * Family member
  * A user can have different roles, e.g., 
    * A user can be a patient and/or a doctor
    * A user can be a family member and/or a patient
  * Provide interfaces to third-party medical device makers (Thermometer, Pulse, Blood pressure, Glucometer, etc.) to have their devices feed data to the system
  * Ability to disable or enable any device maker or application developer
### Medical Professional (MP) User Stories
  * Browse Patients
  * Assign a medical device to a Patient
  * Assign Alert and scheduling for medical measurement, e.g., 
    * Patient to measure blood pressure daily.  MP will receive an alert if it not done. 
    * Temperature is higher or lower than a value.  MP will get an alert if the measurement is outside acceptable range
  * MP can input data for any patient
  * MP can chat with patients using text, voice or videos.
  * MP can read transcripts of Patient uploaded videos and messages
  * MP can search for keywords in messages and chats
  * MP have a calendar where they can show open time slots for appointments
  * MP can see all appointments booked at any time
### Patient Use Cases 
  * Patient can enter measurement at any time
  * Patient can write a text or upload video or voice message to the MP
  * Patient can book an appointment with the MP
  * Patient can view their medical measurements

<img width="751" alt="Screenshot 2024-02-12 at 2 59 32 PM" src="https://github.com/marybelb/EC530/assets/91172956/52c6966d-5a49-4835-9ca8-ca8791907697">

