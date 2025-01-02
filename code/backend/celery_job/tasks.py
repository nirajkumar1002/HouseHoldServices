from celery import Celery
import flask_excel
from celery import shared_task
import time


import os


from celery import shared_task

from models import Role, User, ServiceCategory
import csv
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)



@shared_task(ignore_result=False)
def export_categories_csv():
    
    # with app.app_context():
    categories = ServiceCategory.query.all()
    
    # Prepare data for CSV
    data = [{'Category_name': i.name} for i in categories]
    
    column_names = ['Category_name']
    
    # Ensure the directory exists
    os.makedirs('user-downloads', exist_ok=True)
    
    logger.info('Exporting categories to CSV')
    
    # Save the CSV file
    with open('user-downloads/catergoy.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(data)
        
    return 'category.csv'



@shared_task(ignore_result=False)
def export_closed_service_requests():
    # logger.info('step0')
    # Query service requests with status "closed"
    closed_requests = ServiceRequest.query.filter_by(service_status='closed').all()
    # logger.info('step1')
    # Prepare data for CSV
    data = [{
        'Service ID': request.service_id,
        'Customer ID': request.customer_id,
        'Professional ID': request.professional_id,
        'Date of Request': request.created_at,
        'Remarks': request.service_status
    } for request in closed_requests]
    
    column_names = ['Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Remarks']
    
    # Ensure the directory exists
    os.makedirs('user-downloads', exist_ok=True)
    
    # Save the CSV file
    csv_file_path = 'user-downloads/closed_service_requests.csv'
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(data)
    
    # Send an alert email once done
    admin_email = 'admin@example.com'  # Replace with the actual admin email
    subject = 'Closed Service Requests Export Completed'
    content_body = f'The export of closed service requests has been completed. You can download the file from {csv_file_path}.'
    send_message(admin_email, subject, content_body)
    
    return 'Data exported successfully'





from celery_job.helper_fun import send_message

#email to s1@a.com in every minute
@shared_task(ignore_result=False)
def send_email():
    to = 's1@a.com'
    subject = 'Test Email'
    content_body = 'This is a test email'
    send_message(to, subject, content_body)
    
    return 'Email sent successfully'



from celery import shared_task
from celery_job.helper_fun import send_message
from models import db, ServiceRequest, User

#Each day emails to all professionals with pending requests
@shared_task(ignore_result=False)
def send_email_daily():
    # Query service requests with status "requested"
    pending_requests = ServiceRequest.query.filter_by(service_status='requested').all()
    
    for request in pending_requests:
        professional = User.query.get(request.professional_id)
        if professional:
            to = professional.email
            subject = 'Pending Service Request Reminder'
            content_body = f'Dear {professional.username},<br><br>You have a pending service request. Please visit the application to accept or reject the request.<br><br>Thank you!'
            send_message(to, subject, content_body)
    
    return 'Daily Emails sent successfully'



@shared_task(ignore_result=False)
def send_monthly_report():
    # Query users with the "customer" role
    customer_role = Role.query.filter_by(name='customer').first()
    if not customer_role:
        return 'No customers found'

    customers = User.query.filter(User.roles.contains(customer_role)).all()
    
    for customer in customers:
        services_requested = ServiceRequest.query.filter_by(customer_id=customer.id, service_status='requested').count()
        services_in_progress = ServiceRequest.query.filter_by(customer_id=customer.id, service_status='in progress').count()
        service_rejected = ServiceRequest.query.filter_by(customer_id=customer.id, service_status='rejected').count()
        services_closed = ServiceRequest.query.filter_by(customer_id=customer.id, service_status='closed').count()
        
        content_body = f"""
        <h1>Monthly Activity Report</h1>
        <p>Dear {customer.username},</p>
        <p>Here is your activity report for the month:</p>
        <ul>
            <li>Services Requested: {services_requested}</li>
            <li>Services Pending: {services_in_progress}</li>
            <li>Services Rejected: {service_rejected}</li>
            <li>Services Closed: {services_closed}</li>
        </ul>
        <p>Thank you for using our service!</p>
        """
        
        send_message(customer.email, 'Monthly Activity Report', content_body)
    
    return 'Monthly reports sent successfully'
