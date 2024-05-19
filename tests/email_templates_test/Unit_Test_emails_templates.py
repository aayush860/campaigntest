import unittest
import pytest
import logging
from src.api_utility import get, post
from src.email_templates_utilities.email_template_helper import REQUIRED_FIELDS_TEMPLATE, EXPECTED_MESSAGES_TEMPLATE

logger = logging.getLogger(__name__)


class TestEmailTemplates(unittest.TestCase):

    @pytest.mark.email_templates
    def test_01_get_templates_success(self):
        logger.debug("Starting test_get_templates_success")
        response = get("/api/email_templates")
        self.assertEqual(response.status_code, 200)
        logger.debug("Completed test_get_templates_success with status code: %s", response.status_code)

    @pytest.mark.email_templates
    def test_02_get_templates_fields(self):
        logger.debug("Starting test_get_templates_fields")
        response = get("/api/email_templates")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            for field in REQUIRED_FIELDS_TEMPLATE:
                self.assertIn(field, item)
        logger.debug("Completed test_get_templates_fields with response: %s", response.json())

    @pytest.mark.email_templates
    def test_03_post_template_success(self):
        logger.debug("Starting test_post_template_success")
        data = {"name": "TestTemplate", "content": "Test content"}
        response = post("/api/email_templates", data)
        self.assertEqual(response.status_code, 201)
        logger.debug("Completed test_post_template_success with status code: %s", response.status_code)

    @pytest.mark.email_templates
    def test_04_template_name_unique(self):
        logger.debug("Starting test_template_name_unique")
        data = {"name": "UniqueTemplate", "content": "Test content"}
        response1 = post("/api/email_templates", data)
        self.assertEqual(response1.status_code, 201)

        response2 = post("/api/email_templates", data)
        self.assertEqual(response2.status_code, 409)
        self.assertEqual(response2.json(), EXPECTED_MESSAGES_TEMPLATE["duplicate_name"])
        logger.debug("Completed test_template_name_unique with status code: %s", response2.status_code)

    @pytest.mark.email_templates
    @pytest.mark.xfail(reason="Expected to fail as special characters are not handled by Mock APIs")
    def test_05_template_name_no_special_characters(self):
        logger.debug("Starting test_template_name_no_special_characters")
        data = {"name": "Special@Name", "content": "Test content"}
        response = post("/api/email_templates", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_TEMPLATE["invalid_name_format"])
        logger.debug("Completed test_template_name_no_special_characters with status code: %s", response.status_code)

    @pytest.mark.email_templates
    def test_06_template_name_not_null(self):
        logger.debug("Starting test_template_name_not_null")
        data = {"name": "", "content": "Test content"}
        response = post("/api/email_templates", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_TEMPLATE["name_required"])
        logger.debug("Completed test_template_name_not_null with status code: %s", response.status_code)

    @pytest.mark.email_templates
    def test_07_template_name_max_length(self):
        logger.debug("Starting test_template_name_max_length")
        long_name = "a" * 21
        data = {"name": long_name, "content": "Test content"}
        response = post("/api/email_templates", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_TEMPLATE["name_too_long"])
        logger.debug("Completed test_template_name_max_length with status code: %s", response.status_code)


#pytest /Users/aabharga/Downloads/campaigntest/tests/email_templates_test/Unit_Test_emails_templates.py --html=report.html
if __name__ == '__main__':
    unittest.main()
