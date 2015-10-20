__author__ = 'yanwei'
import hashlib
import sqlite3
import datetime
import sys
import os

def md5(instr):
    a = hashlib.md5()
    a.update(instr)
    return a.hexdigest()

class mydb(object):
    def __init__(self):
        db = sqlite3.connect( os.path.join(sys.path[0],'vote.db') )
        self.db = db

    def __del__(self):
        self.db.close()

    def checkuserexists(self, userid):
        cs = self.db.cursor()
        cs.execute("select id from users where id='%s'" % userid)
        if len(cs.fetchall()) > 0:
            return True
        else:
            return False

    def adduser(self, userid, password, chinese):
        if self.checkuserexists(userid):
            err = "user %s already exists!" % userid
            print err
            return False
        else:
            cs = self.db.cursor()
            cs.execute("insert into users values('%s', '%s', '%s')" %(userid, md5(password), chinese))
            self.db.commit()
            return True

    def getChinese(self, userid):
        cs = self.db.cursor()
        cs.execute("select chinese from users where id='%s'" % userid)
        result = cs.fetchall()
        if len(result) > 0:
            return result[0][0]
        return ''

    def changepassword(self, userid, newpassword):
        if not self.checkuserexists(userid):
            err = "user %s doesn't exist!" % userid
            print err
            return False
        else:
            cs = self.db.cursor()
            cs.execute("update users set password='%s' where id='%s'" %(md5(newpassword), userid))
            self.db.commit()
            return True

    def checkpassword(self, userid, password):
        if not self.checkuserexists(userid):
            err = "user %s doesn't exist!" % userid
            print err
            return False
        else:
            cs = self.db.cursor()
            cs.execute("select password from users where id = '%s'" % userid)
            result = cs.fetchone()[0]
            if result == md5(password):
                return True
            else:
                return False

    def listusers(self):
        cs = self.db.cursor()
        cs.execute("select id, chinese, password from users")
        for i in cs.fetchall():
            print '\t'.join(i)

    def getAllVotesToday(self):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        cs = self.db.cursor()
        cs.execute("select id, restaurant from votes where date='%s'" % today)
        return cs.fetchall()

    def getMyVote(self, userid):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        cs = self.db.cursor()
        cs.execute("select restaurant from votes where id='%s' and date='%s'" % (userid, today))
        result = cs.fetchall()
        if len(result) > 0:
            return result[0][0]
        else:
            return ''

    def getRestaurants(self):
        cs = self.db.cursor()
        cs.execute("select * from restaurants")
        result = cs.fetchall()
        return [x[0] for x in result]

    def vote(self, userid, restaurant):
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        cs = self.db.cursor()
        if self.getMyVote(userid) != '':
            cs.execute("update votes set restaurant='%s' where id='%s' and date='%s'" % (restaurant, userid, today))
        else:
            cs.execute("insert into votes values('%s', '%s', '%s')" % (userid, today, restaurant))
        self.db.commit()




