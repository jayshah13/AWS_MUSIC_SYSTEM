from flask import Blueprint, render_template, request, redirect, flash
import boto3

register_blueprint = Blueprint('register', __name__, url_prefix='/register', template_folder='templates')

# DynamoDB setup and referreicing the login table made in task 1 (also carried forward in login.py)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
login_table = dynamodb.Table('login')

@register_blueprint.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Checking if the email already exists in DynamoDB
        response = login_table.get_item(Key={'email': email})
        user_exists = 'Item' in response

        if user_exists:
            flash('The email already exists.', 'error')
        else:
            # Creating new user in DynamoDB
            user_data = {
                'email': email,
                'user_name': username,
                'password': password
            }
            login_table.put_item(Item=user_data)
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')

    return render_template('register.html')