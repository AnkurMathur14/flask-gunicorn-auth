"""Validator Module"""
import re

def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False

def validate_password(password: str):
    """Password Validator"""
    reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)

def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

def validate_user(**args):
    """User Validator"""
    if  not args.get('email') or not args.get('password') or not args.get('username'):
        return False, {
            'email': 'Email is required',
            'password': 'Password is required',
            'username': 'Name is required'
        }
    if not isinstance(args.get('username'), str) or \
        not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return False, {
            'email': 'Email must be a string',
            'password': 'Password must be a string',
            'username': 'Name must be a string'
        }
    if not validate_email(args.get('email')):
        return False, {
            'email': 'Email is invalid'
        }
    if not validate_password(args.get('password')):
        return False, {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    """
    if not 2 <= len(args['username'].split(' ')) <= 30:
        return False, {
            'username': 'Name must be between 2 and 30 words'
        }
    """
    return True, {}

def validate_email_and_password(email, password):
    """Email and Password Validator"""
    if not (email and password):
        return False, {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return False, {
            'email': 'Email is invalid'
        }
    if not validate_password(password):
        return False, {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True, {}

def validate_username_and_password(username, password):
    """Email and Password Validator"""
    if not (username and password):
        return False, {
            'username': 'username is required',
            'password': 'Password is required'
        }

    if not validate_password(password):
        return False, {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True, {}
  