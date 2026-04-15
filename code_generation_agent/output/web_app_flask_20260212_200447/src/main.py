#Here's the implementation of the Flask web app with all the requested components:

#```python
"""
Main Flask application module for sending emails.
"""

import os
import re
import smtplib
from email.message import EmailMessage
from typing import Dict, Optional, Tuple
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Config:
    """Configuration class for SMTP settings."""
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'noreply@example.com')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

app.config.from_object(Config())

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validates an email address format.

    Args:
        email: The email address to validate.

    Returns:
        Tuple containing (is_valid, error_message). If valid, error_message is None.
    """
    if not email:
        return False, "Email cannot be empty"

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, None

def send_email(recipient: str, subject: str, body: str) -> Dict[str, str]:
    """
    Sends an email using SMTP.

    Args:
        recipient: The email address to send to.
        subject: The subject of the email.
        body: The body content of the email.

    Returns:
        Dictionary with 'success' status and 'message' describing the result.
    """
    try:
        msg = EmailMessage()
        msg['From'] = app.config['SENDER_EMAIL']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(app.config['SMTP_USERNAME'], app.config['SMTP_PASSWORD'])
            server.send_message(msg)

        return {'success': True, 'message': 'Email sent successfully'}

    except smtplib.SMTPException as e:
        return {'success': False, 'message': f'SMTP error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'message': f'Error sending email: {str(e)}'}

@app.route('/', methods=['GET'])
def index() -> str:
    """
    Renders the main page with the email form.

    Returns:
        Rendered HTML template.
    """
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email_route() -> jsonify:
    """
    Handles the email sending request from the form.

    Returns:
        JSON response with success status and message.
    """
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'success': False, 'message': 'Email field is required'}), 400

    email = data['email'].strip()

    # Validate email format
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        return jsonify({'success': False, 'message': error_msg}), 400

    # Send email
    result = send_email(
        recipient=email,
        subject='Test Email from Flask App',
        body='This is a test email sent from the Flask application.'
    )

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
#```

#```python
"""
HTML template for the email form.
"""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Sender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="email"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        #message {
            margin-top: 15px;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background-color: #dff0d8;
            color: #3c763d;
        }
        .error {
            background-color: #f2dede;
            color: #a94442;
        }
    </style>
</head>
<body>
    <h1>Email Sender</h1>
    <form id="emailForm">
        <div class="form-group">
            <label for="email">Recipient Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <button type="submit">Send Email</button>
    </form>
    <div id="message"></div>

    <script>
        document.getElementById('emailForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const messageDiv = document.getElementById('message');

            try {
                const response = await fetch('/send-email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email: email })
                });

                const data = await response.json();

                if (data.success) {
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'success';
                    document.getElementById('email').value = '';
                } else {
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'error';
                }
            } catch (error) {
                messageDiv.textContent = 'An error occurred while sending the email';
                messageDiv.className = 'error';
                console.error('Error:', error);
            }
        });
    </script>
</body>
</html>
#```

#```python
"""
Configuration module for the Flask application.
"""

import os
from typing import Optional

class Config:
    """Base configuration class."""
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.example.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME: Optional[str] = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD: Optional[str] = os.getenv('SMTP_PASSWORD')
    SENDER_EMAIL: str = os.getenv('SENDER_EMAIL', 'noreply@example.com')
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    """Development specific configuration."""
    DEBUG: bool = True

class ProductionConfig(Config):
    """Production specific configuration."""
    DEBUG: bool = False

def get_config(config_name: str = 'DevelopmentConfig') -> Config:
    """
    Returns the appropriate configuration class based on the environment.

    Args:
        config_name: The name of the configuration class to use.

    Returns:
        The configuration class instance.
    """
    config_classes = {
        'DevelopmentConfig': DevelopmentConfig,
        'ProductionConfig': ProductionConfig,
        'Config': Config
    }

    return config_classes.get(config_name, Config)()
#```

#```python
"""
Validator module for input validation.
"""

import re
from typing import Tuple, Optional

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validates an email address format.

    Args:
        email: The email address to validate.

    Returns:
        Tuple containing (is_valid, error_message). If valid, error_message is None.
    """
    if not email:
        return False, "Email cannot be empty"

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"

    return True, None
#```

#```python
"""
Email service module for sending emails.
"""

import smtplib
from email.message import EmailMessage
from typing import Dict
from flask import current_app

def send_email(recipient: str, subject: str, body: str) -> Dict[str, str]:
    """
    Sends an email using SMTP.

    Args:
        recipient: The email address to send to.
        subject: The subject of the email.
        body: The body content of the email.

    Returns:
        Dictionary with 'success' status and 'message' describing the result.
    """
    try:
        msg = EmailMessage()
        msg['From'] = current_app.config['SENDER_EMAIL']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP(current_app.config['SMTP_SERVER'], current_app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(current_app.config['SMTP_USERNAME'], current_app.config['SMTP_PASSWORD'])
            server.send_message(msg)

        return {'success': True, 'message': 'Email sent successfully'}

    except smtplib.SMTPException as e:
        return {'success': False, 'message': f'SMTP error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'message': f'Error sending email: {str(e)}'}
#```

#```python
"""
Test module for the email sender application.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.email_service import send_email
from src.validators import validate_email

class TestEmailSender(unittest.TestCase):
    """Test cases for the email sender application."""

    def test_validate_email_valid(self):
        """Test that valid emails pass validation."""
        self.assertEqual(validate_email('test@example.com'), (True, None))
        self.assertEqual(validate_email('user.name+tag@example.co.uk'), (True, None))

    def test_validate_email_invalid(self):
        """Test that invalid emails fail validation."""
        self.assertEqual(validate_email(''), (False, "Email cannot be empty"))
        self.assertEqual(validate_email('invalid-email'), (False, "Invalid email format"))
        self.assertEqual(validate_email('user@.com'), (False, "Invalid email format"))

    @patch('src.email_service.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending."""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_email('test@example.com', 'Test Subject', 'Test Body')
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'Email sent successfully')

    @patch('src.email_service.smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        """Test email sending failure."""
        mock_smtp.side_effect = smtplib.SMTPException("SMTP Error")

        result = send_email('test@example.com', 'Test Subject', 'Test Body')
        self.assertFalse(result['success'])
        self.assertIn('SMTP error', result['message'])

if __name__ == '__main__':
    unittest.main()
#```

#```python
"""
Main entry point for the Flask application.
"""

from src.app import app
from src.config import get_config

if __name__ == '__main__':
    # Get configuration based on environment
    config = get_config()

    # Update Flask app configuration
    app.config.from_object(config)

    # Run the application
    app.run(host='0.0.0.0', port=5000)
