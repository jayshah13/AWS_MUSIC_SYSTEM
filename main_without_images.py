from flask import Flask, render_template, request, redirect, session, url_for, flash
from login import login_blueprint
from register import register_blueprint
import boto3

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)
app.secret_key ='\xa4\xa5y\x14\xb7\xff.m|i'


# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
music_table = dynamodb.Table('music')
subscription_table = dynamodb.Table('subscription')

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

        # Executing query
        if filter_expression:
            response = music_table.scan(FilterExpression=filter_expression)
            query_results = response.get('Items', [])
        else:
            query_results = []

        if not query_results:
            flash("No result is retrieved. Please query again.", 'info')

        return render_template('main.html', query_results=query_results, show_subscribe=True, username=session.get('username'))

    return render_template('query.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = session['email']
    title = request.form['title']
    artist = request.form['artist']

    # Creating subscription in DynamoDB
    subscription_data = {
        'email': email,
        'title': title,
        'artist': artist
    }
    subscription_table.put_item(Item=subscription_data)

    flash('Subscription added successfully!', 'success')
    return redirect(url_for('main'))

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = session['email']
    title = request.form['title']
    artist = request.form['artist']

    # Removinh subscription from DynamoDB
    subscription_table.delete_item(Key={'email': email, 'title': title, 'artist': artist})

    flash('Subscription removed successfully!', 'info')
    return redirect(url_for('main'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)













