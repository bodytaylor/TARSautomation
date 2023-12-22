def generate_unique_code(full_name, existing_codes):
    # Split the full name into words
    words = full_name.split()

    # Take the first letter from each word and concatenate them
    code = ''.join(word[0] for word in words)

    # Ensure the code is exactly 3 characters by truncating or padding with 'X'
    code = (code + 'XXX')[:3]

    # Check if the code is already in the database
    while code.upper() in existing_codes:
        # If the code is a duplicate, modify it using available characters in the name
        code = modify_code(code, words)

    return code.upper()

def modify_code(code, words):
    # Increment the last character in the code
    last_char = code[-1]
    if last_char.isalpha():
        code = code[:-1] + chr((ord(last_char) - ord('A') + 1) % 26 + ord('A'))
    else:
        code = code[:-1] + 'A'

    # Take the first letter from each word and concatenate them
    code += ''.join(word[0] for word in words)

    # Ensure the code is exactly 3 characters by truncating or padding with 'X'
    code = (code + 'XXX')[:3]

    return code

# Example usage:
existing_codes = {'ABC', 'DEF', 'GHI'}  # Replace this with your actual database of codes
full_name = input("Enter your full name: ")
result_code = generate_unique_code(full_name, existing_codes)
print("Generated code:", result_code)
