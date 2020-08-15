from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)
app.secret_key = "mohit"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/signup')
def signup_template():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(port=5000)
