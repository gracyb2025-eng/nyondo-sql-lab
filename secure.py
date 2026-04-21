import sqlite3
import re

conn = sqlite3.connect('nyondo_stock.db')

def validate_product_name(name):
    """Validate product name: string, at least 2 chars, no < > or ;"""
    if not isinstance(name, str):
        return False, "Must be a string"
    if len(name) < 2:
        return False, "Must be at least 2 characters"
    if '<' in name or '>' in name or ';' in name:
        return False, "Cannot contain < > or ; characters"
    return True, ""

def validate_username(username):
    """Validate username: string, no spaces, not empty"""
    if not isinstance(username, str):
        return False, "Must be a string"
    if len(username) == 0:
        return False, "Cannot be empty"
    if ' ' in username:
        return False, "Cannot contain spaces"
    return True, ""

def validate_password(password):
    """Validate password: string, at least 6 characters"""
    if not isinstance(password, str):
        return False, "Must be a string"
    if len(password) < 6:
        return False, "Must be at least 6 characters"
    return True, ""

def search_product_safe(name):
    # Input validation first
    valid, error = validate_product_name(name)
    if not valid:
        print(f"Validation failed: {error}")
        print(f'Result: []\n')
        return []
    
    # Then parameterised query
    query = "SELECT * FROM products WHERE name LIKE ?"
    param = f'%{name}%'
    print(f'Query: {query}')
    print(f'Parameter: {param}')
    rows = conn.execute(query, (param,)).fetchall()
    print(f'Result: {rows}\n')
    return rows

def login_safe(username, password):
    # Input validation first
    valid_user, error_user = validate_username(username)
    if not valid_user:
        print(f"Validation failed - username: {error_user}")
        print(f'Result: None\n')
        return None
    
    valid_pass, error_pass = validate_password(password)
    if not valid_pass:
        print(f"Validation failed - password: {error_pass}")
        print(f'Result: None\n')
        return None
    
    # Then parameterised query
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f'Query: {query}')
    print(f'Parameters: ({username}, {password})')
    row = conn.execute(query, (username, password)).fetchone()
    print(f'Result: {row}\n')
    return row

# TEST CASES
print("=" * 50)
print("TESTING search_product_safe")
print("=" * 50)

print("\n1. search_product_safe('cement') - should work")
search_product_safe('cement')

print("\n2. search_product_safe('') - should be rejected")
search_product_safe('')

print("\n3. search_product_safe('<script>') - should be rejected")
search_product_safe('<script>')

print("\n" + "=" * 50)
print("TESTING login_safe")
print("=" * 50)

print("\n4. login_safe('admin', 'admin123') - should work")
login_safe('admin', 'admin123')

print("\n5. login_safe('admin', 'ab') - should be rejected (too short)")
login_safe('admin', 'ab')

print("\n6. login_safe('ad min', 'pass123') - should be rejected (space in username)")
login_safe('ad min', 'pass123')

# Also test that injection attempts still fail
print("\n" + "=" * 50)
print("VERIFYING INJECTION ATTACKS STILL FAIL")
print("=" * 50)

print("\nInjection attempt 1:")
search_product_safe("' OR 1=1--")

print("\nInjection attempt 2:")
search_product_safe("' UNION SELECT id,username,password,role FROM users--")

print("\nInjection attempt 3:")
login_safe("admin'--", 'anything')

print("\nInjection attempt 4:")
login_safe("' OR '1'='1", "' OR '1'='1")

conn.close()