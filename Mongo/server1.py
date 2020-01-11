from flask import Flask,render_template, g, current_app
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import request, make_response
# from flask.ext.paginate import Pagination

import json
import math

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/joboid"
mongo = PyMongo(app)

# PAGINATION
def pagination(page):
    job_count = mongo.db.jobs.find().count()
    jobs = mongo.db.jobs.find()
    items = []
    for item in jobs:
        items.append({'job_title':item['job_title'],'company_name':item['company_name'], 'description' : item['description'], 'payscale' : item['payscale'], 'location' : item['location'], 'type' : item['type'] , 'comapny_type' : item['comapny_type'], 'date_posted' : item['date_posted'], 'parent_source' : item['parent_source'], 'active' : item['active']})
    total_pages = job_count
    total_jobs = job_count
    return {
    "total_pages": math.ceil(total_pages/20),
    "total_jobs": total_jobs,
    "page": page,
    "data": items[(page*20)-20: page*20],
    "per_page": 20
    } 

@app.route('/readjobs')
def readjobs():
    page = request.args.get("page", default = 1, type = int)
    return pagination(page)

# SAVED JOBS
@app.route('/savedjobs/jobid', methods = ['POST'])
def savedJobs():
    auth_header = request.headers.get('Authorization')
    token_encoded = auth_header.split(' ')[1]
    decoded_data = jwt.decode(token_encoded, 'naga', algorithm='HS256')

    mongo.db.saved.insert({'email' : decoded_data['email'], 'jobid' : jobid})
    return {'status' : 200}

# EMAIL ALERTS
@app.route('/emailalerts', methods = ['POST'])
def emailAlerts():
    auth_header = request.headers.get('Authorization')
    token_encoded = auth_header.split(' ')[1]
    decoded_data = jwt.decode(token_encoded, 'naga', algorithm='HS256')

    mongo.db.alert.insert({'email' : decoded_data['email'], 'searchquery' : sada, 'Filterapplied' : filter})
    return {'status' : 200}

# !&!&!&!&!&!&!&!&!&!&!&!&!&---ADDING AND REMOVING FILTERS---!&!&!&!&!&!&!&!&!&!&!&!&!&
# COMPANY TYPE FILTER
@app.route('/filtercompany/<companytype>')
def filterCompanytype(companytype):
    finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e177bf59c643c6d1ef77463")})
    arr = finding['company_type']
    if companytype not in arr:
        mongo.db.jobs.update({'_id' : ObjectId("5e177bf59c643c6d1ef77463")}, {'$push' : {'company_type' : companytype}})
        finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e177bf59c643c6d1ef77463")})
        arr = finding['company_type']
    else:
        mongo.db.jobs.update({'_id' : ObjectId("5e177bf59c643c6d1ef77463")}, {'$pull' : {'company_type' : companytype}})
        arr.remove(companytype)
    apply_filter = mongo.db.jobs.find({'comapny_type' : {'$in' : arr}})
    return dumps({'data' : apply_filter})

# JOB TITLE FILTER
@app.route('/filterjobtitle/<jobtitle>')
def filterJobtitle(jobtitle):
    finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e177dd79c643c6d1ef77464")})
    arr = finding['job_title']
    if jobtitle not in arr:
        mongo.db.jobs.update({'_id' : ObjectId("5e177dd79c643c6d1ef77464")}, {'$push' : {'job_title' : jobtitle}})
        finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e177dd79c643c6d1ef77464")})
        arr = finding['job_title']
    else:
        mongo.db.jobs.update({'_id' : ObjectId("5e177dd79c643c6d1ef77464")}, {'$pull' : {'job_title' : jobtitle}})
        arr.remove(jobtitle)
    apply_filter = mongo.db.jobs.find({'job_title' : {'$in' : arr}})
    return dumps({'data' : apply_filter})

# COMPANY NAME FILTER
@app.route('/filtercompanyname/<companyname>')
def filterCompanyname(companyname):
    finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e177de29c643c6d1ef77465")})
    arr = finding['company_name']
    if companyname not in arr:
        mongo.db.jobs.update({'_id' : ObjectId("5e177de29c643c6d1ef77465")}, {'$push' : {'company_name' : companyname}})
        finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e177de29c643c6d1ef77465")})
        arr = finding['company_name']
    else:
        mongo.db.jobs.update({'_id' : ObjectId("5e177de29c643c6d1ef77465")}, {'$pull' : {'company_name' : companyname}})
        arr.remove(companyname)
    apply_filter = mongo.db.jobs.find({'company_name' : {'$in' : arr}})
    return dumps({'data' : apply_filter})

# LOCATION FILTER
@app.route('/filterlocation/<location>')
def filterLocation(location):
    finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e1780e19c643c6d1ef77469")})
    arr = finding['location']
    if location not in arr:
        mongo.db.jobs.update({'_id' : ObjectId("5e1780e19c643c6d1ef77469")}, {'$push' : {'location' : location}})
        finding = mongo.db.jobs.find_one({'_id' : ObjectId("5e1780e19c643c6d1ef77469")})
        arr = finding['location']
    else:
        mongo.db.jobs.update({'_id' : ObjectId("5e1780e19c643c6d1ef77469")}, {'$pull' : {'location' : location}})
        arr.remove(location)
    apply_filter = mongo.db.jobs.find({'location' : {'$in' : arr}})
    return dumps({'data' : apply_filter})

# TYPE FILTER
@app.route('/typefilter/<typefilter>')
def typeFilter(typefilter):
    finding = mongo.db.jobs.find_one({'_id' :ObjectId("5e177df49c643c6d1ef77467")})
    arr = finding['type']
    if typefilter not in arr:
        mongo.db.jobs.update({'_id' : ObjectId("5e177df49c643c6d1ef77467")}, {'$push' : {'type' : typefilter}})
        finding = mongo.db.jobs.find_one({'_id' :ObjectId("5e177df49c643c6d1ef77467")})
        arr = finding['type']
    else:
        mongo.db.jobs.update({'_id' : ObjectId("5e177df49c643c6d1ef77467")}, {'$pull' : {'type' : typefilter}})
        arr.remove(typefilter)
    apply_filter = mongo.db.jobs.find({'type' : {'$in' : arr}})
    return dumps({'data' : apply_filter})

# PARENT SOURCE FILTER
@app.route('/parentsource/<parentsource>')
def parentsource(parentsource):
    finding = mongo.db.jobs.find_one({'_id' :ObjectId("5e177dfd9c643c6d1ef77468")})
    arr = finding['parent_source']
    if parentsource not in arr:
        mongo.db.jobs.update({'_id' : ObjectId("5e177dfd9c643c6d1ef77468")}, {'$push' : {'parent_source' : parentsource}})
        finding = mongo.db.jobs.find_one({'_id' :ObjectId("5e177dfd9c643c6d1ef77468")})
        arr = finding['parent_source']
    else:
        mongo.db.jobs.update({'_id' : ObjectId("5e177dfd9c643c6d1ef77468")}, {'$pull' : {'parent_source' : parentsource}})
        arr.remove(parentsource)
    apply_filter = mongo.db.jobs.find({'parent_source' : {'$in' : arr}})
    return dumps({'data' : apply_filter})

# !&!&!&!&!&!&!&!&!&!&!&!&!&---ADDING AND REMOVING FILTERS---!&!&!&!&!&!&!&!&!&!&!&!&!&