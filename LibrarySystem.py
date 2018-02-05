from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField

from Users import Users
import firebase_admin
from firebase_admin import credentials, db
from StaffU import StaffU
from Create_request import CreateRequest
from descbill import Descbill
from datetime import datetime
# from passlib.hash import sha256_crypt #need to pip install passlib on the command prompt

cred = credentials.Certificate('cred/stop-78245-firebase-adminsdk-jqcbt-d793e7c23d.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://stop-78245.firebaseio.com/'

})


root = db.reference()
app = Flask(__name__)

class ProductForm(Form):
    product = StringField('Name', [validators.DataRequired()])
    quantity = StringField('Quantity', [validators.DataRequired()])
    price = StringField('Price',[validators.DataRequired()])

@app.route('/bill')
def bill():

    listofp = root.child('productDesc').get()
    list = []
    for pubid in listofp:
        eachupdate = listofp[pubid]

        bill = Descbill(eachupdate['product'], eachupdate['quantity'], eachupdate['price'])
        bill.set_pubid(pubid)
        print("ID: {}, Product: {}, Quantity: {}, Price:$ {}".format(bill.get_pubid(), bill.get_product(),bill.get_quantity(), bill.get_price()))
        # print(bill.get_product())
        list.append(bill)
    return render_template('bill.html', listofp=list)

