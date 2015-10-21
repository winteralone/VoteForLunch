#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect
import threading

import myutils
import time
import datetime

app = Flask(__name__)

user_voted_dict = {}


def vote(userid, restaurant):
    user_voted_dict[userid] = restaurant


def sync_vote():
    db = myutils.mydb()
    db.sync_vote(user_voted_dict)
    print "synchronized votes to db at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def thread_func():
    while True:
        time.sleep(300)
        sync_vote()


@app.route('/')
def index():
    if request.cookies.has_key('user'):
        return redirect('/vote')

    return render_template('login.html')

@app.route('/sync')
def sync():
    sync_vote()
    return 'sync completed'


@app.route('/vote', methods=['GET', 'POST'])
def votepage():
    if request.cookies.has_key('user'):

        db = myutils.mydb()
        userid = request.cookies['user'].lower()
        cname = db.getChinese(userid)

        candidate_restaurants = db.getRestaurants()

        voted_user_dict = {}
        for uid, rest in user_voted_dict.items():
            if voted_user_dict.has_key(rest):
                if uid not in voted_user_dict[rest]:
                    voted_user_dict[rest] += ',' + db.getChinese(uid)
            else:
                voted_user_dict[rest] = db.getChinese(uid)

        return render_template('vote.html', name=cname, restaurants=candidate_restaurants, votes=voted_user_dict)
    else:
        return redirect('/')


@app.route('/setvote', methods=['POST'])
def setvote():
    if request.cookies.has_key('user'):
        userid = request.cookies['user'].lower()
        if request.method == 'POST' and request.form['voted'] != '':
            vote(userid, request.form['voted'])
    return redirect('/vote')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    db = myutils.mydb()
    for uid, rest in db.getAllVotesToday():
        vote(uid, rest)
    sync_thread = threading.Thread(target=thread_func)
    sync_thread.start()
    app.run('0.0.0.0')
