def maskify(mobile_number):
    masked_number = '#' * (len(mobile_number) - 3) + mobile_number[-3:]
    print(masked_number)

# Test case
maskify("9988776655")  # Output: #######655
