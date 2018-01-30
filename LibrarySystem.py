from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField
from Magazine import Magazine
from Book import Book
from Users import Users
import firebase_admin
from firebase_admin import credentials, db
from StaffU import StaffU
from descbill import Descbill
# from passlib.hash import sha256_crypt #need to pip install passlib on the command prompt

cred = credentials.Certificate('cred/stop-78245-firebase-adminsdk-jqcbt-032e64dc12.json')
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

        ifUserExists = root.child('messages').order_by_child('username').equal_to(nric).get()

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


@app.route('/delete_publication/<string:id>', methods=['POST'])
def delete_publication(id):
    mag_db = root.child('publications/' + id)
    mag_db.delete()
    flash('Article Deleted', 'success')

    return redirect(url_for('viewpublications'))

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

# class PublicationForm(Form):
#     title = StringField('Title', [
#         validators.Length(min=1, max=150),
#         validators.DataRequired()])
#     pubtype = RadioField('Type Of Publication', choices=[('sbook', 'Book'), ('smag', 'Magazine')], default='sbook')
#     category = SelectField('Caterory', [validators.DataRequired()],
#                            choices=[('', 'Select'), ('FANTASY', 'Fantasy'), ('FASHION', 'Fashion'),
#                                     ('THRILLER', 'Thriller'), ('CRIME', 'Crime'), ('BUSINESS', 'Business')],
#                            default='')
#     publisher = StringField('Publisher', [
#         validators.Length(min=1, max=100),
#         validators.DataRequired()])
#     status = SelectField('Status', [validators.DataRequired()],
#                          choices=[('', 'Select'), ('P', 'Pending'), ('A', 'Available For Borrowing'),
#                                   ('R', 'Only For Reference')], default='')
#     isbn = StringField('ISBN No', [validators.Length(min=1, max=100), RequiredIf(pubtype='sbook')])
#     author = StringField('Author', [
#         validators.Length(min=1, max=100),
#         RequiredIf(pubtype='sbook')])
#     synopsis = TextAreaField('Synopsis', [
#         RequiredIf(pubtype='sbook')])
#     frequency = RadioField('Frequency', [RequiredIf(pubtype='smag')],
#                            choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')])

#
# @app.route('/newpublication', methods=['GET', 'POST'])
# def new():
#     form = PublicationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         if  form.pubtype.data == 'smag':
#             title = form.title.data
#             type = form.pubtype.data
#             category = form.category.data
#             status = form.status.data
#             frequency = form.frequency.data
#             publisher = form.publisher.data
#             created_by = "U0001" # hardcoded value
#
#             mag = Magazine(title, publisher, status, created_by, category, type, frequency)
#
#
#             #create the magazine object
#             mag_db = root.child('publications')
#             mag_db.push({
#                     'title': mag.get_title(),
#                     'type': mag.get_type(),
#                     'category': mag.get_category(),
#                     'status': mag.get_status(),
#                     'frequency': mag.get_frequency(),
#                     'publisher': mag.get_publisher(),
#                     'created_by': mag.get_created_by(),
#                     'create_date': mag.get_created_date()
#             })
#
#             flash('Magazine Inserted Sucessfully.', 'success')
#
#         elif form.pubtype.data == 'sbook':
#             title = form.title.data
#             type = form.pubtype.data
#             category = form.category.data
#             status = form.status.data
#             isbn = form.isbn.data
#             author = form.author.data
#             synopsis = form.synopsis.data
#             publisher = form.publisher.data
#             created_by = "U0001"  # hardcoded value
#
#             book = Book(title, publisher, status, created_by, category, type, synopsis, author, isbn)
#             mag_db = root.child('publications')
#             mag_db.push({
#                 'title': book.get_title(),
#                 'type': book.get_type(),
#                 'category': book.get_category(),
#                 'status': book.get_status(),
#                 'author': book.get_author(),
#                 'publisher': book.get_publisher(),
#                 'isbn': book.get_isbnno(),
#                 'synopsis': book.get_synopsis(),
#                 'created_by': book.get_created_by(),
#                 'create_date': book.get_created_date()
#             })
#
#             flash('Book Inserted Sucessfully.', 'success')
#
#         return redirect(url_for('viewpublications'))
#
#
#     return render_template('create_publication.html', form=form)

