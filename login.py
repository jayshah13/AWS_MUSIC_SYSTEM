from flask import Blueprint, render_template, request, redirect, session, flash
import boto3

# Ccreating a Blueprint for the login
login_blueprint = Blueprint('login', __name__, template_folder='templates')

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
login_table = dynamodb.Table('login')

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # retrieve the user from DynamoDB login table
        response = login_table.get_item(Key={'email': email})
        user_data = response.get('Item')

        if user_data and user_data['password'] == password:
            session['email'] = email
            session['username'] = user_data['user_name']
            flash('Login successful!', 'success')
            return redirect('/main')
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')