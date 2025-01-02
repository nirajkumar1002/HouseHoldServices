import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from celery_job.tasks import export_categories_csv

from flask import Flask, request, jsonify, make_response
from models import db, User, Role, Service, ServiceRequest, ServiceCategory, ServiceReview
from flask_sqlalchemy import SQLAlchemy 
from flask_security import Security, auth_required, roles_accepted, SQLAlchemyUserDatastore

from flask_cors import CORS

import uuid
from datetime import datetime
from flask_security.utils import hash_password, verify_password



from celery import Celery
import csv



def create_app():
    initapp = Flask(__name__)
    from config import LocalDev
    initapp.config.from_object(LocalDev)
    db.init_app(initapp)
    
    from caching_instance import cache
    #cache init
    # cache = Cache() 
    # initapp.cache = cache
    cache.init_app(initapp)
    
    
    
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    initapp.security = Security(initapp, datastore=user_datastore, register_blueprint=False)
    
    
    initapp.app_context().push()
    
    
    from flask_restful import Api
    initApi = Api(initapp, prefix='/api')
    
    
    return initapp, initApi


app, api = create_app()
CORS(app)
    
user_datastore :SQLAlchemyUserDatastore = app.security.datastore
# cache = app.cache

from celery_job.celery_factory import make_celery
celery_app = make_celery(app)



#...........................................................
from caching_instance import cache

@app.get('/cache')
@cache.cached(timeout=5, key_prefix='cache')
def cache_test():
    return {'time': str(datetime.now())}


# @app.route('/celery', methods=['GET'])
# def celery():
#     task = add.delay(10,20)
#     return {'task_id': task.id}, 200
    
# @app.get('/get-celery-data/<id>')
# def getData(id):
#     result = add.AsyncResult(id)
#     return {'status': result.state, 'result': result.result}, 200


#export categories to csv
@app.get('/export')
def exportCategoriesCSV():
    task = export_categories_csv.delay()
    return {'task_id': task.id}, 200


from celery_job.tasks import export_closed_service_requests

@app.route('/export-data', methods=['GET'])
def export_closed_requests():
    task = export_closed_service_requests.delay()
    return jsonify({"message": "Export task triggered", "task_id": task.id}), 202

@app.route('/') 
def index():
    return 'Hello, World!'

#...........................................................
#for notifications(Email)


from celery_job.tasks import send_email
from celery.beat import crontab
from celery_job.tasks import send_email_daily

celery_app.conf.beat_schedule = {
    # 'send-email-every-minute': {
    #     'task': 'celery_job.tasks.send_email',
    #     'schedule': crontab(minute='*/1')
    # },
    
    'daily-reminder': {
        'task': 'celery_job.tasks.send_email_daily',
        # 'schedule': crontab(minute='*/1'), 
        'schedule': crontab(minute=0, hour=20), 
    },
    
    'monthly-report': {
        'task': 'celery_job.tasks.send_monthly_report',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'), 
        # 'schedule': crontab(minute='*/1'), 
    },
}










# celery_app.conf.beat_schedule = {
#     'schedule-1': {
#         'task': 'celery_tasks.reminder',
#         'schedule': crontab(minute='18', hour='21'),
#     },
#     'schedule-2': {
#         'task': 'celery_tasks.plus',
#         'schedule': crontab(minute='18', hour='21'),
#         # 'args': (1, 2)
#     },
    # 'schedule-3': {
    #     'task': 'celery_tasks.dbQuery',
    #     'schedule': 5,
    #     'agrs': (3, 4)
    # }
# }

#..............................ROUTES........................................................................................
#register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.form
    role_name = data.get('role')
    print(role_name)
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({'message': 'Role not found'}), 400

    new_user = user_datastore.create_user(
        username=data['username'],
        email=data['email'],
        active=False if role_name == 'service_provider' else True,
        password=hash_password(data['password']),
        fs_uniquifier=str(uuid.uuid4()),
        service_category_id=data.get('serviceCategory') if role_name == 'service_provider' else None,
        years_of_experience=data.get('yearsOfExperience') if role_name == 'service_provider' else None
    )
    user_datastore.add_role_to_user(new_user, role)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


#login
@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'data not found, supply json'}), 400)
    present_user = user_datastore.find_user(email=data['emailFromJson'])
    print(present_user)
    print(present_user.active)
    if present_user is None:
        return make_response(jsonify({'message': 'email id is not registered with us', "email": data['emailFromJson']}), 406)
    if present_user.active == True:
        if verify_password(data['passwordFromJson'], present_user.password):
            auth_token = present_user.get_auth_token()
            print( present_user)
            print(data)
            print(auth_token)
            
            user_role = present_user.roles[0].name if present_user.roles else 'customer'
            return make_response(jsonify({
                'message': 'login success',
                'email': data['emailFromJson'],
                'authToken': auth_token,
                'role': user_role,
                'user': {
                    'id': present_user.id,
                    'role': user_role
                }
            }), 200)
        return make_response(jsonify({'message': 'login failed, password mismatch', "email": data['emailFromJson']}), 406)
    return make_response(jsonify({'message': 'login failed, user is not active contact admin', "email": data['emailFromJson']}), 406)


