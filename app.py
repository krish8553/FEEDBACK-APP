from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail   # Make sure this is correctly implemented

app = Flask(__name__)

# Configuration
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname/database_name'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Definition
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True, nullable=False)
    dealer = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        
        if not customer or not dealer:
            return render_template('index.html', message='Please enter required fields')

        # Check for existing feedback
        existing_feedback = Feedback.query.filter_by(customer=customer).first()
        if existing_feedback:
            return render_template('index.html', message='You have already submitted feedback.')

        # Create new feedback
        new_feedback = Feedback(customer=customer, dealer=dealer, rating=int(rating), comments=comments)

        try:
            db.session.add(new_feedback)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)  # Send the email
            return render_template('success.html')
        except Exception as e:
            db.session.rollback()  # Roll back the session in case of error
            return render_template('index.html', message='Error saving feedback: ' + str(e))

# Email Configuration
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'dc16b9de187c00'
app.config['MAIL_PASSWORD'] = '8c4c79264426b8'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Main Block
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run()
