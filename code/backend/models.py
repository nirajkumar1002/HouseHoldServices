from flask_sqlalchemy import SQLAlchemy
from flask_security import AsaList, RoleMixin, UserMixin, SQLAlchemyUserDatastore
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList


db = SQLAlchemy()

class RoleUser(db.Model):
    __tablename__ = 'role_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='role_user', backref=db.backref('users', lazy='dynamic'))
    service_category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=True)
    years_of_experience = db.Column(db.Integer, nullable=True)
    
    
class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    services = db.relationship('Service', backref='category', lazy='dynamic')
    users = db.relationship('User', backref='service_category', lazy='dynamic')


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('services', lazy='dynamic'))


class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    service_status = db.Column(db.String(255), nullable=False, default='requested')
    user = db.relationship('User', foreign_keys=[customer_id], backref=db.backref('service_requests', lazy='dynamic'))
    professional = db.relationship('User', foreign_keys=[professional_id], backref=db.backref('assigned_requests', lazy='dynamic'))
    service = db.relationship('Service', backref=db.backref('service_requests', lazy='dynamic'))


class ServiceReview(db.Model):
    __tablename__ = 'service_reviews'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(255), nullable=False)
    service_request = db.relationship('ServiceRequest', backref=db.backref('service_reviews', lazy='dynamic'))
    customer = db.relationship('User', backref=db.backref('service_reviews', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)