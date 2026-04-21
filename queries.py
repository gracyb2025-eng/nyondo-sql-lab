import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

print("=== Query A: Get every column of every product ===")
rows = conn.execute('SELECT * FROM products').fetchall()
for row in rows:
    print(row)

print("\n=== Query B: Get only name and price ===")
rows = conn.execute('SELECT name, price FROM products').fetchall()
for row in rows:
    print(row)

print("\n=== Query C: Product with id = 3 ===")
row = conn.execute('SELECT * FROM products WHERE id = 3').fetchone()
print(row)

print("\n=== Query D: Products with name containing 'sheet' ===")
rows = conn.execute('SELECT * FROM products WHERE name LIKE "%sheet%"').fetchall()
for row in rows:
    print(row)

print("\n=== Query E: Products sorted by price, highest first ===")
rows = conn.execute('SELECT * FROM products ORDER BY price DESC').fetchall()
for row in rows:
    print(row)

print("\n=== Query F: 2 most expensive products ===")
rows = conn.execute('SELECT * FROM products ORDER BY price DESC LIMIT 2').fetchall()
for row in rows:
    print(row)

print("\n=== Query G: Update Cement price to 38,000 ===")
conn.execute('UPDATE products SET price = 38000 WHERE id = 1')
conn.commit()
rows = conn.execute('SELECT * FROM products').fetchall()
for row in rows:
    print(row)

conn.close()