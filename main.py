from flask import Flask, render_template, request, session, make_response, redirect
from module.login import LogIn
from module.signup import SignUp
from database.database import Database
app = Flask(__name__)
app.secret_key = "mohit"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    login_account_object = LogIn(username, password)
    result = login_account_object.Check_Username()
    if result:
        return redirect("/profile", code=307)
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['first_name']+" "+request.form['last_name']
    mobile = request.form['mobile']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    create_account_object = SignUp(name, mobile, username, password, confirm_password)
    result = create_account_object.Check_Retype_Password()
    if result:
        return redirect("/profile", code=307)
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def signup_template():
    return render_template('signup.html')


@app.route('/profile', methods=['POST'])
def profile_template():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
