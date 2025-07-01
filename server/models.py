
from flask_sqlalchemy import SQLAlchemy
"""
models.py

This file defines the database models for the Classroom Booking System. It uses SQLAlchemy to map Python classes to database tables. 
Each class represents a table in the database, and the attributes of the class represent the columns of the table. 
This file is essential for managing the database structure and relationships between different entities in the system.

Classes:
    User:
        Represents a user in the system. Users can have different roles such as 'cr' (Class Representative), 'user', or 'admin'.
        Attributes include user details like name, email, password, role, and approval status.
    
    CR:
        Represents a Class Representative (CR). Each CR is associated with a user and has additional details like branch and section.
        CRs can report issues, which are linked to this class.

    Issue:
        Represents an issue reported by a CR. Each issue is associated with a CR and contains details like subject, description, and timestamp.
        Issues can have a single admin reply.

    AdminReply:
        Represents a reply from an admin to a reported issue. Each reply is linked to an issue and contains the reply message, timestamp, and a seen status.
"""

# Initialize the SQLAlchemy object to be used for database operations.
# This object acts as the interface between the Flask application and the database.
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # cr, user, admin
    is_approved = db.Column(db.Boolean, default=False)
    cr = db.relationship('CR', backref='user', uselist=False)

class CR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    branch = db.Column(db.String(100))
    section = db.Column(db.String(100))
    issues = db.relationship('Issue', backref='cr')

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cr_id = db.Column(db.Integer, db.ForeignKey('cr.id'))
    subject = db.Column(db.String(255))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    reply = db.relationship('AdminReply', backref='issue', uselist=False)

class AdminReply(db.Model):
    __tablename__ = 'admin_reply'
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    seen = db.Column(db.Boolean, default=False)  # NEW FIELD


    def __repr__(self):
        return f'<Issue {self.issue_title}>'



