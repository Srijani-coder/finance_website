from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db=SQLAlchemy()
class Admin(UserMixin,db.Model):
 def get_id(self): return f"admin:{self.id}"
 id=db.Column(db.Integer,primary_key=True); username=db.Column(db.String(80),unique=True,nullable=True); email=db.Column(db.String(160),unique=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False)
class SiteSetting(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120),default='Nibeedita Marketing & Distribution Service Pvt. Ltd.'); tagline=db.Column(db.String(220),default='Finance, marketing and distribution solutions built on trust.'); hero_title=db.Column(db.String(220),default='Financial Distribution With Clarity & Confidence'); hero_text=db.Column(db.Text,default='Helping clients navigate financial products, distribution and service with a relationship-first approach.'); cover_image=db.Column(db.Text); phone=db.Column(db.String(60),default=''); email=db.Column(db.String(160),default=''); address=db.Column(db.Text,default=''); about=db.Column(db.Text,default='We combine disciplined service, transparent communication and practical financial distribution support.'); facebook=db.Column(db.Text,default=''); linkedin=db.Column(db.Text,default=''); twitter=db.Column(db.Text,default=''); profile_image=db.Column(db.Text,default=''); chatbot_intro=db.Column(db.Text,default='Our financial planning professional offers thoughtful, client-focused guidance. Please review their qualifications and contact them for verified certification details.'); chatbot_plan=db.Column(db.Text,default="Start early. Here is our financial expert's contact information."); certifications=db.Column(db.Text,default='Qualifications and certifications will be published after verification.'); instagram=db.Column(db.Text,default='')
class Post(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(220),nullable=False); slug=db.Column(db.String(240),unique=True,nullable=False); excerpt=db.Column(db.Text); body=db.Column(db.Text); image=db.Column(db.Text); seo_title=db.Column(db.String(220)); meta_description=db.Column(db.String(320)); published=db.Column(db.Boolean,default=True); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Gallery(db.Model):
 id=db.Column(db.Integer,primary_key=True); image=db.Column(db.Text,nullable=False); caption=db.Column(db.String(220)); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Service(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(160),nullable=False); description=db.Column(db.Text,nullable=False); icon=db.Column(db.String(20),default='◆')
class Testimonial(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(120)); quote=db.Column(db.Text); approved=db.Column(db.Boolean,default=True)

class Client(UserMixin,db.Model):
 def get_id(self): return f"client:{self.id}"
 id=db.Column(db.Integer,primary_key=True)
 name=db.Column(db.String(120),nullable=False)
 email=db.Column(db.String(160),unique=True,nullable=False,index=True)
 password_hash=db.Column(db.String(255),nullable=False)
 created_at=db.Column(db.DateTime,default=datetime.utcnow)
