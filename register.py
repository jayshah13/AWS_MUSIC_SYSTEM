from flask import Blueprint, render_template, request, redirect, flash
import boto3
import re

register_blueprint = Blueprint(
    'register',
    url_prefix='/register',
    template_folder='templates'
)

# DynamoDB setup and referencing the login table
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
login_table = dynamodb.Table('login')

# Password validation: min 8 chars, lowercase, uppercase, digit, special char
PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
)

def is_strong_password(password: str) -> bool:
    return bool(PASSWORD_PATTERN.match(password))


@register_blueprint.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Validate password strength
        if not is_strong_password(password):
            flash(
                'Password must be at least 8 characters and include '
                'uppercase, lowercase, number, and special character.',
                'error'
            )
            return render_template('register.html')

        # Checking if the email already exists in DynamoDB
        email_response = login_table.get_item(Key={'email': email})
        email_exists = 'Item' in email_response

        # Checking if the username already exists in DynamoDB
        username_response = login_table.scan(
            FilterExpression='user_name = :username',
            ExpressionAttributeValues={':username': username}
        )
        username_exists = bool(username_response['Items'])

        if email_exists:
            flash('The email already exists.', 'error')
            return render_template('register.html')
        elif username_exists:
            flash(
                'The username already exists. Please choose a different username.',
                'error'
            )
            return render_template('register.html')
        else:
            # Creating new user in DynamoDB
            user_data = {
                'email': email,
                'user_name': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name
            }
            login_table.put_item(Item=user_data)
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')

    return render_template('register.html')
