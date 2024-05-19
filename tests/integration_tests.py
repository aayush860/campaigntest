import unittest
import logging
from src.api_utility import post
from src.campaigns_utilities.campaigns_helper import CONFIG

logger = logging.getLogger(__name__)


class TestIntegration(unittest.TestCase):
    def test_create_recipient_category(self):
        logger.debug("Starting test_create_recipient_category")
        data = {"recipient_category": CONFIG['recipient_category']['category_name'], "description": "automation test"}
        response = post("/api/recipient_lists", data)
        self.assertEqual(response.status_code, 201)
        category_data = response.json()
        self.assertEqual(category_data['recipient_category'], data['recipient_category'])
        logger.debug("Completed test_create_recipient_category with response: %s", category_data)
        return data['recipient_category']

    def test_create_members(self):
        logger.debug("Starting test_create_members")
        created_members = []
        for member in CONFIG['members']:
            response = post("/api/recipients", member)
            self.assertEqual(response.status_code, 201)
            member_data = response.json()
            for field in member:
                self.assertEqual(member_data[field], member[field])
            created_members.append(member_data)
            logger.debug("Completed test_create_member with response: %s", member_data)
        return created_members

    def test_create_email_template(self):
        logger.debug("Starting test_create_email_template")
        data = CONFIG['email_template']
        response = post("/api/email_templates", data)
        self.assertEqual(response.status_code, 201)
        template_data = response.json()
        self.assertEqual(template_data['name'], data['name'])
        self.assertEqual(template_data['content'], data['content'])
        logger.debug("Completed test_create_email_template with response: %s", template_data)
        return data['name']


if __name__ == '__main__':
    unittest.main()
