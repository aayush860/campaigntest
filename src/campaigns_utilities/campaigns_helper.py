from datetime import datetime, timedelta
import time
# Test data for campaigns
TEST_DATA_CAMPAIGN = {
    "valid_post_data": {
        "name": "TestCampaign"+str(datetime.utcnow()),
        "send_time": (datetime.utcnow()+timedelta(hours=5)).isoformat(),  # To be updated dynamically
        "campaign_template": "Hello Admins How are You",
        "recipient_category": "vendors",
        "template_name": "Admin_Template"
    },
    "invalid_special_name": {
        "name": "Special@Name"+str(datetime.utcnow()),
        "send_time": (datetime.utcnow()+timedelta(hours=5)).isoformat(),
        "campaign_template": "TestTemplate",
        "recipient_category": "vendors",
        "template_name": "Admin_Template"
    },
    "null_name": {
        "send_time": (datetime.utcnow()+timedelta(hours=5)).isoformat(),
        "campaign_template": "TestTemplate",
        "recipient_category": "vendors",
        "template_name": "Admin_Template"
    },
    "long_name": {
        "name": ("a" * 21)+str(datetime.utcnow()),
        "send_time": (datetime.utcnow()+timedelta(hours=5)).isoformat(),
        "campaign_template": "TestTemplate",
        "recipient_category": "vendors",
        "template_name": "Admin_Template"
    },
    "null_send_time": {
        "name": "TestCampaign"+str(datetime.utcnow()),
        "campaign_template": "TestTemplate",
        "recipient_category": "vendors",
        "template_name": "Admin_Template"
    },
    "past_send_time": {
        "name": "TestCampaign"+str(datetime.utcnow()),
        "send_time": (datetime.utcnow()-timedelta(hours=5)).isoformat(),
        "campaign_template": "TestTemplate",
        "recipient_category": "vendors",
        "template_name": "Admin_Template"
    },
    "null_template_name": {
        "name": "TestCampaign"+str(datetime.utcnow()),
        "send_time": (datetime.utcnow()+timedelta(hours=5)).isoformat(),
        "campaign_template": "TestTemplate",
        "recipient_category": "vendors"
    },
    "null_recipient_category": {
        "name": "TestCampaign"+str(datetime.utcnow()),
        "send_time": (datetime.utcnow()+timedelta(hours=5)).isoformat(),
        "campaign_template": "TestTemplate",
        "template_name": "Admin_Template"
    }
}

# Required fields for campaigns
REQUIRED_FIELDS_CAMPAIGN = ["name", "send_time", "campaign_template", "recipient_category", "template_name"]

# Expected messages for campaigns
EXPECTED_MESSAGES_CAMPAIGN = {
    "duplicate_name": {
        "error": "Duplicate entry",
        "message": "A campaign with this name already exists."
    },
    "invalid_name_format": {
        "error": "Invalid input",
        "message": "Campaign name should not contain special characters."
    },
    "name_required": {
        "error": "Invalid input",
        "message": "Campaign name is required."
    },
    "name_too_long": {
        "error": "Invalid input",
        "message": "Campaign name should not exceed 20 characters."
    },
    "send_time_required": {
        "error": "Invalid input",
        "message": "Send time is required."
    },
    "past_send_time": {
        'error': 'Send time must be in the future'
    },
    "template_name_required": {
        "error": "Invalid input",
        "message": "Template name is required."
    },
    "recipient_category_required": {'error': 'Campaign name already exists'}
}

unique_tag = str(time.time()).split(".")[0]
category_name = "automation"+str(time.time())
CONFIG = {
    "recipient_category": {
        "category_name": category_name
    },
    "members": [
        {"name": "Alice", "email": f"{unique_tag}_bot@example.com", "recipient_category": category_name},
        {"name": "Bob", "email": f"{unique_tag}_auto@example.com", "recipient_category": category_name},
        {"name": "Charlie", "email": f"{unique_tag}_hybrid@example.com", "recipient_category": category_name}
    ],
    "email_template": {
        "name": "at"+unique_tag,
        "content": f"Hello {unique_tag} How are You"
    },
    "campaign": {
        "name": "TestCampaign"+unique_tag,
        "send_time": (datetime.utcnow() + timedelta(hours=5)).isoformat(),
        "campaign_template": f"Hello {unique_tag} How are You",
        "recipient_category": category_name,
        "template_name": "at"+unique_tag
    }
}


def campaign_patch_data_generator(recipient_category, email_template):
    unique_tag = str(time.time()).split(".")[0]
    update_data = {
        "name": "UC" + unique_tag,
        "send_time": (datetime.utcnow() + timedelta(hours=10)).isoformat(),
        "campaign_template": "camptemp" + unique_tag,
        "recipient_category": recipient_category,
        # Assuming recipient category is a dictionary
        "template_name": email_template  # Assuming email template is a dictionary
    }
    return update_data
