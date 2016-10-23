from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Company, Job, User

#Connect to Database and create database session
engine = create_engine('sqlite:///jobboard.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# oauth imports
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError, Credentials
import httplib2
import json
from flask import make_response
import requests
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # prevent token forgery if state token sent is not valid
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code) #exchange auth code for credentials obj
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to make auth code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check that token is valid
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if there was an error in access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # verify that access token is valid for this app
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already logged in'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store token in session for later use
    login_session['credentials'] = credentials.to_json()
    print login_session['credentials']
    login_session['gplus_id'] = gplus_id

    #get user Information
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    print user_id
    if not user_id:
        print 'creating user'
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    flash('You are signed in')

    return 'Welcome !'


@app.route('/gdisconnect')
def gdisconnect():

    credentials_json = login_session.get('credentials')

    if login_session.get('credentials'):
        del login_session['credentials']
    if login_session.get('gplus_id'):
        del login_session['gplus_id']
    if login_session.get('username'):
        del login_session['username']
    if login_session.get('email'):
        del login_session['email']
    if login_session.get('picture'):
        del login_session['picture']
    if login_session.get('user_id'):
        del login_session['user_id']

    if credentials_json is None:
        flash('User was not signed in')
        return redirect(url_for('showCompanies'))
    else:
        credentials = Credentials.new_from_json(credentials_json)

    try:
        h = httplib2.Http()
        credentials.revoke(h)
    except:
        flash('User was not signed in')
        return redirect(url_for('showCompanies'))

    flash('You have successfully logged out.')
    return redirect(url_for('showCompanies'))

# create a new state token and return it
# used to prevent cross-site request forgery attacks
def state_token():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return state

@app.route('/login')
def showLogin():
    state = state_token()
    return render_template("login.html", STATE=state)

def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# # # JSON APIs to view company Information

# return all jobs from a company
@app.route('/company/<int:company_id>/jobs/JSON')
def companyMenuJSON(company_id):
    company = session.query(Company).filter_by(id = company_id).one()
    jobs = session.query(Job).filter_by(company_id = company_id).order_by(asc(Job.created)).all()
    return jsonify(jobs=[j.serialize for j in jobs])

# return specific job
@app.route('/company/<int:company_id>/jobs/<int:job_id>/JSON')
def jobJSON(company_id, job_id):
    job = session.query(Job).filter_by(id = job_id).one()
    return jsonify(job=job.serialize)

# return all companies
@app.route('/company/JSON')
@app.route('/companies/JSON')
def companiesJSON():
    companies = session.query(Company).all()
    return jsonify(companies=[c.serialize for c in companies])


#Show all companys
@app.route('/')
@app.route('/company/')
@app.route('/companies/')
def showCompanies():
    companies = session.query(Company).order_by(asc(Company.name))
    if 'username' not in login_session:
        return render_template('companies.html', companies=companies)
    else:
        return render_template('companies.html', companies=companies, session=login_session)

#Create a new company
@app.route('/company/new/', methods=['GET','POST'])
def newCompany():
    if 'username' not in login_session:
        flash('You must be logged in to create a new company.')
        return redirect('/login')
    if request.method == 'POST':
      newCompany = Company(name=request.form['name'], user_id=login_session['user_id'])
      session.add(newCompany)
      flash('New Company %s Successfully Created' % newCompany.name)
      session.commit()
      return redirect(url_for('showCompany', company_id=newCompany.id))
    else:
      return render_template('newCompany.html', session=login_session)

#Edit a company
@app.route('/company/<int:company_id>/edit/', methods = ['GET', 'POST'])
def editCompany(company_id):
    if 'username' not in login_session:
        flash('You must be logged in to create a new company.')
        return redirect('/login')
    editedCompany = session.query(Company).filter_by(id=company_id).one()
    if 'user_id' in login_session and login_session['user_id'] == editedCompany.user_id:
        if request.method == 'POST':
            if request.form['name']:
                editedCompany.name = request.form['name']
                flash('Company Successfully Edited %s' % editedCompany.name)
                return redirect(url_for('showCompany', company_id=editedCompany.id))
        else:
            return render_template('editCompany.html', company=editedCompany, session=login_session)
    else:
        return 'You must be creator of the company to edit it'


#Delete a company
@app.route('/company/<int:company_id>/delete/', methods = ['GET','POST'])
def deleteCompany(company_id):
    if 'username' not in login_session:
        return redirect('/login')
    company = session.query(Company).filter_by(id=company_id).one()
    if 'user_id' in login_session and login_session['user_id'] == company.user_id:
        if request.method == 'POST':
            session.delete(company)
            flash('%s Successfully Deleted' % company.name)
            session.commit()
            return redirect(url_for('showCompanies', company_id=company_id))
        else:
            return render_template('deleteCompany.html',company = company, session=login_session)
    else:
        return 'You must be owner of the company to delete it'

#Show a company menu
@app.route('/company/<int:company_id>/')
@app.route('/company/<int:company_id>/jobs/')
def showCompany(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    creator = getUserInfo(company.user_id)
    jobs = session.query(Job).filter_by(company_id=company_id).all()

    return render_template('company.html',
                                jobs=jobs,
                                company=company,
                                creator=creator,
                                session=login_session)




# Create a new job posting
@app.route('/company/<int:company_id>/jobs/new/',methods=['GET','POST'])
def newJob(company_id):
    if 'username' not in login_session:
        return redirect('/login')
    company = session.query(Company).filter_by(id=company_id).one()
    if 'user_id' in login_session and login_session['user_id'] == company.user_id:
        if request.method == 'POST':
            newJob = Job(
                title=request.form['title'],
                description=request.form['description'],
                company_id=company_id,
                user_id=login_session['user_id'])
            session.add(newJob)
            session.commit()
            flash('New Job %s Item Successfully Created' % (newJob.title))
            return redirect(url_for('showCompany', company_id=company_id, session=login_session))
        else:
            return render_template('newjob.html', company_id=company_id, session=login_session)
    else:
        return 'you must be owner of the company to add a job'

# Edit a job
@app.route('/company/<int:company_id>/jobs/<int:job_id>/edit', methods=['GET','POST'])
def editJob(company_id, job_id):
    if 'username' not in login_session:
        return redirect('/login')

    job = session.query(Job).filter_by(id = job_id).one()
    company = session.query(Company).filter_by(id = company_id).one()
    if 'user_id' in login_session and login_session['user_id'] == company.user_id:
        if request.method == 'POST':
            if request.form['title']:
                job.title = request.form['title']
            if request.form['description']:
                job.description = request.form['description']
            session.add(job)
            session.commit()
            flash('Job Successfully Edited')
            return redirect(url_for('showCompany', company_id = company_id))
        else:
            return render_template('editJob.html',
                                    company=company,
                                    job=job,
                                    session=login_session)
    else:
        return 'Only the owner may edit this item'


#Delete a job
@app.route('/company/<int:company_id>/jobs/<int:job_id>/delete', methods = ['GET','POST'])
def deleteJob(company_id,job_id):
    if 'username' not in login_session:
        return redirect('/login')
    company = session.query(Company).filter_by(id=company_id).one()
    job = session.query(Job).filter_by(id=job_id).one()
    if 'user_id' in login_session and login_session['user_id'] == company.user_id:
        if request.method == 'POST':
            session.delete(job)
            session.commit()
            flash('Job Successfully Deleted')
            return redirect(url_for('showCompany', company_id=company_id))
        else:
            return render_template('deleteJob.html', job=job, company=company, session=login_session)
    else:
        return 'Only the owner may delete this item'




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
