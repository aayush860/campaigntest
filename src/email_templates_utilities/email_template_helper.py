# config.py

# Required fields for email templates
REQUIRED_FIELDS_TEMPLATE = ["name", "content", "created_at", "updated_at"]

# Expected messages for email templates
EXPECTED_MESSAGES_TEMPLATE = {
    "duplicate_name": {
        "error": "Duplicate entry",
        "message": "A template with this name already exists."
    },
    "invalid_name_format": {
        "error": "Invalid input",
        "message": "The template name contains special characters."
    },
    "name_required": {
        "error": "Invalid input",
        "message": "Template name is required and cannot be null."
    },
    "name_too_long": {
        "error": "Invalid input",
        "message": "Template name cannot be more than 20 characters."
    }
}
