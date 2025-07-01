from flask import Flask, request, jsonify
"""
This script implements a Classroom Booking System using Flask. It provides APIs for user management, 
classroom booking, issue reporting, and admin functionalities. Below is a breakdown of the code:
1. **Imports and Configurations**:
    - Imports necessary libraries for Flask, SQLAlchemy, CORS, email handling, and date/time operations.
    - Configures the Flask app, SQLAlchemy database, and email settings.
2. **Database Models**:
    - `User`: Represents a user in the system with attributes like name, email, password, year, section, phone, and approval status.
    - `CR`: Represents a Class Representative (CR) with attributes like name, email, password, year, section, phone, batch, and related issues.
    - `Issue`: Represents an issue reported by a CR with attributes like subject, description, timestamp, resolution status, and admin reply.
    - `AdminReply`: Represents a reply from the admin to a reported issue.
    - `ClassroomBooking`: Represents a classroom booking with attributes like classroom name, timing, subject, faculty, CR name, and day.
3. **Routes**:
    - `/`: A simple route to check if the server is running.
    - `/signup`: Handles user signup requests and validates input fields.
    - `/login`: Handles user and admin login with role-based responses.
    - `/get-signup-requests`: Fetches unapproved user signup requests for admin approval.
    - `/approve-cr`: Approves a user as a CR and moves them to the CR list.
    - `/reject-cr`: Rejects a user signup request and removes them from the database.
    - `/approved-crs`: Fetches a list of all approved CRs.
    - `/remove-cr`: Removes a CR from the system.
    - `/report-issue`: Allows CRs to report issues with details like title, description, and timestamp.
    - `/issues`: Fetches all reported issues with details like subject, description, timestamp, and admin reply.
    - `/reply-to-issue`: Allows the admin to reply to a reported issue and marks it as resolved.
    - `/book-classroom/<day>`: Allows CRs to book a classroom for a specific day and time.
    - `/get-bookings<classroom_name>`: Fetches all bookings for a specific classroom.
4. **Error Handling**:
    - Includes error handling for database operations and invalid inputs.
5. **Database Initialization**:
    - Creates all database tables when the app starts.
6. **Email Notifications**:
    - Sends email notifications to CRs when the admin replies to their reported issues.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime
import re
# Flask is a micro web framework for building web applications
# request is used to handle HTTP requests, jsonify is used to return JSON responses
# SQLAlchemy is an ORM (Object Relational Mapper) for database operations
# CORS is used to handle Cross-Origin Resource Sharing
# Mail and Message are used for sending emails
# datetime is used for handling date and time operations
# re is used for regular expression operations
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'boydevil77740@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'aaaa'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'boydevil77740@gmail.com'  # Replace with your email
mail = Mail(app)

# Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    year = db.Column(db.String(10))
    section = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    approved = db.Column(db.Boolean, default=False)
    # The User class represents a user in the system.
    # Each attribute corresponds to a column in the 'user' table in the database.
    # id: Primary key, unique identifier for each user.
    # name: Name of the user.
    # email: Email address of the user, must be unique.
    # password: Password for the user's account.
    # year: Academic year of the user.
    # section: Section of the user.
    # phone: Phone number of the user.
    # approved: Boolean indicating whether the user is approved by the admin.
class CR(db.Model):
    __tablename__ = 'cr'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    year = db.Column(db.String(10))
    section = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    batch = db.Column(db.String(10))
    issues = db.relationship('Issue', backref='cr', lazy=True)
    # The CR class represents a Class Representative in the system.
    # Each attribute corresponds to a column in the 'cr' table in the database.
    # id: Primary key, unique identifier for each CR.
    # name: Name of the CR.
    # email: Email address of the CR, must be unique.
    # password: Password for the CR's account.
    # year: Academic year of the CR.
    # section: Section of the CR.
    # phone: Phone number of the CR.
    # batch: Batch of the CR.
    # issues: Relationship to the Issue model, representing issues reported by the CR.
class Issue(db.Model):
    """
    Represents an issue reported in the Classroom Booking System.
    Attributes:
        id (int): The primary key for the issue.
        cr_id (int): A foreign key referencing the 'cr' table's id, 
                     indicating the classroom related to the issue.
        subject (str): The subject or title of the issue, with a maximum length of 200 characters.
        description (str): A detailed description of the issue.
        timestamp (datetime): The date and time when the issue was created. 
                              Defaults to the current timestamp using `db.func.current_timestamp()`.
                              - `db.func.current_timestamp()`: Automatically sets the timestamp to the 
                                current date and time when the record is created.
        resolved (bool): A flag indicating whether the issue has been resolved. Defaults to False.
        reply (AdminReply): A one-to-one relationship with the AdminReply model, representing the 
                            admin's reply to the issue.
    """
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True)
    cr_id = db.Column(db.Integer, db.ForeignKey('cr.id'))
    subject = db.Column(db.String(200))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    resolved = db.Column(db.Boolean, default=False)
    reply = db.relationship('AdminReply', backref='issue', uselist=False)

class AdminReply(db.Model):
    __tablename__ = 'admin_reply'
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class ClassroomBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_name = db.Column(db.String(100), nullable=False)  # Name of the classroom
    timing = db.Column(db.String(50), nullable=False)  # Timing of the booking
    subject = db.Column(db.String(255), nullable=False)  # Subject for the booking
    faculty = db.Column(db.String(100), nullable=False)  # Faculty name
    cr_name = db.Column(db.String(100), nullable=False)  # CR name
    day = db.Column(db.String(20), nullable=False)  # Day of the booking
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Booking creation timestamp

    def __repr__(self):
        return f"<ClassroomBooking {self.classroom_name} - {self.timing} by {self.cr_name}>"

# Routes
@app.route('/')
def home():
    return "Server is running!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    year = data.get('year')
    section = data.get('section')
    phone = data.get('phone')

    if not all([name, email, password, year, section, phone]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    if not email.endswith('@rguktrkv.ac.in'):
        return jsonify({'success': False, 'message': 'Invalid email domain'}), 400

    if not re.match(r'^\d{10}$', phone):
        return jsonify({'success': False, 'message': 'Invalid phone number'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    new_user = User(name=name, email=email, password=password, year=year, section=section, phone=phone)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Signup request sent for admin approval'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Database error'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    if email == "admincbs@rguktrkv.ac.in" and password == "Admin@CBS":
        return jsonify({'success': True, 'message': 'Admin login successful', 'role': 'admin'}), 200

    cr = CR.query.filter_by(email=email).first()
    if cr and cr.password == password:
        return jsonify({'success': True, 'message': 'Login successful', 'user_id': cr.id, 'role': 'cr'}), 200

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        if user.approved:
            return jsonify({'success': True, 'message': 'Login successful (User)', 'user_id': user.id, 'role': 'user'}), 200
        else:
            return jsonify({'success': False, 'message': 'User not approved yet'}), 403

    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/get-signup-requests', methods=['GET'])
def get_signup_requests():
    unapproved_users = User.query.filter_by(approved=False).all()

    if not unapproved_users:
        return jsonify({"success": False, "message": "No signup requests available."}), 200

    user_data = [{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "section": user.section,
        "year": user.year
    } for user in unapproved_users]

    return jsonify({"success": True, "requests": user_data}), 200

@app.route('/approve-cr', methods=['POST'])
def approve_cr():
    data = request.get_json()
    user_id = data.get('id')
    phone = data.get('phone')
    batch = data.get('batch')

    if not all([user_id, phone, batch]):
        return jsonify({"error": "Missing required approval details."}), 400

    user = User.query.get(user_id)
    if user:
        new_cr = CR(name=user.name, email=user.email, password=user.password, year=user.year,
                    section=user.section, phone=phone, batch=batch)
        try:
            db.session.add(new_cr)
            db.session.delete(user)
            db.session.commit()
            return jsonify({"success": True, "message": "CR approved and moved to CR list."}), 200
        except Exception:
            db.session.rollback()
            return jsonify({"error": "An error occurred during approval."}), 500

    return jsonify({"error": "User not found."}), 400

@app.route('/reject-cr', methods=['POST'])
def reject_cr():
    data = request.get_json()
    user_id = data.get('id')

    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"success": True, "message": "Signup request rejected."}), 200
        except Exception:
            db.session.rollback()
            return jsonify({"success": False, "message": "Error while rejecting."}), 500

    return jsonify({"success": False, "message": "User not found."}), 404

@app.route('/approved-crs', methods=['GET'])
def get_approved_crs():
    crs = CR.query.all()
    if not crs:
        return jsonify({"success": False, "message": "No approved CRs found."}), 404

    cr_data = [{
        "id": cr.id,
        "name": cr.name,
        "email": cr.email,
        "phone": cr.phone,
        "section": cr.section,
        "year": cr.year,
        "batch": cr.batch
    } for cr in crs]

    return jsonify({"success": True, "crs": cr_data}), 200

@app.route('/remove-cr', methods=['POST'])
def remove_cr():
    data = request.get_json()
    cr_id = data.get('id')

    cr = CR.query.get(cr_id)
    if cr:
        try:
            db.session.delete(cr)
            db.session.commit()
            return jsonify({"success": True, "message": "CR removed successfully."}), 200
        except Exception:
            db.session.rollback()
            return jsonify({"success": False, "message": "Error while removing CR."}), 500
    return jsonify({"success": False, "message": "CR not found."}), 404

@app.route('/report-issue', methods=['POST'])
def report_issue():
    try:
        data = request.get_json()
        cr_email = data.get("crEmail")
        issue_title = data.get("issueTitle")
        issue_description = data.get("issueDescription")
        date_str = data.get("date")

        if not cr_email or not issue_title or not issue_description or not date_str:
            return jsonify({"success": False, "message": "Missing fields"}), 400

        cr = CR.query.filter_by(email=cr_email).first()
        if not cr:
            return jsonify({"success": False, "message": "CR not found"}), 404

        timestamp = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

        new_issue = Issue(
            cr_id=cr.id,
            subject=issue_title,
            description=issue_description,
            timestamp=timestamp
        )

        db.session.add(new_issue)
        db.session.commit()

        return jsonify({"success": True, "message": "Issue reported successfully"}), 200

    except Exception as e:
        print("Error reporting issue:", e)
        return jsonify({"success": False, "message": "An error occurred while reporting the issue"}), 500

@app.route('/issues', methods=['GET'])
def get_issues():
    issues = Issue.query.order_by(Issue.timestamp.desc()).all()
    result = []
    for issue in issues:
        cr = issue.cr
        result.append({
            'id': issue.id,
            'subject': issue.subject,
            'description': issue.description,
            'timestamp': issue.timestamp,
            'resolved': issue.resolved,
            'cr_name': cr.name if cr else None,
            'cr_email': cr.email if cr else None,
            'reply': issue.reply.message if issue.reply else None
        })

    return jsonify({'success': True, 'issues': result}), 200

@app.route('/reply-to-issue', methods=['POST'])
def reply_to_issue():
    data = request.get_json()
    issue_id = data.get('issue_id')
    message = data.get('message')

    if not all([issue_id, message]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    issue = db.session.get(Issue, issue_id)

    if not issue:
        return jsonify({'success': False, 'message': 'Issue not found'}), 404

    try:
        reply = AdminReply(issue_id=issue_id, message=message)
        issue.resolved = True
        db.session.add(reply)
        db.session.commit()

        if issue.cr:
           cr_email = issue.cr.email
           cr_name = issue.cr.name
           msg = Message(
                'Response to Your Reported Issue',
                recipients=[cr_email],
                body=f"Dear {cr_name},\n\n"
                     f"The admin has replied to your reported issue:\n\n"
                     f"Subject: {issue.subject}\n"
                     f"Reply: {message}\n\n"
                     "Kind regards,\nYour Admin Team"
            )   
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Reply submitted successfully and email sent'}), 200

    except Exception as e:
        db.session.rollback()
        print("Error while replying:", str(e))
        return jsonify({'success': False, 'message': f'Error while submitting reply: {str(e)}'}), 500

@app.route('/book-classroom/<day>', methods=['POST'])
def book_classroom(day):
    data = request.get_json()
    classroom_name = data.get('classroom_name')
    timing = data.get('timing')
    subject = data.get('subject')
    faculty = data.get('faculty')
    user_email = data.get('cr_email')  # Email of the logged-in user

    # Assign the day directly as 'today' or 'tomorrow'
    booking_day = day.lower()
    # Validate input
    if not all([classroom_name, timing, subject, faculty, user_email, booking_day]):
        return jsonify({'success': False, 'message': 'All fields are required, including day'}), 400

    # Validate timing format (e.g., "8:00 to 9:00")
    if not re.match(r'^\d{1,2}:\d{2} to \d{1,2}:\d{2}$', timing):
        return jsonify({'success': False, 'message': 'Invalid timing format. Use "8:00 to 9:00"'}), 400
    
  
    # Get CR name based on the logged-in user
    cr = CR.query.filter_by(email=user_email).first()
    if not cr:
        return jsonify({'success': False, 'message': 'CR not found for the logged-in user'}), 404

    cr_name = cr.name

      # Filter bookings based on the day column and booking_day
    existing_bookings = ClassroomBooking.query.filter_by(day=booking_day, timing=timing, classroom_name=classroom_name, cr_name=cr_name).first()
    if existing_bookings:
        return jsonify({'success': False, 'message': 'Classroom is already booked for this timing on the selected day'}), 400

    # Create a new booking
    new_booking = ClassroomBooking(
        classroom_name=classroom_name,
        timing=timing,
        subject=subject,
        faculty=faculty,
        cr_name=cr_name,
        day=booking_day  # Use the booking_day variable
    )

    try:
        db.session.add(new_booking)
        db.session.commit()
        print(classroom_name)
        return jsonify({
                'success': True,
                'message': 'Classroom booked successfully',
                'total_bookings': ClassroomBooking.query.count(),
                'all_bookings': [
                {
                    'classroom_name': booking.classroom_name,
                    'timing': booking.timing,
                    'subject': booking.subject,
                    'faculty': booking.faculty,
                    'cr_name': booking.cr_name,
                    'day': booking.day
                } for booking in ClassroomBooking.query.filter_by(classroom_name=classroom_name).all()
                ]
            }), 200
    except Exception as e:
        db.session.rollback()
        print("Error while booking classroom:", str(e))
        return jsonify({'success': False, 'message': 'An error occurred while booking the classroom'}), 500
    
@app.route('/get-bookings<classroom_name>', methods=['GET'])
def get_bookings(classroom_name):
    try:
        # Fetch all bookings from the database
        bookings = ClassroomBooking.query.filter_by(classroom_name=classroom_name).all()

        # Format the bookings into a list of dictionaries
        booking_data = [
            {
                'classroom_name': booking.classroom_name,
                'timing': booking.timing,
                'subject': booking.subject,
                'faculty': booking.faculty,
                'cr_name': booking.cr_name,
                'day': booking.day,
                'timestamp': booking.timestamp
            }
            for booking in bookings
        ]

        return jsonify({'success': True, 'bookings': booking_data}), 200
    except Exception as e:
        print("Error fetching bookings:", str(e))
        return jsonify({'success': False, 'message': 'An error occurred while fetching bookings'}), 500

#Flask App Execution**:
# Runs the Flask app in debug mode.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
