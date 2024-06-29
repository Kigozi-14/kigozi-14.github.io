from flask import Flask, render_template, request, redirect, url_for, flash
from leetcode_progress import my_data
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/myblog'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


# THIS IS OUR DATABASE MODEL (FOR OUR POSTS)
class my_posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(12))
    description = db.Column(db.String(200))
    photo = db.Column(db.LargeBinary)

    def __init__(self, date, description, photo):
        self.date = date
        self.description = description
        self.photo = photo

# FUNCTION TO CHECK WHETHER THE FILE BEING PASSED INTO OUR FORM IS AN IMAGE
def image_checking(image_name):
    file_types = {'jpg', 'png', 'PNG', 'JPG'}
    exte = None
    for i in range(len(image_name)-1, -1, -1):
        if image_name[i] == '.':
            exte = image_name[i+1:]
            break
    if exte in file_types:
        return True
    else:
        return False

# FUNCTION TO CHECK WHETHER MY PASSWORD IS CORRECT
def password_checking(password):
    if password == 'E1234@ria':
        return True
    else:
        return False
    
# ROUTE FOR OUR HOME PAGE (THE LANDING)
@app.route('/')
def home():
    posts = my_posts.query.all()
    for post in posts:
        if post.photo:
            post.photo = base64.b64encode(post.photo).decode('utf-8')
    leet_code_data = my_data('Kigozi_Eria')
    easy = leet_code_data[0]
    medium = leet_code_data[1]
    hard = leet_code_data[2]
    all = leet_code_data[3]
    return render_template('index.html', posts=posts, easy=easy, medium=medium, hard=hard, all=all)

# ROUTE FOR OUR POSTING PAGE
@app.route('/posting')
def post():
    return render_template('posting.html')

# ROUTE TO PICK DATA FROM THE FORM AND SUBMIT IT FOR POSTING
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        my_date = request.form['currentDate']
        my_description = request.form['description']
        my_password  = request.form['password']
        my_image= request.files['image_file'].read()
        photo_name = request.files['image_file']
        image_name = photo_name.filename
        if my_description != '' and image_checking(image_name) == True and password_checking(my_password) == True:
            post_data = my_posts(my_date, my_description, my_image)
            db.session.add(post_data)
            db.session.commit()
            print(my_date, image_name, my_description, my_password)
            return redirect(url_for('home'))
        else:
            return render_template('posting.html', message='Please enter required fields....  you might have entered a wrong image file type or a wrong password')
    return redirect(url_for('home'))

# DISPLAY IMAGE BY HITTING ITS ID
@app.route('/delete', methods=['POST'])
def delete_photo():
    del_id = request.form.get('to_delete')
    to_del = my_posts.query.get(del_id)
    if to_del is None:
        return redirect(url_for('home'))
    if password_checking:  # Make sure this is implemented securely
        try:
            db.session.delete(to_del)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.run()


