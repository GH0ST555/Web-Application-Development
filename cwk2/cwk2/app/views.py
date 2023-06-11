#import relevent modules
from flask import render_template, flash,redirect,request, make_response
from app import app , models,db,login_manager,mail
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from .forms import Loginform,Signupform, Newpwdform
from .models import User, Product
from datetime import datetime ,date
import json
from flask_login import LoginManager,login_required,logout_user,login_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import logging




@login_manager.user_loader
def load_user(id):
    iid = int(id)
    return User.query.get(id)

#route for user login
@app.route('/login', methods=['GET','POST'])
def login():
    #checks if user has previously logged in to the site
    if current_user.is_authenticated:
        #redirect user to the landing page
        return redirect('/landing_page')
    #else initialize the loginform
    form = Loginform()
    #store username entered in form field
    usr = form.uname.data
    #validations on form submission
    if form.validate_on_submit():
        #retrieve the user info from database
        user = User.query.filter_by(user=usr).first()
        #if the username does not exist or the password does not match
        if user is None or not user.check_password(form.pwd.data):
            #provide error
            flash('Invalid Login')
            app.logger.warning('Invalid Login')
            #reload page
            return redirect('/login')
        #else authentication was successful
        #user is logged in and led to landing page

        app.logger.info('Login Success')
        login_user(user,remember = form.remember.data)
        return redirect('/landing_page')
    return render_template('login_page.html',
                        title='Login',form = form)


    


@app.route('/update_pwd', methods=['GET','POST'])
@login_required
def newpwds():
    form = Newpwdform()
    user = User.query.filter_by(user=current_user.user).first()
    if form.validate_on_submit():
        #retrieve the user info from database
        #if the username does not exist or the password does not match
        if user is None or not user.check_password(form.curpwd.data):
            #provide error
            flash('Wrong Current Password')
            app.logger.warning('Invalid Account Access')
            #reload page
            return redirect('/update_pwd')
        #store new password
        newpassword = form.paswrd.data
        #hash it
        user.password = generate_password_hash(newpassword)
        #save changes
        db.session.commit()
        app.logger.info('Password Changed Successfully')
        #send the email to user
        msg = Message('RE:Password Changed', sender =   'arjun.krishnan0033@gmail.com', recipients = [current_user.email])
        msg.html = "Dear User, Your Password Has been reset. <br>IF this was not done by you, please contact customer service IMMEDIATELY<br> <br> Regards,<br>Shoptoro"
        mail.send(msg)
        #login
        login_user(user)
        return redirect('/landing_page')
    return render_template('change_password.html',
                    title='Change Password',form = form)

#route for users to create accounts
@app.route('/create_account', methods=['GET','POST'])
def signup():
    #this is the signup form
    form = Signupform()
    #retrieve user details
    usr = form.uname.data
    email = form.email.data
    paswrd = form.pwd.data
    #validations to be performed on submitting user details
    if form.validate_on_submit():
        #tries to retreive existing username and email
        usern = User.query.filter_by(user=usr).first()
        emailn = User.query.filter_by(email=email).first()
        #if the username already exists
        if usern is not None:
            #print error message and reload page
            flash('User already exists')
            app.logger.warning('Invalid Account Creation')
            return redirect('/create_account')
        #if the email already exists
        if emailn is not None:
            #print error message and reload page
            app.logger.warning('Invalid Account Creation')
            flash('email ID already exists')
            return redirect('/create_account')
        #the username and email are both valid and hence user account is generated
        #add user info to the database and save changes to database
        add_user = User(user =usr,email =email,password = generate_password_hash(form.pwd.data))
        db.session.add(add_user)
        msg = Message('RE:Account created', sender =   'arjun.krishnan0033@gmail.com', recipients = [email])
        msg.html = "Thank you for creating a SHOPTORO account.<br> We hope you have a pleasant shopping experience<br><br>Regards,<br>SHOPTORO Team"
        mail.send(msg)
        #directly logs the user in to landing page
        #saves info to db
        db.session.commit()
        app.logger.info('Account Created')
        login_user(add_user)
        return redirect('/landing_page')
    return render_template('signup.html',
                        title='Signup',form = form)
    
#route for landing page
# i want to create a form where users can log in
@app.route('/')
def Homepage():
    #redirects user to landing page
    return render_template('welcome.html',
                           title='Home')

@app.route('/landing_page')
@login_required
def Landpage():
    result = Product.query.all()   
    #redirects user to landing page
    return render_template('landing_page.html',
                           title='Welcome Shopper',data = result)

#route to see all the 
@app.route('/mc<id>')
@login_required
def Mystuff(id):
    user_items= User.query.filter_by(id = id).first()
    data = user_items.products
    #redirects user to landing page
    return render_template('myitems.html',
                           title='Welcome Shopper',data = data)




#logout route for user
@app.route('/logout')
def logout():
    #logs out the user (built in method)
    logout_user()
    #returns user to landing page
    res =make_response()
    app.logger.info('Logged Out')
    #this is because of the login_required condition specified
    res.set_cookie("landing_page", value="",expires = "0")
    return redirect('/')


# #app route to allow users to add item to cart
@app.route('/add_to_cart/<id>', methods=['POST'])
@login_required
def add_to_cart(id):
    #stores the id of the product
    Prod = Product.query.filter_by(pid = id).first()
    #retrieves id of user
    user = current_user

    #if the user has clicked on the button
    if request.method == 'POST':
        user.products.append(Prod)
        #commit
        db.session.commit()
        #redirects user back to shopping page
        #log info
    app.logger.info('Item Added To List')
    return redirect('/landing_page')



#app route to allow users to add item to cart
@app.route('/remove_from_cart/<id>', methods=['GET','POST'])
@login_required
def rem_from_cart(id):
    prod = Product.query.filter_by(pid = id).first()
    user = current_user
    #stores the id of the product
    user.products.remove(prod)
    db.session.commit()
    #retrieves id of user
    app.logger.info('Item Removed from List')
    return redirect('/landing_page')

#route for landing page
# i want to create a form where users can log in
@app.route('/blogs')
def blog():
    #redirects user to landing page
    return render_template('blogs.html',
                           title='Blogs')
