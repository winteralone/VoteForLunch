__author__ = 'yanwei'
from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect
from flask import url_for
import json


import sys
app = Flask(__name__)

@app.route('/')
def index(yourname=None):
    if request.cookies.has_key('user'):
        return redirect('/vote')

    fp = sys.path[0] + '/login.html'
    html = open(fp).read()
    return html

@app.route('/vote')
def vote():
    if request.cookies.has_key('user'):
        return render_template('vote.html', name=request.cookies['user'], restaurants=['food1','food2','food3'])
    else:
        return redirect('/')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method  == 'POST':
        args = request.form
        cookies = request.cookies
        retstring = redirect('/vote')
        resp = make_response(retstring)
        resp.set_cookie('user', args['userid'], 3600)
        return resp
    return 'Unsupported request type GET'

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user')
    return resp


if __name__ == '__main__':
    app.run(debug=True)