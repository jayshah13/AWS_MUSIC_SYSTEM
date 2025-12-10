from flask import Flask, render_template, request, redirect, session, url_for, flash
from login import login_blueprint
from register import register_blueprint
import requests
import boto3

#this python file is actually my attempt to integrate the Lambda Functions with the functionality of the application

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.secret_key = '\xa4\xa5y\x14\xb7\xff.m|i'

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
music_table = dynamodb.Table('music')
subscription_table = dynamodb.Table('subscription')

#API HANDLING
API_BASE_URL = 'https://{api-id}.execute-api.{region}.amazonaws.com/{stage}'

# S3 setup
s3 = boto3.client('s3')
bucket_name = 'music-app-images'

@app.route('/')
def index():
    if 'email' in session:
        return redirect('/main')
    return redirect('/login')

@app.route('/main')
def main():
    if 'email' not in session:
        flash('Please login to access this page.', 'info')
        return redirect('/login')

    email = session['email']
    username = session.get('username', 'User')

    # Fetching subscriptions from DynamoDB
    response = subscription_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
    )
    subscriptions = response.get('Items', [])

    # Retrieveing artist images from S3
    for subscription in subscriptions:
        artist = subscription['artist']
        image_name = f"{artist}.jpg"
        image_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': image_name},
            ExpiresIn=3600  # URL expiration time in seconds
        )
        subscription['image_url'] = image_url

    return render_template('main.html', username=username, subscriptions=subscriptions)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        year = request.form.get('year')

        # Building filter expression for query
        filters = []
        if title:
            filters.append(boto3.dynamodb.conditions.Attr('title').eq(title))
        if artist:
            filters.append(boto3.dynamodb.conditions.Attr('artist').eq(artist))
        if year:
            filters.append(boto3.dynamodb.conditions.Attr('year').eq(year))

        # Combining filters into a single condition if multiple filters exist
        filter_expression = None
        if filters:
            filter_expression = filters[0]
            for f in filters[1:]:
                filter_expression &= f

        # Execute query
        if filter_expression:
            response = music_table.scan(FilterExpression=filter_expression)
            query_results = response.get('Items', [])
        else:
            query_results = []

        # Retrieve artist images from S3
        for result in query_results:
            artist = result['artist']
            image_name = f"{artist}.jpg"
            image_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': image_name},
                ExpiresIn=3600  # URL expiration time in seconds
            )
            result['image_url'] = image_url

        if not query_results:
            flash("No result is retrieved. Please query again.", 'info')

        return render_template('main.html', query_results=query_results, show_subscribe=True, username=session.get('username'))

    return render_template('query.html')







@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = session['email']
    title = request.form['title']
    artist = request.form['artist']
    
    subscription_data = {
        'email': email,
        'title': title,
        'artist': artist
    }
    
    response = requests.post(f'{API_BASE_URL}/subscriptions', json=subscription_data)
    
    if response.status_code == 201:
        flash('Subscription added successfully!', 'success')
    else:
        flash('Failed to add subscription. Please try again.', 'error')
    
    return redirect(url_for('main'))

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = session['email']
    title = request.form['title']
    
    response = requests.delete(f'{API_BASE_URL}/unsubscribe', params={
        'email': email,
        'title': title
    })
    
    if response.status_code == 200:
        flash('Subscription removed successfully!', 'info')
    else:
        flash('Failed to remove subscription. Please try again.', 'error')
    
    return redirect(url_for('main'))








#@app.route('/subscribe', methods=['POST'])
#def subscribe():
 #   email = session['email']
  #  title = request.form['title']
   # artist = request.form['artist']

    # Create subscription in DynamoDB
    #subscription_data = {
     #   'email': email,
      #  'title': title,
       # 'artist': artist
   # }
    #subscription_table.put_item(Item=subscription_data)

    #flash('Subscription added successfully!', 'success')
    #return redirect(url_for('main'))

#@app.route('/unsubscribe', methods=['POST'])
#def unsubscribe():
 #   email = session['email']
  #  title = request.form['title']
   # artist = request.form['artist']

    # Remove subscription from DynamoDB
    #subscription_table.delete_item(Key={'email': email, 'title': title, 'artist': artist})

    #flash('Subscription removed successfully!', 'info')
   # return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
