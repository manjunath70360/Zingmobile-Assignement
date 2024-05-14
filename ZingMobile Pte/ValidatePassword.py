def validate_password(password):
    if len(password) < 8:
        return False
    has_lower = False
    has_upper = False
    has_digit = False
    has_symbol = False
    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in ['_', '@', '$']:
            has_symbol = True
        else:
            return False
    return has_lower and has_upper and has_digit and has_symbol

# Test case
password = input("Enter password: ")
if validate_password(password):
    print("Password is safe")
else:
    print("Password does not meet the criteria")
