# AWS Web-Hosted Cloud Music Subscription Application

Welcome to the AWS Web-Hosted Cloud Music Subscription Application! This project is a cloud-based web application that allows users to register, log in, query a music database, subscribe to songs, and manage their subscriptions. The application leverages various AWS services such as EC2, S3, DynamoDB, API Gateway, and Lambda functions.

---

## Project Overview

This project is developed as part of a larger project to create a cloud-based music subscription application using AWS services. The application is fully hosted on an AWS EC2 instance running Ubuntu Server and is accessible via a web browser using the EC2 instance's public DNS.

The application allows users to:

- Register and log in.
- Query a music database.
- Subscribe to songs.
- Manage their subscriptions.
- Securely access artist images stored in S3.

---

## Features

- **User Authentication:**
  - Secure user registration and login system.
  - Passwords are stored securely in DynamoDB.

- **Music Database Querying:**
  - Users can search for songs by title, artist, and year.
  - Displays query results with song information and artist images.

- **AWS Integration:**
  - Uses DynamoDB for data storage.
  - Stores artist images in S3 and generates presigned URLs.
  - API Gateway and Lambda functions handle registration and subscription actions.

- **Responsive Web Design:**
  - User-friendly interfaces built with HTML and Bootstrap.
  - Consistent styling and animations for better user experience.

---

## AWS Services Used

- **EC2 (Elastic Compute Cloud):** Hosts the web application on an Ubuntu Server instance.
- **S3 (Simple Storage Service):** Stores artist images securely.
- **DynamoDB:** NoSQL database service used to store user, music, and subscription data.
- **API Gateway:** Exposes REST API endpoints for interacting with Lambda functions.
- **Lambda Functions:** Executes backend logic for user registration and subscription management.
- **IAM (Identity and Access Management):** Manages roles and permissions for AWS services.
- **Boto3:** AWS SDK for Python used to interact with AWS services programmatically.

---

## Prerequisites

- **AWS Account:** You need an AWS account with access to the AWS Management Console.
- **AWS CLI:** Installed and configured with your AWS credentials.
- **Python 3.x:** Installed on your local machine or EC2 instance.
- **Flask:** Python web framework used for the application.
- **Boto3:** AWS SDK for Python.
- **An EC2 Instance:** Ubuntu Server 20.04 LTS recommended.

---

## Installation and Setup

### 1. Launch an EC2 Instance

- Launch an Ubuntu Server 20.04 LTS EC2 instance.
- Configure security groups to allow inbound traffic on ports 80 (HTTP) and 443 (HTTPS).
- Associate an IAM role with necessary permissions for DynamoDB, S3, API Gateway, and Lambda.

### 2. Connect to the EC2 Instance

- Use SSH to connect to your EC2 instance.

  ```bash
  ssh -i /path/to/your/key.pem ubuntu@your-ec2-public-dns
  ```

### 3. Install Required Packages

- Update the package lists:

  ```bash
  sudo apt update
  ```

- Install Python 3 and pip:

  ```bash
  sudo apt install python3 python3-pip -y
  ```

- Install Flask and Boto3:

  ```bash
  pip3 install flask boto3 requests
  ```

- Install Apache2 web server:

  ```bash
  sudo apt install apache2 libapache2-mod-wsgi-py3 -y
  ```

### 4. Clone the Repository

- Clone your project repository to the EC2 instance.

  ```bash
  git clone https://github.com/reyiyama/aws-cloud-music-app.git
  ```

- Navigate to the project directory:

  ```bash
  cd aws-cloud-music-app
  ```

### 5. Configure AWS Credentials

- Since the EC2 instance has an IAM role attached, AWS services can be accessed without explicit credentials.

### 6. Set Up the Application

- **Task 1:** Run `task1.py` to set up DynamoDB tables and load data.

  ```bash
  python3 task1.py
  ```

- **Task 2:** Run `task2.py` to download artist images and upload them to S3.

  ```bash
  python3 task2.py
  ```

- **Configure Apache2:**

  - Create a new Apache2 configuration file for the Flask application.

    ```bash
    sudo nano /etc/apache2/sites-available/your-app.conf
    ```

  - Add the following configuration:

    ```apache
    <VirtualHost *:80>
    ServerName ec2-3-226-76-29.compute-1.amazonaws.com

    WSGIDaemonProcess aws-music python-home=/home/ubuntu/AWS_MUSIC_SYSTEM/venv python-path=/home/ubuntu/AWS_MUSIC_SYSTEM threads=5
    WSGIProcessGroup aws-music
    WSGIScriptAlias / /home/ubuntu/AWS_MUSIC_SYSTEM/app.wsgi

    <Directory /home/ubuntu/AWS_MUSIC_SYSTEM>
        Require all granted
        Options FollowSymLinks
        AllowOverride All
    </Directory>

    Alias /static /home/ubuntu/AWS_MUSIC_SYSTEM/static
    <Directory /home/ubuntu/AWS_MUSIC_SYSTEM/static>
        Require all granted
        Options FollowSymLinks
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/aws-music-error.log
    CustomLog ${APACHE_LOG_DIR}/aws-music-access.log combined
</VirtualHost>
    ```

  - Enable the site and restart Apache2:

    ```bash
    sudo a2ensite your-app
    sudo systemctl restart apache2
    ```

---

## Usage

- Access the application by entering your EC2 instance's public DNS in your web browser.

  ```
  http://your-ec2-public-dns
  ```

- **Register a New User:**

  - Click on the "Register" link on the login page.
  - Fill in the email, username, and password fields.
  - If the email is unique, the account will be created, and you'll be redirected to the login page.

- **Login:**

  - Enter your email and password on the login page.
  - If the credentials are valid, you'll be redirected to the main page.

- **Main Page Features:**

  - **User Area:** Displays your username.
  - **Subscription Area:** Shows your subscribed songs with artist images.
    - Click "Remove" to unsubscribe from a song.
  - **Query Area:** Search for songs by title, artist, or year.
    - Click "Query" to display matching songs.
    - Click "Subscribe" to add a song to your subscriptions.

- **Logout:**

  - Click the "Logout" link to end your session and return to the login page.

---

#### Common Functionality Across All Versions

- **User Session Management:**
  - Ensures the user is logged in before accessing main features.
  - Redirects unauthenticated users to the login page.

- **Query Area:**
  - Allows users to search for songs by title, artist, and year.
  - Builds a filter expression based on provided criteria.
  - Retrieves matching songs from the `music` table in DynamoDB.
  - Displays query results with an option to subscribe.

- **Logout:**
  - Clears the user session and redirects to the login page.

---
