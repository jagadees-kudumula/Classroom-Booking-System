SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
"""
This configuration file is used to set up and manage the application's settings, 
including database and email configurations.

Attributes:
    SQLALCHEMY_DATABASE_URI (str): The URI for the SQLite database used by SQLAlchemy.
    SQLALCHEMY_TRACK_MODIFICATIONS (bool): A flag to disable SQLAlchemy's event system 
        for performance improvements.

Email Configuration:
    MAIL_SERVER (str): The SMTP server address for sending emails.
    MAIL_PORT (int): The port number for the SMTP server.
    MAIL_USE_TLS (bool): A flag to enable Transport Layer Security (TLS) for secure email communication.
    MAIL_USERNAME (str): The email address used for authentication with the SMTP server.
    MAIL_PASSWORD (str): The password for the email account used for authentication.
    MAIL_DEFAULT_SENDER (str): The default sender email address for outgoing emails.

Note:
    Replace 'MAIL_USERNAME' and 'MAIL_PASSWORD' with your actual email credentials.
    Ensure that sensitive information like email credentials is stored securely 
    and not hardcoded in production environments.
"""
SQLALCHEMY_TRACK_MODIFICATIONS = False

from flask_mail import Mail, Message

# Add this to your Flask app configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change this for other email providers
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'boydevil77740@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'aaaa'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'boydevil77740@gmail.com'

# Initialize Flask-Mail
mail = Mail(app)

