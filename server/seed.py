#!/usr/bin/env python3

import random
import csv
import sys

# Remote library imports
from faker import Faker
from rich import print

# Local imports
from server.config import db, app
from models import Property, User, Review  # Adjust the import based on your project structure

fake = Faker()

def clear_tables():
    with app.app_context():
        print('\n[purple]------------- BEGIN ------------[/purple]')
        print('\n')

        # Clean Database
        print('[purple]Cleaning Database 🧽 [/purple]...\n')
        try:
            Review.query.delete()
            Property.query.delete()
            User.query.delete()
            db.session.commit()
            print('\t[green]Cleaning Complete[/green] ✅\n')
        except Exception as e:
            print('[red]Cleaning Failed[/red] 😞', str(e), '\n')
            sys.exit(1)

# Create Properties
def load_properties(filename='properties.csv'):
    with app.app_context():
        print('[purple]Creating Properties 🏡[/purple] ...\n')
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                try:
                    # Adjust fields based on your CSV structure
                    address, price, bedrooms, bathrooms, sq_ft, description = row
                    property = Property(
                        address=address,
                        price=float(price),
                        bedrooms=int(bedrooms),
                        bathrooms=int(bathrooms),
                        sq_ft=int(sq_ft),
                        description=description
                    )
                    db.session.add(property)
                except ValueError as ve:
                    print(f"Error processing row {row}: {ve}")
                    print('\t[red]Property Creation Failed[/red] 😞\n')
                    sys.exit(1)
            db.session.commit()
            print('\t[green]Properties Created ✅[/green] \n')

# Create Users
def create_users():
    with app.app_context():
        print('[purple]Creating Users[/purple] 🧑🏻‍💻 ...\n')
        try:
            users = []
            usernames = []
            emails = []
            for _ in range(20):
                username = fake.first_name()
                email = fake.email()
                while username in usernames or email in emails:
                    username = fake.first_name()
                    email = fake.email()
                usernames.append(username)
                emails.append(email)
                user = User(username=username, email=email)
                user.password_hash = user.username + 'Password1!'
                users.append(user)
            db.session.add_all(users)
            db.session.commit()
            print('\t[green]Users Created[/green] ✅ \n')
        except Exception as e:
            print('\t[red]User Creation Failed[/red] 😞 \n')
            print(e)
            sys.exit(1)

# Create Reviews
def create_reviews():
    with app.app_context():
        print('[purple]Creating Reviews[/purple] ✍🏽 ...\n')
        
        try:
            properties = Property.query.all()
            users = User.query.all()
            for _ in range(100):
                property = random.choice(properties)
                user = random.choice(users)
                new_review = Review(
                    rating=random.randint(1, 5),
                    review=fake.paragraph(),
                    user_id=user.id,
                    property_id=property.id
                )
                db.session.add(new_review)
            db.session.commit()
            print('\t[green]Reviews Created ✅[/green]\n')
        except Exception as e:
            print('\t[red]Review Creation Failed[/red] 😞 \n')
            print(e)
            sys.exit(1)

if __name__ == '__main__':
    clear_tables()
    load_properties()
    create_users()
    create_reviews()  # Include this if your app includes reviews
