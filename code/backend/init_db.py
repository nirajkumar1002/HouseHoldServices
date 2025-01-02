from models import db, user_datastore, ServiceCategory
from app import create_app
import uuid

app, api = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables created")
    
    # # Create roles
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='customer', description='Customer')
    user_datastore.find_or_create_role(name='service_provider', description='Service Provider')
    
    db.session.commit()
    
    # Create service categories
    categories = [
        "Beauty & Spa",
        "Car Repairing",
        "Cleaning",
        "Electrical",
        "Event Planning",
        "Fitness Training",
        "Nutrition Counseling",
        "Plumbing",
        "Towing Service"
    ]

    for category_name in categories:
        category = ServiceCategory(name=category_name, description=f"{category_name} services")
        db.session.add(category)
    
    db.session.commit()
    print("Service categories created")
    
    # # Create admin user if not exists
    admin_user = user_datastore.find_user(email='a@a.com')
    if not admin_user:
        new_user = user_datastore.create_user(username="admin", email="a@a.com", password="a", fs_uniquifier=str(uuid.uuid4()))
        user_datastore.add_role_to_user(new_user, 'admin')
        db.session.commit()
    
    # # Create service provider user if not exists
    # service_provider_user = user_datastore.find_user(email='s@a.com')
    # if not service_provider_user:
    #     new_user = user_datastore.create_user(username='service_provider', email="s@a.com", password="s", fs_uniquifier=str(uuid.uuid4()))
    #     user_datastore.add_role_to_user(new_user, 'service_provider')
    #     db.session.commit()
    
    # # Create customer user if not exists
    # customer_user = user_datastore.find_user(email='c@a.com')
    # if not customer_user:
    #     new_user = user_datastore.create_user(username="customer", email="c@a.com", password="c", fs_uniquifier=str(uuid.uuid4()))
    #     user_datastore.add_role_to_user(new_user, 'customer')
    #     db.session.commit()
    
    print("Database initialized with roles, categories, and users")