# @app.route('/update/<string:id>/', methods=['GET', 'POST'])
# def update_publication(id):
#     form = PublicationForm(request.form)
#
#     if request.method == 'POST' and form.validate():
#         if form.pubtype.data == 'smag':
#             title = form.title.data
#             type = form.pubtype.data
#             category = form.category.data
#             status = form.status.data
#             frequency = form.frequency.data
#             publisher = form.publisher.data
#             created_by = "U0001"  # hardcoded value
#
#             mag = Magazine(title, publisher, status, created_by, category, type, frequency)
#
#             # create the magazine object
#             mag_db = root.child('publications/' + id)
#             mag_db.set({
#                     'title': mag.get_title(),
#                     'type': mag.get_type(),
#                     'category': mag.get_category(),
#                     'status': mag.get_status(),
#                     'frequency': mag.get_frequency(),
#                     'publisher': mag.get_publisher(),
#                     'created_by': mag.get_created_by(),
#                     'create_date': mag.get_created_date()
#             })
#
#             flash('Magazine Updated Sucessfully.', 'success')
#
#         elif form.pubtype.data == 'sbook':
#             title = form.title.data
#             type = form.pubtype.data
#             category = form.category.data
#             status = form.status.data
#             isbn = form.isbn.data
#             author = form.author.data
#             synopsis = form.synopsis.data
#             publisher = form.publisher.data
#             created_by = "U0001"  # hardcoded value
#
#             book = Book(title, publisher, status, created_by, category, type, synopsis, author, isbn)
#             mag_db = root.child('publications/' + id)
#             mag_db.set({
#                 'title': book.get_title(),
#                 'type': book.get_type(),
#                 'category': book.get_category(),
#                 'status': book.get_status(),
#                 'author': book.get_author(),
#                 'publisher': book.get_publisher(),
#                 'isbn': book.get_isbnno(),
#                 'synopsis': book.get_synopsis(),
#                 'created_by': book.get_created_by(),
#                 'create_date': book.get_created_date()
#             })
#
#             flash('Book Updated Successfully.', 'success')
#
#         return redirect(url_for('viewpublications'))
#
#     else:
#         url = 'publications/' + id
#         eachpub = root.child(url).get()
#
#         if eachpub['type'] == 'smag':
#             magazine = Magazine(eachpub['title'], eachpub['publisher'], eachpub['status'],
#                                 eachpub['created_by'], eachpub['category'], eachpub['type'],
#                                 eachpub['frequency'])
#
#             magazine.set_pubid(id)
#             form.title.data = magazine.get_title()
#             form.pubtype.data = magazine.get_type()
#             form.category.data = magazine.get_category()
#             form.publisher.data =  magazine.get_publisher()
#             form.status.data =  magazine.get_status()
#             form.frequency.data = magazine.get_frequency()
#         elif eachpub['type'] == 'sbook':
#             book = Book(eachpub['title'], eachpub['publisher'], eachpub['status'],
#                         eachpub['created_by'], eachpub['category'], eachpub['type'],
#                         eachpub['synopsis'], eachpub['author'], eachpub['isbn'])
#             book.set_pubid(id)
#             form.title.data = book.get_title()
#             form.pubtype.data = book.get_type()
#             form.category.data = book.get_category()
#             form.publisher.data = book.get_publisher()
#             form.status.data = book.get_status()
#             form.synopsis.data = book.get_synopsis()
#             form.author.data = book.get_author()
#             form.isbn.data = book.get_isbnno()
#
#         return render_template('update_publication.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