class StaffLogin(Form):
    staffid = StringField('Staff id', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    type = RadioField('Type', choices=[('tDoctor', 'Doctor'), ('tNurse', 'Nurse')], default='tDoctor')

@app.route('/stafflogin', methods=['GET', 'POST'])
def stafflogin():
    form = StaffLogin(request.form)
    if request.method == 'POST' and form.validate():
        staffid = form.staffid.data
        password = form.password.data
        type = form.type.data

        ifUserExists = root.child('users').order_by_child('staffid').equal_to(staffid).get()
        # print(root.child('messages').order_by_child('staffid').equal_to(staffid).get())
        print(password)
        for k, v in ifUserExists.items():
            print(k, v)

            print(v['staffid'])
            print(v['password'])


            if staffid == v['staffid'] and  password == v['password'] and type == v['type']:
                session['logged_in'] = True
                session['staffid'] = staffid
                # session['password'] = password
                return redirect(url_for('home'))
            else:
                error = 'Invalid login'
                flash(error, 'danger')
                return render_template('StaffLog.html', form=form)
    else:
        return render_template('StaffLog.html', form=form)
    return render_template('StaffLog.html',form=form)

class Staffreg(Form):
    staffid = StringField('Staffid',validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    type = RadioField('Type', choices=[('tDoctor', 'Doctor'), ('tNurse', 'Nurse')], default='tDoctor')

@app.route('/staffreg', methods=['POST', 'GET'])
def register():
    form = Staffreg(request.form)
    if request.method == 'POST' and form.validate():
        #  def __init__(self, username, fullname, password, email):

        staffid = form.staffid.data

        password = form.password.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption
        type = form.type.data

        ifUserExists = root.child('users').order_by_child('staffid').equal_to(staffid).get()

        print(ifUserExists)

        for k, v in ifUserExists.items():
            print(k, v)

        if len(ifUserExists) > 0:
            flash('User exist.', 'danger')
        else:

            user = StaffU(staffid, password, type)
            user_db = root.child('users')


            user_db.push(
                {
                    'staffid': user.get_staffid(),
                    'password': user.get_password(),
                    'type': user.get_type()
                }
            )

            flash('Registraion Successfully.', 'success')
            return redirect(url_for('stafflogin'))

    else:
        return render_template('staffreg.html', form=form)


@app.route('/afterLog')
def afterLog():
    return render_template('afterLog.html')

class RegisterUserForm(Form):
    nric = StringField('Nric', validators=[validators.DataRequired()])
    fullname = StringField('Full Name', validators=[validators.DataRequired()])
    gender = RadioField('Gender', choices=[('tMale', 'Male'), ('tFemale', 'Female')], default='tMale')
    dob = StringField('Date Of Birth(dd/MM/YYYY)',validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    # email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    form = RegisterUserForm(request.form)
    if request.method == 'POST' and form.validate():
        #  def __init__(self, username, fullname, password, email):

        # username = form.username.data
        nric = form.nric.data
        fullname = form.fullname.data
        gender = form.gender.data
        password = form.password.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption
        # email = form.email.data
        dob = form.dob.data

        ifUserExists = root.child('patientacc').order_by_child('username').equal_to(nric).get()

        print(ifUserExists)

        for k, v in ifUserExists.items():
            print(k, v)

        if len(ifUserExists) > 0:
            flash('User exist.', 'danger')
        else:

            user = Users(nric, fullname, dob, gender, password)
            user_db = root.child('messages')


            user_db.push(
                {
                    'nric': user.get_nric(),
                    'fullname': user.get_fullname(),
                    'dob': user.get_dob(),
                    'gender': user.get_gender(),
                    'password': user.get_password(),


                }
            )

            flash('Registraion Successfully.', 'success')
            return redirect(url_for('login'))

    else:
        return render_template('Register.html', form=form)

class Request(Form):
    drinks=SelectField('Drinks',
                              choices=[('', 'Select'), ('Warm Water', 'Warm Water'),
                                       ('Cold Water', 'Cold Water'),
                                       ('Milo', 'Milo'), ('Green Tea', 'Green Tea')], default='')

    food=SelectField('Food',
                              choices=[('', 'Select'), ('Chicken Porridge', 'Chicken Porridge'),
                                       ('Vegetarian Rice', 'Vegetarian Rice'),
                                       ('Steamed Bun', 'Steamed Bun')], default='')

    assistance=SelectField('Assistance',
                              choices=[( '', 'Select'), ('Bathing Service', "Bathing Service"),
                                       ('Toilet Assistance', 'Toilet Assistance'),
                                       ('Outdoor Personal Assistant', 'Outdoor Personal Assistant')], default='')

    emergency=SelectField('Emergency',
                                    choices=[('','Select'),('PAIN', 'Im in great pain'), ('Urgent Leave Required', "Urgent reason to leave the hospital")], default='')


    other=StringField('Other', default='')



@app.route('/request_help', methods=['GET', 'POST'])
def requesthelppage():
    form = Request(request.form)

    if request.method == 'POST' and form.validate():

        status= 1
        NRIC = session['nric']
        DatePublished = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drinks = form.drinks.data
        food = form.food.data
        assistance = form.assistance.data
        other = form.other.data
        emergency= form.emergency.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption

        # ifUserExists = root.child('request').order_by_child('NRIC').equal_to(NRIC).get()
        #
        # print(ifUserExists)
        #
        # # for k, v in ifUserExists.items():
        # #     print(ifUserExists.items())
        # #     print(k, v)
        # #     print(session['nric'])

        user = CreateRequest(drinks, food, assistance, other, DatePublished, NRIC, status, emergency)
        user_db = root.child('request/')

        user_db.push(
            {
                'emergency': user.get_emergency(),
                'status': user.get_status(),
                'NRIC': user.get_NRIC(),
                'DatePublished': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'drinks': user.get_drinks(),
                'food': user.get_food(),
                'assistance': user.get_assistance(),
                'other': user.get_other(),
            }
        )

        flash('Request Sent.', 'success')
        return redirect(url_for('home'))

    else:
        return render_template('Request_help.html', form=form)

    return render_template('Request_help.html', form=form)


@app.route('/request_help/<string:id>', methods=['GET', 'POST'])
def updaterequestpage(id):
    form = Request(request.form)

    if request.method == 'POST' and form.validate():

        status= 1
        NRIC = session['nric']
        DatePublished = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drinks = form.drinks.data
        food = form.food.data
        assistance = form.assistance.data
        other = form.other.data
        emergency= form.emergency.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption

        # ifUserExists = root.child('request').order_by_child('NRIC').equal_to(NRIC).get()
        #
        # print(ifUserExists)
        #
        # # for k, v in ifUserExists.items():
        # #     print(ifUserExists.items())
        # #     print(k, v)
        # #     print(session['nric'])

        user = CreateRequest(drinks, food, assistance, other, DatePublished, NRIC, status, emergency)
        user_db = root.child('request/'+ id)

        user_db.set(
            {
                'emergency': user.get_emergency(),
                'status': user.get_status(),
                'NRIC': user.get_NRIC(),
                'DatePublished': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'drinks': user.get_drinks(),
                'food': user.get_food(),
                'assistance': user.get_assistance(),
                'other': user.get_other(),
            }
        )

        flash('Request Sent.', 'success')
        return render_template('Request_help.html', form=form)
    return redirect(url_for('home'))





@app.route('/')
def default():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


# @app.route('/viewpublications')
# def viewpublications():
#     publications = root.child('publications').get()
#     list = [] #create a list to store all the publication objects
#     print(publications)
#     for pubid in publications:
#
#         eachpublication = publications[pubid]
#
#         if eachpublication['type'] == 'smag':
#             magazine = Magazine(eachpublication['title'], eachpublication['publisher'], eachpublication['status'], eachpublication['created_by'], eachpublication['category'], eachpublication['type'], eachpublication['frequency'])
#             magazine.set_pubid(pubid)
#             print(magazine.get_pubid())
#             list.append(magazine)
#         else:
#             book = Book(eachpublication['title'], eachpublication['publisher'], eachpublication['status'], eachpublication['created_by'], eachpublication['category'], eachpublication['type'], eachpublication['synopsis'], eachpublication['author'], eachpublication['isbn'])
#             book.set_pubid(pubid)
#             list.append(book)
#
#     return render_template('view_all_publications.html', publications = list)

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)


@app.route('/viewrequest/<string:id>', methods=['POST'])
def viewrequestform(id):
    user_db = root.child('request/'+ id)
    user_db.delete()
    flash('Request Deleted', 'success')

    return redirect(url_for('listofrequest'))

@app.route('/current_request/<string:id>', methods=['POST'])
def deleterequestform(id):
    user_db = root.child('request/'+ id)
    user_db.delete()
    flash('Request Deleted', 'success')

    return redirect(url_for('specificrequest'))

@app.route("/current_request")
def specificrequest():
    listofcurrent = root.child('request').get()
    list = []
    if listofcurrent == None:
        flash('no current requests made by this user', 'success')
        return render_template('home.html')
    else:
        for pubid in listofcurrent:
            eachupdate = listofcurrent[pubid]
            if eachupdate["NRIC"]== session['nric']:
                currentrequest = CreateRequest(eachupdate['drinks'], eachupdate['food'], eachupdate['assistance'],
                                             eachupdate['other'], eachupdate['DatePublished'], eachupdate['NRIC'],
                                             eachupdate['status'], eachupdate['emergency'])
                currentrequest.set_pubid(pubid)
                print(currentrequest.get_pubid())
                list.append(currentrequest)
                print(list)
            else:
                pass
    return render_template('currentrequest.html', listofcurrent=list)

@app.route('/viewrequest')
def listofrequest():
    listofrequest = root.child('request').get()
    list = []
    if listofrequest== None:
        flash('There are no requests for now', 'success')
        return render_template('viewrequestempty.html')
    else:
        for pubid in listofrequest:
            eachupdate = listofrequest[pubid]
            storerequest = CreateRequest( eachupdate['drinks'], eachupdate['food'], eachupdate['assistance'], eachupdate['other'], eachupdate['DatePublished'], eachupdate['NRIC'], eachupdate['status'], eachupdate['emergency'])
            storerequest.set_pubid(pubid)
            print(storerequest.get_pubid())
            list.append(storerequest)
            print(list)
        return render_template('viewrequest.html', listofrequest=list)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        nric = form.nric.data
        password = form.password.data

        ifUserExists = root.child('messages').order_by_child('nric').equal_to(nric).get()

        for k, v in ifUserExists.items():
            print(k, v)
            # print(sha256_crypt.encrypt(password))
            print(v['nric'])
            print(v['password'])

            # if username == v['username'] and sha256_crypt.verify(password, v['password']):
            if nric == v['nric'] and  password == v['password']:
                session['logged_in'] = True
                session['nric'] = nric
                print(nric)
                # session['password'] = password
                return redirect(url_for('afterLog'))
            else:
                error = 'Invalid login'
                flash(error, 'danger')
                return render_template('Login.html', form=form)
    else:
        return render_template('Login.html', form=form)
    return render_template('Login.html',form=form)



@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

class LoginForm(Form):
    nric = StringField('Nric', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])



@app.route("/request_help/<string:id>", methods=['GET', 'POST'])
def update_request(id):
    form = Request(request.form)
    if request.method == "POST" and form.validate():
        status = 1
        NRIC = session['nric']
        DatePublished = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drinks = form.drinks.data
        food = form.food.data
        assistance = form.assistance.data
        other = form.other.data
        emergency = form.emergency.data

        updaterq = CreateRequest(drinks, food, assistance, other, DatePublished, NRIC, status, emergency)
        if request.method == "POST":
            updaterq_db= root.child("request/" + id)
            updaterq_db.set({
                "NRIC":session["nric"],
                "status":updaterq.get_status(),
                "DatePublished":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "assistance":updaterq.get_assistance(),
                "drinks":updaterq.get_drinks(),
                "food":updaterq.get_food(),
                "emergency":updaterq.get_emergency(),
                "other":updaterq.get_other(),
                })
            flash('Request update.', 'success')
            return redirect(url_for('updaterequestpage'))

        return render_template('home.html')

@app.route("/viewrequest/<string:id>", methods=['GET', 'POST'])
def update_status(id):
    form = Request(request.form)
    if request.method == "POST" and form.validate():
        status = 2
        updaterq = CreateRequest(status)
        if request.method == "POST":
            updaterq_db= root.child("request/" + id)
            updaterq_db.set({
                "status":updaterq.get_status(),
                })
            flash('Request update.', 'success')
            return redirect(url_for('listofrequest'))

        return render_template('home.html')

# @app.route('/viewrequest/<string:id>/', methods=['GET', 'POST'])
# def update_request(id):
#     if request.method == "POST":
#         if request.form["taken"] == "Interested?":
#             status = "Taken"
#             ride = root.child("listofridesp/" + id)
#             ride.set({
#                 "Starting position": from_where,
#                 "Destination": to_where,
#                 "date": date,
#                 "sessionemail": "sessionemail",
#                 "time": time,
#                 "usertype": userid,
#                 "schedule": schedule,
#                 "status": "Taken"})
#             return redirect(url_for("listofridesD"))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
