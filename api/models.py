from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from database import Base

user_roles = Table('user_roles', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    roles = relationship('Role', secondary=user_roles, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship('User', secondary=user_roles, back_populates='roles')

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    is_enabled = Column(Boolean, default=True)

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('users.id'))
    record = Column(Text)

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('users.id'))
    professional_id = Column(Integer, ForeignKey('users.id'))
    scheduled_time = Column(DateTime)
    description = Column(String(255))

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('users.id'))
    condition = Column(String(255))
    threshold = Column(Float)
    message = Column(String(255))

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
    timestamp = Column(DateTime)

