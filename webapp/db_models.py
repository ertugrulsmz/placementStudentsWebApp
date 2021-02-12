from webapp import db,login_manager
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin


#login manager is obj in init.py works as loginmanager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.Boolean,nullable=False,default=True) #default student and True.
    complete = db.Column(db.Boolean,nullable=False,default=False)
    student_details = db.relationship( 'Studentdetail', uselist = False, backref='user')
    company_details = db.relationship('Companydetail', uselist = False, backref='user')
    responses = db.relationship( 'Response', backref='user')

    def __repr__(self):
        type = 'student' if self.type == True else 'company'
        return f"User('{self.username}', '{self.email}', '{type}')"


#Many to Many
advertisement_studentdetail = db.Table('advertisement_studentdetail',
    db.Column('advertisement_id', db.Integer, db.ForeignKey('advertisement.id'), primary_key=True),
    db.Column('studentdetail_id', db.Integer, db.ForeignKey('studentdetail.id'), primary_key=True)
)

studentdetail_keyword  = db.Table('studentdetail_keyword',
    db.Column('studentdetail_id', db.Integer, db.ForeignKey('studentdetail.id'), primary_key=True),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True)
)

class Studentdetail(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    name_surname = db.Column(db.String(150), nullable=False)
    description = db.Column( db.String( 800 ))
    university = db.Column(db.String(120), nullable=False)
    class_level = db.Column(db.Integer, nullable=False)
    gpa = db.Column(db.Float,nullable=False)
    active = db.Column(db.Boolean,nullable=False,default=True)
    github = db.Column( db.String( 180 ) )
    linkedin = db.Column( db.String( 180 ) )
    img = db.Column( db.Text, nullable=True )
    imgname = db.Column( db.Text, nullable=True )
    mimetype = db.Column( db.Text, nullable=True )
    advertisements = db.relationship( 'Advertisement', secondary=advertisement_studentdetail, lazy='subquery',
                            backref=db.backref('studentdetails', lazy=True ))
    keywords = db.relationship( 'Keyword', secondary=studentdetail_keyword, lazy='subquery',
                                      backref=db.backref( 'studentdetails', lazy=True ) )



    def __repr__(self):
        return f"Studentdetail('{self.id}', '{self.name_surname}', '{self.university}')"


advertisement_keyword = db.Table('advertisement_keyword',
    db.Column('advertisement_id', db.Integer, db.ForeignKey('advertisement.id'), primary_key=True),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True)
)

advertisement_users = db.Table('advertisement_users',
    db.Column('advertisement_id', db.Integer, db.ForeignKey('advertisement.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)



class Advertisement(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    companydetail_id = db.Column( db.Integer, db.ForeignKey( 'companydetail.id' ),
                           nullable=False )
    date_posted = db.Column( db.Date, nullable=False, default=date.today())
    deadline = db.Column( db.Date, nullable=False, default=date.today() + relativedelta(months=+1))
    title  = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(800),nullable=False)
    keywords = db.relationship( 'Keyword', secondary=advertisement_keyword, lazy='subquery',
                                      backref=db.backref( 'advertisements', lazy=True ) )

    users = db.relationship( 'User', secondary=advertisement_users, lazy='subquery',
                                      backref=db.backref( 'advertisements', lazy=True ) )

    responses = db.relationship( 'Response', backref='advertisement')



    def __repr__(self): #alihan
        return f"Advertisement('{self.id}', '{self.title}')"


class Keyword(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f"Keyword('{self.id}', '{self.name}')"


companydetail_keyword  = db.Table('companydetail_keyword',
    db.Column('companydetail_id', db.Integer, db.ForeignKey('companydetail.id'), primary_key=True),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keyword.id'), primary_key=True)
)

companydetail_interestarea  = db.Table('companydetail_interestarea',
    db.Column('companydetail_id', db.Integer, db.ForeignKey('companydetail.id'), primary_key=True),
    db.Column('interestarea_id', db.Integer, db.ForeignKey('interestarea.id'), primary_key=True)
)


class Companydetail(db.Model):
    id = db.Column( db.Integer, primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    name = db.Column( db.String( 150 ), nullable=False )
    description = db.Column( db.String( 800 ), nullable=False )
    address = db.Column( db.String( 800 ), nullable=False )
    website = db.Column( db.String( 180 ) )
    github = db.Column( db.String( 180 ) )
    linkedin = db.Column( db.String( 180 ) )
    numberofworkers = db.Column(db.Integer)
    advertisements = db.relationship('Advertisement', backref='company_detail', lazy=True)
    img = db.Column( db.Text, nullable=True )
    imgname = db.Column( db.Text, nullable=True)
    mimetype = db.Column( db.Text, nullable=True )
    keywords = db.relationship( 'Keyword', secondary=companydetail_keyword, lazy='subquery',
                                backref=db.backref( 'companydetails', lazy=True ) )

    interests = db.relationship( 'Interestarea', secondary=companydetail_interestarea, lazy='subquery',
                                backref=db.backref( 'companydetails', lazy=True ) )




    def __repr__(self):
        return f"Companydetail('{self.id}', '{self.name}')"



class Interestarea(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f"Keyword('{self.id}', '{self.name}')"



class Response(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisement.id'))

    answer = db.Column( db.Integer,default=None)

    def __repr__(self):
        return f"Response('{self.id}', '{self.user_id}', '{self.advertisement_id}','{self.answer}')"





"""class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('pages', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)"""