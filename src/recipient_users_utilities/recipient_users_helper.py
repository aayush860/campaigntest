# config.py

# Required fields for recipient lists
REQUIRED_FIELDS = ["name", "email", "recipient_category"]

# Expected messages
EXPECTED_MESSAGES = {
    "duplicate_email": {
        "error": "Duplicate entry",
        "message": "A recipient with this email already exists."
    },
    "invalid_email_format": {
        "error": "Invalid input",
        "message": "The email format is invalid."
    },
    "email_required": {
        "error": "Invalid input",
        "message": "email is required and cannot be null."
    },
    "name_too_long": {
        "error": "Invalid input",
        "message": "name cannot be more than 32 characters."
    },
    "recipient_category_required": {
        "error": "Invalid input",
        "message": "recipient_category is required and cannot be null."
    },
    "no_recipients_found": {
        "error": "Not Found",
        "message": "No recipients found for the given category."
    }
}
