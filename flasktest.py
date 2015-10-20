# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect
import datetime

import myutils


import sys
app = Flask(__name__)

@app.route('/')
def index():
    if request.cookies.has_key('user'):
        return redirect('/vote')

    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.cookies.has_key('user'):
        db = myutils.mydb()
        userid = request.cookies['user'].lower()
        cname = db.getChinese(userid)
        candidate_restaurants = db.getRestaurants()
        if request.method == 'POST' and request.form['voted'] != '':
            db.vote(userid, request.form['voted'])
        votes = db.getAllVotesToday()
        vote_dict = {}
        for uid, rest in votes:
            if vote_dict.has_key(rest):
                if uid not in vote_dict[rest]:
                    vote_dict[rest] += ','+db.getChinese(uid)
            else:
                vote_dict[rest] = db.getChinese(uid)

        return render_template('vote.html', name=cname, restaurants=candidate_restaurants, votes=vote_dict)
    else:
        return redirect('/')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method  == 'POST':
        args = request.form
        db = myutils.mydb()
        userid = args['userid'].lower()
        if not db.checkuserexists(userid):
            return render_template('login.html', errmsg='User does not exist')
        elif db.checkpassword(userid, args['password']):
            retstring = redirect('/vote')
            resp = make_response(retstring)
            resp.set_cookie('user', args['userid'], 3600)
            return resp
        else:
            return render_template('login.html', errmsg='Incorrect password')
    return 'Unsupported request type GET'

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user')
    return resp


if __name__ == '__main__':
    app.run(debug=True)