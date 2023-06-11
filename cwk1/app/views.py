#import relevent modules
from flask import render_template, flash,redirect,request
from app import app , models,db
from flask_sqlalchemy import SQLAlchemy
from .forms import AssesmentForm
from .models import assesments
from datetime import datetime ,date




#route for homepage
@app.route('/')
def Homepage():
    #query to get the details of all assesments
    data = models.assesments.query.all()
    return render_template('all_assesments.html',
                           title='All Assesments',
                           data=data)

#route for create assesment
@app.route('/create_assesment', methods=['GET', 'POST'])
def createform():
    #initialize the form
    form = AssesmentForm()

    #to submit the form data to the database when submit button is clicked
    if form.is_submitted():
       
        #saves title info
       titl=request.form['ttl']
        #saves module code
       modulcode=request.form['mc']
       #saves deadline 
       deadlne=request.form['dline'] 
        #converts date to proper format
       dtime = datetime.strptime(deadlne,'%d-%m-%Y').date()
        #saves description
       descrption = request.form['desc']
        #sets status to UNCOMPLETE by default
       sttus = 'UNCOMPLETE'
       # adds data to table
       rec = assesments(titl,modulcode,dtime,descrption,sttus)
       #add record
       db.session.add(rec)
       #commit
       db.session.commit()
       #redirects user to the homepage
       return redirect('/')

    
	
    return render_template('create_assesments.html',
                           title='Create Assesment',
                           form=form)

            
#app route to create update function for an incomplete assessment
@app.route('/incomplete_assessments/<id>', methods=['POST'])
def incomplete_to_complete(id):
    #stores the id of the row
    ids= int(id)
    
    #if the user has clicked on the button
    if request.method == 'POST':
        #get the specific recoed
        admin=assesments.query.filter_by(id=ids).first()
        #convert status to complete
        admin.status = 'COMPLETED'
        #save changes
        db.session.commit()
    #redirect to complete assessments page
    return redirect('/completed_assessments')
    


#route for incomplete assessments
#displays all incomplete assesments
@app.route('/incomplete_assessments' , methods=['GET', 'POST'])
def incomplete_loadstuff():
    #stores query where assessment status is incomplete
    result = assesments.query.filter_by(status='UNCOMPLETE')
    return render_template('uncomplete.html',
                    title='Incomplete Assesments',
                    data=result)


#route for complete assessments
#displays all complete assesments
@app.route('/completed_assessments')
def complete():
    #stores query where assessment status is complete
    result = assesments.query.filter_by(status='COMPLETED')
    return render_template('complete.html',
                           title='Complete Assesments',
                           data=result)
