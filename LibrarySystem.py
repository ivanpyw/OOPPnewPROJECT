from flask import Flask, render_template
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators


app = Flask(__name__)

#accessing firebase
# firebase = firebase.FirebaseApplication('https://my-python-project-dae81.firebaseio.com/')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createbook')
def create_book():
    return render_template('create_book.html')


if __name__ == '__main__':
    app.run()
