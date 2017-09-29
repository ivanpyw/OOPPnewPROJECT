from flask import Flask, render_template
# from firebase import firebase


app = Flask(__name__)

#accessing firebase
# firebase = firebase.FirebaseApplication('https://my-python-project-dae81.firebaseio.com/')

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
