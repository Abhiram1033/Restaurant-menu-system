The Restaurant Menu Management System is a command-line application built using Python and SQLite.
It allows restaurant staff (Admin role) to manage categories, menu items, and users, while customers can view the menu.

This project demonstrates:

Database connectivity using SQLite

CRUD operations

Role-based access

Command Line Interface design

Secure login using username & password

Supports two roles:

Admin

Customer

Feature	Description
Add Category	Create new food categories
View Categories	Display all categories
Delete Category	Remove unwanted categories
Add Menu Item	Add dishes with price & category
View Menu	Display all menu items
Update Menu Item	Modify name, price, or category
Delete Menu Item	Remove items
Add Users	Add new admin or customer accounts
Customer Features
Feature	Description
View Menu	Display available food items with categories & price
place order 
Logout	Exit 


 Technology Stack

Python 3

SQLite3 Database

CLI (Command Line Interface)

 Database Schema
1️ users
Column	Type	Description
id	INTEGER	Primary Key
username	TEXT	Unique username
password	TEXT	User password
role	TEXT	admin / customer
2️ categories
Column	Type	Description
id	INTEGER	Primary Key
name	TEXT	Category name
3️ menu_items
Column	Type	Description
id	INTEGER	Primary Key
item_name	TEXT	Name of the dish
price	REAL	Price of the dish
category_id	INTEGER	Foreign key referencing categories

 How to Run the Project
Step 1: Install Python

Ensure you have Python 3.x installed.

Step 2: Download the project

 download the repository:


Step 3: Run the script
python restaurant.py

Step 4: Default Admin Logins

Use any of the default users:

Username	Password	Role
ben	Ben@123	admin
arjun	Arjun@123	admin
aryan	Aryan@123	customer
rahul	Rahul@123	customer
tom	Tom@123	customer


