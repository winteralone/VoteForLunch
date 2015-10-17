__author__ = 'yanwei'
import hashlib
import sqlite3

def md5(instr):
    a = hashlib.md5()
    a.update(instr)
    return a.hexdigest()

class mydb(object):
    def __init__(self):
        db = sqlite3.connect('vote.db');
        self.db = db

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
        cs.execute("select userid, chinese, password from users")
        for i in cs.fetchall():
            print '\t'.join(i)



