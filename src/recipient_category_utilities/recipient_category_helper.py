# Required fields for recipient lists
REQUIRED_FIELDS = ["id", "recipient_category", "description", "created_at", "updated_at"]

# Expected messages
EXPECTED_MESSAGES = {
    "duplicate_entry": {
        "error": "Duplicate entry",
        "message": "A recipient list with this category already exists."
    },
    "invalid_input": {
        "error": "Invalid input",
        "message": "recipient_category is required and cannot be null."
    },
    # Add more expected messages as needed
}
