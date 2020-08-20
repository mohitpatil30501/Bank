from flask import Flask, render_template, request, redirect, session
import random
from module.login import LogIn
from module.signup import SignUp
from module.profile import Profile
from module.deposit import Deposit
from module.withdraw import Withdraw
from database.database import Database

app = Flask(__name__)
app.secret_key = "mohit"


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/withdraw', methods=['POST'])
def withdraw_template():
    return render_template('withdraw.html')


@app.route('/auth/withdraw', methods=['POST'])
def withdraw_user():
    payment_amount = request.form['withdraw']
    Withdraw.Otp_Call(payment_amount)
    return redirect('/otp', code=307)


@app.route('/proceed/withdraw', methods=['POST'])
def Proceed_Withdraw():
    if session['otp_progress']:
        withdraw_object = Withdraw(session['payment_amount'], session['username'], session['name'], session['mobile'],
                                   session['balance'], session['key'])
        withdraw_process_status = withdraw_object.Proceed_withdraw()
        if withdraw_process_status:
            return redirect('/success', code=307)
        else:
            return render_template('error.html', title="Error", text="Oops..", path="/")
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/deposit', methods=['POST'])
def deposit_template():
    return render_template('deposit.html')


@app.route('/auth/deposit', methods=['POST'])
def deposit_user():
    payment_amount = request.form['deposit']
    Deposit.Otp_Call(payment_amount)
    return redirect('/otp', code=307)


@app.route('/proceed/deposit', methods=['POST'])
def Proceed_Deposit():
    if session['otp_progress']:
        deposit_object = Deposit(session['payment_amount'], session['username'], session['name'], session['mobile'],
                                 session['balance'], session['key'])
        deposit_process_status = deposit_object.Proceed_Deposit()
        if deposit_process_status:
            return redirect('/success', code=307)
        else:
            return render_template('error.html', title="Error", text="Oops..", path="/")
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/otp', methods=['POST'])
def otp_template():
    session['otp'] = generate_otp = int(random.randint(100000, 999999))
    # Send otp using sms
    print("OTP:" + str(generate_otp))
    # ==================
    mobile = '*******' + session['mobile'][-3:]
    return render_template('otp.html', mobile=mobile)


@app.route('/auth/otp', methods=['POST'])
def otp_user():
    otp = request.form['otp']
    if str(otp) == str(session['otp']):
        session['otp_progress'] = True
        return redirect("/proceed/" + session['process'], code=307)
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/profile', methods=['POST'])
def profile_template():
    user_profile_object = Profile()
    if user_profile_object.username is not None:
        user_profile_object.Data_Decode()
        return render_template('profile.html', name=user_profile_object.name, balance=user_profile_object.balance)
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/success', methods=['POST'])
def Success():
    return render_template("success.html")


@app.route('/logout')
def Logout():
    Profile.logout()
    return redirect("/")


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    login_account_object = LogIn(username, password)
    result = login_account_object.Check_Username()
    if result:
        login_account_object.User_session_create()
        return redirect("/profile", code=307)
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/register')
def register_template():
    return render_template('signup.html')


@app.route('/proceed/register', methods=['POST'])
def Proceed_Register():
    if session['otp_progress']:
        name = session['register_data']['name']
        mobile = session['register_data']['mobile']
        username = session['register_data']['username']
        password = session['register_data']['password']
        confirm_password = session['register_data']['confirm_password']
        create_account_object = SignUp(name, mobile, username, password, confirm_password)
        result = create_account_object.Check_Retype_Password()
        if result:
            create_account_object.User_session_create()
            return redirect("/profile", code=307)
        else:
            return render_template('error.html', title="Error", text="Oops..", path="/")
    else:
        return render_template('error.html', title="Error", text="Oops..", path="/")


@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['first_name'] + " " + request.form['last_name']
    mobile = request.form['mobile']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    session['register_data'] = {
        'name': name,
        'mobile': mobile,
        'username': username,
        'password': password,
        'confirm_password': confirm_password
    }
    session['mobile'] = str(mobile)
    SignUp.Otp_Call()
    return redirect('/otp', code=307)


@app.route('/')
def home_template():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
