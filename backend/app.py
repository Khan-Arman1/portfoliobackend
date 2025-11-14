import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins= "*") # Allow requests from your frontend
app.secret_key = os.getenv("secret_key") 
print(os.getenv("secret_key"))

# --- Email Configuration ---
# IMPORTANT: Use environment variables for security.
# Do not hardcode your email or password in the code.
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
print(EMAIL_ADDRESS)
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
print(EMAIL_PASSWORD)
# RECIPIENT_EMAIL = "armankhan52210@gmail.com" # The email address where you want to receive messages
RECIPIENT_EMAIL = os.getenv('EMAIL_USER') # The email address where you want to receive messages
print(RECIPIENT_EMAIL)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    if not all(k in data for k in ['name', 'email', 'number', 'message']):
        return jsonify({'error': 'Missing data in request'}), 400

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
         return jsonify({'error': 'Email server is not configured.'}), 500

    name = data['name']
    sender_email = data['email']
    number = data['number']
    message_body = data['message']

    # --- Create the Email ---
    subject = f"New Message from {name} via Portfolio"
    body = f"""
    You received a new message from your portfolio contact form.

    Name: {name}
    Email: {sender_email}
    Phone: {number}

    Message:
    {message_body}
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL

    # --- Send the Email ---
    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp_server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'error': 'Failed to send email.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

