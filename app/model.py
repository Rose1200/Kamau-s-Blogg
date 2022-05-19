from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),unique=True,nullable=False)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password_hash=db.Column(db.String,nullable=False)
    blog_id=db.relationship('Blogs',backref='user')

    @property
    def password(self):
        raise AttributeError("You can't read the password")

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)    

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)  

    
    def __repr__(self): 
        return f'{self.username}: {self.email}'   

class Blogs(db.Model,UserMixin):
    __tablename__ = 'blogs'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    post=db.Column(db.Text())
    author = db.Column(db.String(255))
    comments=db.relationship('Comment',backref='comments',lazy='dynamic')
    upvote=db.relationship('Upvote',backref='blogs',lazy='dynamic')
    downvote=db.relationship('Downvote',backref='blogs',lazy='dynamic')
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    image_file=db.Column(db.String(255),nullable=False,default='default.jpg')
    # date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Blogs{self.post}'  

class Comment(db.Model):
    __tablename__ = 'comments'

    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.Text(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id=db.Column(db.Integer,db.ForeignKey('blogs.id'),nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod 
    def get_comments(cls,id):
        comments=Comment.query.filter_by(id=id).all()
        return comments   

    def __repr__(self):
        return f'Blog{self.comment}'       

class Upvote(db.Model):
    __tablename__='upvotes'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id=db.Column(db.Integer,db.ForeignKey('blogs.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        downvote=Upvote.query.filter_by(blog_id=id).all()
        return upvote    

    def __repr__(self):
        return f'{self.user_id}:{self.blog_id}' 
class Downvote(db.Model):
    __tablename__='downvotes'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id=db.Column(db.Integer,db.ForeignKey('blogs.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_downvotes(cls,id):
        downvote=Downvote.query.filter_by(blog_id=id).all()
        return downvote    

    def __repr__(self):
        return f'{self.user_id}:{self.blog_id}'  