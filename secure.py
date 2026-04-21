import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

def search_product_safe(name):
    # SECURE: Using parameterised query with ? placeholder
    query = "SELECT * FROM products WHERE name LIKE ?"
    # Add % wildcards to the parameter, not the query
    param = f'%{name}%'
    print(f'Query: {query}')
    print(f'Parameter: {param}')
    rows = conn.execute(query, (param,)).fetchall()
    print(f'Result: {rows}\n')
    return rows

def login_safe(username, password):
    # SECURE: Using parameterised query with ? placeholders
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f'Query: {query}')
    print(f'Parameters: ({username}, {password})')
    row = conn.execute(query, (username, password)).fetchone()
    print(f'Result: {row}\n')
    return row

# Test attacks - all should return empty results
print("=== TEST 1: OR 1=1 attack ===")
print('Result:', search_product_safe("' OR 1=1--"))

print("\n=== TEST 2: UNION attack ===")
print('Result:', search_product_safe("' UNION SELECT id,username,password,role FROM users--"))

print("\n=== TEST 3: Login bypass with comment ===")
print('Result:', login_safe("admin'--", 'anything'))

print("\n=== TEST 4: Always true login ===")
print('Result:', login_safe("' OR '1'='1", "' OR '1'='1"))

conn.close()