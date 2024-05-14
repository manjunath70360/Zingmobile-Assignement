# Decimal to Hexadecimal
def decimal_to_hex(decimal):
    try:
        decimal = int(decimal)
    except ValueError:
        print("Invalid input")
        return
    hexadecimal = ""
    while decimal > 0:
        remainder = decimal % 16
        if remainder < 10:
            hexadecimal = str(remainder) + hexadecimal
        else:
            hexadecimal = chr(ord('A') + remainder - 10) + hexadecimal
        decimal //= 16
    print(hexadecimal)

# Hexadecimal to Decimal
def hex_to_decimal(hexadecimal):
    decimal = 0
    try:
        for digit in hexadecimal:
            if '0' <= digit <= '9':
                decimal = decimal * 16 + int(digit)
            elif 'A' <= digit <= 'F':
                decimal = decimal * 16 + (ord(digit) - ord('A') + 10)
            else:
                print("Invalid input")
                return
        print(decimal)
    except ValueError:
        print("Invalid input")

# Test cases
decimal_to_hex(123)  # Output: 7B
hex_to_decimal("7B") # Output: 123
