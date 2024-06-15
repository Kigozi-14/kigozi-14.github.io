from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posting')
def post():
    return render_template('posting.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        my_date = request.form['currentDate']
        my_description = request.form['description']
        my_image= request.files['image_file'].read()
        photo_name = request.files['image_file']
        image_name = photo_name.filename
        print(my_date, image_name, my_description)
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()