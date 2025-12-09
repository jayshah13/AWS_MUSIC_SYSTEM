from flask import Blueprint, render_template, request, redirect, flash
import boto3

register_blueprint = Blueprint('register', __name__, url_prefix='/register', template_folder='templates')

# DynamoDB setup and referencing the login table made in task 1 (also carried forward in login.py)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
login_table = dynamodb.Table('login')

@register_blueprint.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

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
            flash('The username already exists. Please choose a different username.', 'error')
            return render_template('register.html')
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
