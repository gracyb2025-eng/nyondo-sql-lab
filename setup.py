import sqlite3

# Connect to database (creates it if doesn't exist)
conn = sqlite3.connect('nyondo_stock.db')

# Create products table (ONCE)
conn.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
)
''')

# Create users table
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'attendant'
)
''')

# Insert users (using INSERT OR IGNORE to avoid duplicates)
conn.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
conn.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('fatuma', 'pass456', 'attendant')")
conn.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('wasswa', 'pass789', 'manager')")

# Clear existing products to avoid duplicates
conn.execute('DELETE FROM products')

# Insert products
products = [
    ('Cement (bag)', 'Portland cement 50kg bag', 35000),
    ('Iron Sheet 3m', 'Gauge 30 roofing sheet 3m long', 110000),
    ('Paint 5L', 'Exterior wall paint white 5L', 60000),
    ('Nails 1kg', 'Common wire nails 1kg pack', 12000),
    ('Timber 2x4', 'Pine timber plank 2x4 per metre', 25000)
]

conn.executemany('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', products)
conn.commit()

# Verify everything
print("=== Users Table ===")
users = conn.execute('SELECT * FROM users').fetchall()
for user in users:
    print(user)

print("\n=== Products Table ===")
products_result = conn.execute('SELECT * FROM products').fetchall()
for product in products_result:
    print(product)

# Close connection ONLY ONCE at the very end
conn.close()