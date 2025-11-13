import sqlite3

conn = sqlite3.connect("restaurant.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('admin', 'customer'))
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE 
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    price REAL,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(id)
)
""")


conn.commit()

def insert_default_users():
    users = [
        ("ben", "Ben@123", "admin"),
        ("arjun", "Arjun@123", "admin"),
        ("aryan", "Aryan@123", "customer"),
        ("rahul", "Rahul@123", "customer"),
        ("tom", "Tom@123", "customer")
    ]

    for u in users:
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", u)
        except sqlite3.IntegrityError:
            pass

    conn.commit()

insert_default_users()

def insert_default_data():
    categories = ["Beverages", "Snacks", "Main Course", "Desserts"]

    for cat in categories:
        try:
            c.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
        except sqlite3.IntegrityError:
            pass

    conn.commit()

    c.execute("SELECT id, name FROM categories")
    cats = {name: cid for cid, name in c.fetchall()}

    items = [
        ("Tea", 20, cats["Beverages"]),
        ("Coffee", 30, cats["Beverages"]),
        ("Cold Drink", 40, cats["Beverages"]),
        ("Samosa", 15, cats["Snacks"]),
        ("Sandwich", 50, cats["Snacks"]),
        ("French Fries", 60, cats["Snacks"]),
        ("Veg Biryani", 120, cats["Main Course"]),
        ("Chicken Biryani", 180, cats["Main Course"]),
        ("Paneer Butter Masala", 150, cats["Main Course"]),
        ("Ice Cream", 40, cats["Desserts"]),
        ("Gulab Jamun", 25, cats["Desserts"]),
    ]

    for name, price, cid in items:
        try:
            c.execute("INSERT INTO menu_items (item_name, price, category_id) VALUES (?, ?, ?)", (name, price, cid))
        except sqlite3.IntegrityError:
            pass

    conn.commit()

insert_default_data()


def login():
    print("\n LOGIN ")
    username = input("Username: ")
    password = input("Password: ")

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    if user:
        print(f"\n Welcome {user[1]}! (Role: {user[3]})\n")
        return user
    else:
        print(" Invalid username or password!\n")
        return None


def add_user():
    print("\n ADD NEW USER ")
    username = input("Enter new username: ")
    password = input("Enter password: ")
    role = input("Role (admin/customer): ")

    if role not in ("admin", "customer"):
        print(" Invalid role!\n")
        return

    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        print(" User added successfully!\n")
    except sqlite3.IntegrityError:
        print(" Username already exists!\n")


def view_categories():
    c.execute("SELECT * FROM categories")
    rows = c.fetchall()
    print("\nCATEGORIES ")
    for r in rows:
        print(f"{r[0]}. {r[1]}")
    print()


def add_category():
    name = input("Enter category name: ")

    try:
        c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        print(" Category added!\n")
    except sqlite3.IntegrityError:
        print(" Category already exists!\n")


def delete_category():
    view_categories()
    cid = input("Enter category ID to delete: ")
    c.execute("DELETE FROM categories WHERE id=?", (cid,))
    conn.commit()
    print("Category deleted!\n")


def view_menu():
    print("\n MENU ITEMS ")
    c.execute("""
    SELECT m.id, m.item_name, m.price, c.name
    FROM menu_items m
    LEFT JOIN categories c ON m.category_id = c.id
    """)
    rows = c.fetchall()
    for r in rows:
        print(f"{r[0]}. {r[1]} - ₹{r[2]} ({r[3]})")
    print()


def add_menu_item():
    item_name = input("Item name: ")
    price = float(input("Price: "))

    print("\nSelect category:")
    view_categories()
    cat_id = input("Category ID: ")

    c.execute("INSERT INTO menu_items (item_name, price, category_id) VALUES (?, ?, ?)", (item_name, price, cat_id))
    conn.commit()
    print(" Menu item added!\n")


def delete_menu_item():
    view_menu()
    item_id = input("Enter item ID to delete: ")
    c.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
    conn.commit()
    print(" Item deleted!\n")


def update_menu_item():
    view_menu()
    item_id = input("Enter item ID to update: ")

    new_name = input("New name: ")
    new_price = float(input("New price: "))

    print("\nSelect category:")
    view_categories()
    new_cat = input("New category ID: ")

    c.execute("""
    UPDATE menu_items
    SET item_name=?, price=?, category_id=?
    WHERE id=?
    """, (new_name, new_price, new_cat, item_id))

    conn.commit()
    print(" Item updated!\n")


def admin_menu():
    while True:
        print("""
 ADMIN MENU 
1. Add Category
2. View Categories
3. Delete Category
4. Add Menu Item
5. View Menu
6. Update Menu Item
7. Delete Menu Item
8. Add User
9. Logout
""")
        ch = input("Choice: ")

        if ch == "1": add_category()
        elif ch == "2": view_categories()
        elif ch == "3": delete_category()
        elif ch == "4": add_menu_item()
        elif ch == "5": view_menu()
        elif ch == "6": update_menu_item()
        elif ch == "7": delete_menu_item()
        elif ch == "8": add_user()
        elif ch == "9": return
        else:
            print("Invalid choice!\n")


def place_order(user_id):
    print("\n PLACE ORDER ")
    view_menu()

    cart = []
    total = 0

    while True:
        item_id = input("Enter item ID to add to order (or 'done' to finish): ")

        if item_id.lower() == "done":
            break

        c.execute("SELECT item_name, price FROM menu_items WHERE id=?", (item_id,))
        item = c.fetchone()

        if item:
            cart.append(item)
            total += item[1]
            print(f" Added: {item[0]} (₹{item[1]})")
        else:
            print(" Invalid item ID!")

    if not cart:
        print("No items selected.\n")
        return

    print("\nORDER SUMMARY ")
    for name, price in cart:
        print(f"{name} - ₹{price}")
    print(f"TOTAL: ₹{total}")

conn.commit()
        
def customer_menu(user):
    while True:
        print("""
CUSTOMER MENU 
1. View Menu
2. Place Order
3. Logout
""")
        ch = input("Choice: ")

        if ch == "1": view_menu()
        elif ch == "2": place_order(user[0])
        elif ch == "3": return
        else:
            print("Invalid choice!\n")


def main():
    while True:
        print("""

   RESTAURANT MENU SYSTEM

1. Login
2. Exit
""")
        ch = input("Choice: ")

        if ch == "1":
            user = login()
            if user:
                if user[3] == "admin":
                    admin_menu()
                else:
                    customer_menu(user)
        elif ch == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!\n")

main()
conn.close()

