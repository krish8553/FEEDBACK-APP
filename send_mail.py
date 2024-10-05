import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
    port = 587
    smtp_server = 'sandbox.smtp.mailtrap.io'
    login = 'dc16b9de187c00'
    password = '8c4c79264426b8'
    
    # Create message
    message = f"""
    <h3>New Feedback Submission</h3>
    <ul>
        <li>Customer: {customer}</li>
        <li>Dealer: {dealer}</li>
        <li>Rating: {rating}</li>
        <li>Comments: {comments}</li>
    </ul>
    """
    
    sender_email = 'email1@example.com'  # Replace with your sender email
    receiver_email = 'email2@example.com'  # Replace with your receiver email
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Start TLS encryption
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {str(e)}")
