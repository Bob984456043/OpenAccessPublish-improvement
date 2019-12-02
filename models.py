from flask_login import UserMixin
from app import app, db, lm
import datetime
import re
import time
import base64

# for users (unavailable)
ROLE_USER = 0
ROLE_ADMIN = 1

CSsubject=[]
CSsubject.append('CS')
CSsubject.append('computer science')
CSsubject.append('Computer Science')
CSsubject.append('ComputerScience')
CSsubject.append('CompSci')


# User class is unavailable
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __repr__(self):
        return "user %s %s %s %s" % (self.id, self.username, self.email, self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        # TO DO:Change return value into a specific value after eamil active has been implemented
        return True

    def is_anonymous(self):
        return False


# @lm.user_loader
# def load_user(id):
#    return User.query.get(int(id))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    depth = db.Column(db.Integer, default=0)
    name = db.Column(db.String(50), unique=True)
    super_subject = db.Column(db.String(30))

    def __init__(self):
        self.children = []


class Email(db.Model):
    email = db.Column(db.String(40), primary_key=True)
    validated = db.Column(db.String(10))
    validate_time = db.Column(db.DateTime)
    password = db.Column(db.String(100))
    ban = db.Column(db.String(10))

    def is_exist(self):
        num = Email.query.filter_by(email=self.email).count()
        if num > 0:
            e = Email.query.filter_by(email=self.email).first()
            self.validated = e.validated
            self.validate_time = e.validate_time
            self.password = e.password
            return True
        return False

    def is_banned(self):
        if self.ban == 'yes':
            return True
        return False

    def is_validated(self):
        if self.is_banned():
            return False
        if self.validated == 'yes':
            return True
        return False

    def __init__(self, email=None, is_validate='no', password='', validate_time=None, ban='no'):
        self.email = email
        self.validated = "no"
        self.validate_time = validate_time
        self.password = password
        self.ban = ban

    def generate_password(self):
        pwd = str(int(datetime.datetime.now().strftime("%Y%m%d%H%M%S")) % 1000000007)
        e = str(self.email)
        pwd += re.sub('[@.]', '', e)
        self.password = pwd
        return str(pwd)


class Article(db.Model):
    def __str__(self):
        return "ID:%s title:%s" % (self.id, self.title)

    def __lt__(self, other):
        return self.point > other.point

    def getEmail(self):
        return re.sub("\\S{1,3}@\\S+", '**@**', self.email)

    def getB64Email(self):
        return base64.b64encode(self.email)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    highlight = db.Column(db.Text)
    subject = db.Column(db.String(50), db.ForeignKey('subject.name'))
    email = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    pdf = db.Column(db.String(100))
    voteup = db.Column(db.Integer, default=0)
    votedown = db.Column(db.Integer, default=0)
    is_hide = db.Column(db.String(10), default='no')
    point = 0
    visit = 0

    def getVisit(self):
        self.visit = int(IpRecord.query.filter_by(target_id=self.id, page="detail").group_by("ip").count())
        return self.visit

    def getPoint(self):
        now = time.time()
        t1 = self.date.timestamp()
        delta_time = now - t1
        vote = self.voteup * 1.0 / (self.votedown + 1.0)
        self.point = (self.visit / delta_time * 100) * 0.3 + vote * 0.7
        return self.point


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    target = db.Column(db.Integer, db.ForeignKey("article.id"))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)
    voteup = db.Column(db.Integer, default=0)
    votedown = db.Column(db.Integer, default=0)

    def getEmail(self):
        return re.sub("\\S{1,3}@\\S+", '**@***', self.email)


class Vote():
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    type = db.Column(db.String(50), default="up")


class VoteArticle(Vote, db.Model):
    target_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    pass


class VoteComment(Vote, db.Model):
    target_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    pass


class BadUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    ip = db.Column(db.String(20))


class BadWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))


class IpRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(50))
    page = db.Column(db.String(50))
    target_id = db.Column(db.Integer)


# Delete all rubbish data in database after a time
def delete_rubbish():
    pass


db.drop_all()

db.create_all()
