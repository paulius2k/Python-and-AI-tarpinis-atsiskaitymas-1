from InquirerPy import prompt
from InquirerPy.validator import NumberValidator

def custom_integer_validator(value):
    print()
    print(f"Validating: {value}")  # Debugging
    number_validator = NumberValidator()
    try:
        number_validator.validate(value)
    except Exception as e:
        print(f"Validation error: {e}")  # Debugging
        return False

    if int(value) <= 0:
        print("Custom validation failed: Value must be > 0.")  # Debugging
        return False

    print("Validation passed.")  # Debugging
    return True


def failing_validator(value):
    return False


questions = [
    {
        "type": "input",
        "name": "number",
        "message": "Enter a positive integer:",
        "validate": custom_integer_validator,
    }
]

answers = prompt(questions)
print(f"You entered: {answers['number']}")