#admin login
@app.route('/api/adminlogin', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'message': 'data not found, supply json'}), 400)
    
    admin_email = data.get('emailFromJson')
    admin_password = data.get('passwordFromJson')
    
    # if not user:
    #     return jsonify({
    #         'message':'User doesnot exist'
    #     }),401
        
    if data['emailFromJson'] and data['passwordFromJson']:
        user = user_datastore.find_user(email = admin_email )
        if verify_password(admin_password, user.password) :
            return jsonify({
                "id":user.id,
                "email":user.email,
                
                "token":user.get_auth_token(),
                
                "active" : user.active
            }),200

        return make_response(jsonify({'message': 'login success', 'role': 'admin'}), 200)
    else:
        return make_response(jsonify({'message': 'login failed, invalid credentials'}), 401)


#manage services
#create service
@app.route('/api/admin/create_service', methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def create_service():
    data = request.get_json()
    # print(data)
    new_service = Service(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category_id=data['category_id']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service created'}), 201


@app.route('/api/admin/create_category', methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def create_category():
    data = request.get_json()
    category_name = data.get('name')
    if not category_name:
        return jsonify({'error': 'Category name is required'}), 400

    new_category = ServiceCategory(name=category_name)
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully'}), 201



@app.route('/api/service_categories', methods=['GET'])
def get_service_categories():
    categories = ServiceCategory.query.all()
    categories_list = [{
        'id': category.id,
        'name': category.name,
        # 'description': category.description
    } for category in categories]
    return jsonify(categories_list), 200


# Update service
@app.route('/api/admin/update_service/<int:service_id>', methods=['PUT'])
@auth_required('token')
@roles_accepted('admin')
def update_service(service_id):
    data = request.get_json()
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    service.name = data['name']
    service.description = data['description']
    service.price = data['price']
    service.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Service updated'}), 200


#Delete service
@app.route('/api/admin/delete_service/<int:service_id>', methods=['DELETE'])
@auth_required('token')
@roles_accepted('admin')
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted'}), 200


#accept service request (service provider)
@app.route('/api/professional/accept_service_request/<int:request_id>', methods=['PUT'])
def accept_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404
    service_request.service_status = 'accepted'
    service_request.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Service request accepted'}), 200


#reject service request (service provider)
@app.route('/api/professional/reject_service_request/<int:request_id>', methods=['PUT'])
def reject_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404
    service_request.service_status = 'rejected'
    service_request.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Service request rejected'}), 200


#close service request (service provider)
@app.route('/api/professional/close_service_request/<int:request_id>', methods=['PUT'])
def professional_close_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404
    service_request.service_status = 'completed'
    service_request.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Service request completed'}), 200


@app.route('/api/professional/service_requests', methods=['GET'])
def get_professional_service_requests():
    professional_id = request.args.get('professional_id')
    if not professional_id:
        return jsonify({'message': 'Professional ID is required'}), 400
    
    service_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()
    requests_list = []
    for service_request in service_requests:
        if service_request.service:  # Check if the service is not None
            requests_list.append({
                'id': service_request.id,
                'service_id': service_request.service_id,
                'service_name': service_request.service.name,
                'service_description': service_request.service.description,
                'service_price': service_request.service.price,
                'customer_id': service_request.customer_id,
                'customer_name': service_request.user.username if service_request.user else 'Unknown',
                'service_status': service_request.service_status
            })
    return jsonify(requests_list), 200


@app.route('/api/professional/update_service_request/<int:request_id>', methods=['PUT'])
@auth_required('token')
@roles_accepted('service_provider')
def update_service_request_status(request_id):
    data = request.get_json()
    service_status = data.get('service_status')

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404

    service_request.service_status = service_status
    db.session.commit()
    return jsonify({'message': 'Service request updated'}), 200


@app.route('/api/professional/summary', methods=['GET'])
# @auth_required('token')
def get_professional_summary():
    professional_id = request.args.get('professional_id')
    
    if not professional_id:
        
        return jsonify({'message': 'Professional ID is required'}), 400

    pending_requests = ServiceRequest.query.filter_by(professional_id=professional_id, service_status='requested').count()
    accepted_requests = ServiceRequest.query.filter_by(professional_id=professional_id, service_status='accepted').count()
    rejected_requests = ServiceRequest.query.filter_by(professional_id=professional_id, service_status='rejected').count()

    return jsonify({
        'pendingRequests': pending_requests,
        'acceptedRequests': accepted_requests,
        'rejectedRequests': rejected_requests
    }), 200
       
    
@app.route('/api/professional/details', methods=['GET'])
def get_professional_details():
    professional_id = request.args.get('professional_id')
    if not professional_id:
        return jsonify({'message': 'Professional ID is required'}), 400

    professional = User.query.get(professional_id)
    if not professional:
        return jsonify({'message': 'Professional not found'}), 404

    professional_details = {
        'id': professional.id,
        'username': professional.username,
        'email': professional.email,
        'service_category_name': professional.service_category.name if professional.service_category else 'N/A',
        'years_of_experience': professional.years_of_experience
    }
    return jsonify(professional_details), 200


@app.route('/api/customers', methods=['GET'])
def get_customers():
    customers = User.query.join(Role, User.roles).filter(Role.name == 'customer').all()
    customers_list = [{
        'id': customer.id,
        'username': customer.username,
        'email': customer.email,
        'active': customer.active
    } for customer in customers]
    return jsonify(customers_list), 200


@app.route('/api/user/<int:user_id>', methods=['GET'])
# @cache.memoize(timeout=5)
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user_details = {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }
    return jsonify(user_details), 200


@app.route('/api/admin/summary', methods=['GET'])
def get_admin_summary():
    customers_count = User.query.join(Role, User.roles).filter(Role.name == 'customer').count()
    service_providers_count = User.query.join(Role, User.roles).filter(Role.name == 'service_provider').count()
    services_count = Service.query.count()
    
    services = Service.query.all()
    category_distribution = {}
    services_details = []
    
    for service in services:
        category_name = service.category.name if service.category else 'N/A'
        if category_name not in category_distribution:
            category_distribution[category_name] = 0
        category_distribution[category_name] += 1
        
        # Calculate average rating for each service and gather reviews
        reviews = ServiceReview.query.join(ServiceRequest).filter(ServiceRequest.service_id == service.id).all()
        if reviews:
            average_rating = sum(review.rating for review in reviews) / len(reviews)
            reviews_text = [review.review for review in reviews]
        else:
            average_rating = 0
            reviews_text = []
        
        services_details.append({
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'rating': average_rating,
            'reviews': reviews_text
        })
    
    summary_data = {
        'customersCount': customers_count,
        'serviceProvidersCount': service_providers_count,
        'servicesCount': services_count,
        'categoryDistribution': category_distribution,
        'services': services_details
    }
    
    return jsonify(summary_data), 200

    
# Endpoint to fetch services
@app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    services_list = [{
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'category_id': service.category_id,  # Ensure category_id is included
        'category_name': service.category.name  # Include category name
    } for service in services]
    return jsonify(services_list), 200


# Endpoint to create service request
@app.route('/api/customer/create_service_request', methods=['POST'])
def create_service_request():
    data = request.get_json()
    customer_id = data.get('customer_id')
    service_id = data.get('service_id')
    professional_id = data.get('professional_id')

    if not customer_id or not service_id or not professional_id:
        return jsonify({'message': 'Missing required fields'}), 400

    new_request = ServiceRequest(
        customer_id=customer_id,
        service_id=service_id,
        professional_id=professional_id,
        service_status='requested'
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'message': 'Service request created'}), 201


@app.route('/api/professionals', methods=['GET'])
@cache.cached(timeout=5, key_prefix='cache')
def get_professionals():
    professionals = User.query.join(Role, User.roles).filter(Role.name == 'service_provider').all()
    professionals_list = [{
        'id': professional.id,
        'username': professional.username,
        'email': professional.email,
        'service_category_name': professional.service_category.name if professional.service_category else 'N/A',
        'years_of_experience': professional.years_of_experience,
        'active': professional.active
    } for professional in professionals]
    return jsonify(professionals_list), 200


@app.route('/api/customer/service_requests', methods=['GET'])
@auth_required('token')
@roles_accepted('customer')
def get_customer_service_requests():
    customer_id = request.args.get('customer_id')
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    requests_list = []
    for service_request in service_requests:  # Rename the local variable to avoid conflict
        if service_request.service:  # Check if the service is not None
            requests_list.append({
                'id': service_request.id,
                'service_name': service_request.service.name,
                'service_description': service_request.service.description,
                'service_id': service_request.service.id,
                'service_price': service_request.service.price,
                'professional_name': service_request.professional.username if service_request.professional else 'N/A',
                'service_status': service_request.service_status
            })
    return jsonify(requests_list), 200


@app.route('/api/customer/edit_service_request/<int:request_id>', methods=['PUT'])
def edit_service_request(request_id):
    data = request.get_json()
    service_status = data.get('service_status')

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404

    service_request.service_status = service_status
    db.session.commit()
    return jsonify({'message': 'Service request updated'}), 200


@app.route('/api/customer/summary', methods=['GET'])
def get_customer_summary():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify({'message': 'Customer ID is required'}), 400

    total_requests = ServiceRequest.query.filter_by(customer_id=customer_id).count()
    requests_in_progress = ServiceRequest.query.filter_by(customer_id=customer_id, service_status='in progress').count()
    completed_requests = ServiceRequest.query.filter_by(customer_id=customer_id, service_status='completed').count()
    pending_requests = ServiceRequest.query.filter_by(customer_id=customer_id, service_status='requested').count()
    closed_requests = ServiceRequest.query.filter_by(customer_id=customer_id, service_status='closed').count()

    return jsonify({
        'totalRequests': total_requests,
        'requestsInProgress': requests_in_progress,
        'completedRequests': completed_requests,
        'pendingRequests': pending_requests,
        'closedRequests': closed_requests
    }), 200


@app.route('/api/customer/details', methods=['GET'])
def get_customer_details():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify({'message': 'Customer ID is required'}), 400

    customer = User.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    customer_details = {
        'id': customer.id,
        'username': customer.username,
        'email': customer.email
    }
    return jsonify(customer_details), 200


@app.route('/api/customer/rate_service', methods=['POST'])
def rate_service():
    data = request.get_json()
    service_request_id = data.get('service_request_id')
    customer_id = data.get('customer_id')
    rating = data.get('rating')
    review = data.get('review')

    if not service_request_id or not customer_id or not rating or not review:
        return jsonify({'message': 'Missing required fields'}), 400

    service_review = ServiceReview(
        service_request_id=service_request_id,
        customer_id=customer_id,
        rating=rating,
        review=review
    )
    db.session.add(service_review)
    db.session.commit()
    return jsonify({'message': 'Service rated successfully'}), 201


@app.route('/api/admin/blacklist_user/<int:user_id>', methods=['PUT'])
def blacklist_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.active = False
    db.session.commit()
    return jsonify({'message': 'User blacklisted'}), 200


@app.route('/api/admin/unblacklist_user/<int:user_id>', methods=['PUT'])
def unblacklist_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.active = True
    db.session.commit()
    return jsonify({'message': 'User unblacklisted'}), 200


@app.route('/api/unapproved_providers', methods=['GET'])
def get_unapproved_providers():
    unapproved_providers = User.query.filter(
        User.active == False,
        User.roles.any(name='service_provider')
    ).all()
    providers_list = [{
        'id': provider.id,
        'username': provider.username,
        'email': provider.email,
        'service_category_name': provider.service_category.name if provider.service_category else 'N/A',
        'years_of_experience': provider.years_of_experience
    } for provider in unapproved_providers]
    return jsonify(providers_list), 200


@app.route('/api/admin/approve_provider/<int:provider_id>', methods=['PUT'])
def approve_provider(provider_id):
    provider = User.query.get(provider_id)
    if not provider:
        return jsonify({'message': 'Provider not found'}), 404

    provider.active = True
    db.session.commit()
    return jsonify({'message': 'Provider approved successfully'}), 200


@app.route('/api/customer/services', methods=['GET'])
def get_customer_services():
    customer_id = request.args.get('customer_id')
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    services_list = []
    for request in service_requests:
        if request.service:  # Check if the service is not None
            services_list.append({
                'id': request.service.id,
                'name': request.service.name,
                'description': request.service.description,
                'price': request.service.price,
                'category_name': request.service.category.name if request.service.category else 'N/A'
            })
    return jsonify(services_list), 200


@app.route('/api/services/<int:service_id>', methods=['GET'])
def get_service_details(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}), 404

    reviews = ServiceReview.query.filter_by(service_request_id=service_id).all()
    reviews_list = [{
        'id': review.id,
        'rating': review.rating,
        'review': review.review
    } for review in reviews]

    total_ratings = sum(review.rating for review in reviews)
    average_rating = total_ratings / len(reviews) if reviews else 0

    service_details = {
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'category_name': service.category.name if service.category else 'N/A',
        'reviews': reviews_list,
        'total_ratings': total_ratings,
        'average_rating': average_rating
    }
    return jsonify(service_details), 200


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'active': user.active
    } for user in users]
    return jsonify(users_list), 200


@app.route('/api/admin/toggle_user_status/<int:user_id>', methods=['PUT'])
def toggle_user_status(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.active = data.get('active', user.active)
    db.session.commit()
    return jsonify({'message': 'User status updated'}), 200



#...............................................................................................................



# excel.init_excel(app)
if __name__ == '__main__':
    #init flask_excel
    app.run()

