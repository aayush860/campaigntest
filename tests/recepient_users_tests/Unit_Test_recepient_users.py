import unittest
import pytest
import logging
from src.api_utility import get, post
from src.recipient_users_utilities.recipient_users_helper import REQUIRED_FIELDS, EXPECTED_MESSAGES

logger = logging.getLogger(__name__)


class TestRecipients(unittest.TestCase):
    @pytest.mark.recipients
    def test_01_get_recipients_success(self):
        logger.debug("Starting test_get_recipients_success")
        response = get("/api/recipients")
        self.assertEqual(response.status_code, 200)
        logger.debug("Completed test_get_recipients_success with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_02_get_recipients_fields(self):
        logger.debug("Starting test_get_recipients_fields")
        response = get("/api/recipients")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            for field in REQUIRED_FIELDS:
                self.assertIn(field, item)
        logger.debug("Completed test_get_recipients_fields with response: %s", response.json())

    @pytest.mark.recipients
    def test_03_post_recipient_success(self):
        logger.debug("Starting test_post_recipient_success")
        data = {"name": "TestName", "email": "test@example.com", "recipient_category": "TestCategory"}
        response = post("/api/recipients", data)
        self.assertEqual(response.status_code, 201)
        logger.debug("Completed test_post_recipient_success with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_04_email_unique(self):
        logger.debug("Starting test_email_unique")
        data = {"name": "TestName", "email": "unique@example.com", "recipient_category": "TestCategory"}
        response1 = post("/api/recipients", data)
        self.assertEqual(response1.status_code, 201)

        response2 = post("/api/recipients", data)
        self.assertEqual(response2.status_code, 409)
        self.assertEqual(response2.json(), EXPECTED_MESSAGES["duplicate_email"])
        logger.debug("Completed test_email_unique with status code: %s", response2.status_code)

    @pytest.mark.recipients
    @pytest.mark.xfail(reason="Expected to fail as special characters are not handled by Mock APIs")
    def test_05_email_no_special_characters(self):
        logger.debug("Starting test_email_no_special_characters")
        data = {"name": "TestName", "email": "special@#%$.com", "recipient_category": "TestCategory"}
        response = post("/api/recipients", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES["invalid_email_format"])
        logger.debug("Completed test_email_no_special_characters with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_06_email_not_null(self):
        logger.debug("Starting test_email_not_null")
        data = {"name": "TestName", "email": "", "recipient_category": "TestCategory"}
        response = post("/api/recipients", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES["email_required"])
        logger.debug("Completed test_email_not_null with status code: %s", response.status_code)

    @pytest.mark.recipients
    @pytest.mark.xfail(reason="Expected to fail as email structure is not handled by Mock APIs")
    def test_07_email_structure(self):
        logger.debug("Starting test_email_structure")
        data = {"name": "TestName", "email": "invalid-email", "recipient_category": "TestCategory"}
        response = post("/api/recipients", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES["invalid_email_format"])
        logger.debug("Completed test_email_structure with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_08_name_max_length(self):
        logger.debug("Starting test_name_max_length")
        long_name = "a" * 33
        data = {"name": long_name, "email": "test@example.com", "recipient_category": "TestCategory"}
        response = post("/api/recipients", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES["name_too_long"])
        logger.debug("Completed test_name_max_length with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_09_recipient_category_not_null(self):
        logger.debug("Starting test_recipient_category_not_null")
        data = {"name": "TestName", "email": "test@example.com", "recipient_category": ""}
        response = post("/api/recipients", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES["recipient_category_required"])
        logger.debug("Completed test_recipient_category_not_null with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_10_get_recipient_category_success(self):
        logger.debug("Starting test_get_recipient_category_success")
        response = get("/api/recipients/TestCategory")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            for field in REQUIRED_FIELDS:
                self.assertIn(field, item)
        logger.debug("Completed test_get_recipient_category_success with response: %s", response.json())

    @pytest.mark.recipients
    def test_11_get_recipient_category_not_found(self):
        logger.debug("Starting test_get_recipient_category_not_found")
        response = get("/api/recipients/NonExistingCategory")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), EXPECTED_MESSAGES["no_recipients_found"])
        logger.debug("Completed test_get_recipient_category_not_found with status code: %s", response.status_code)

    @pytest.mark.recipients
    def test_12_get_recipient_category_specific(self):
        logger.debug("Starting test_get_recipient_category_specific")
        category = "TestCategory"
        response = get(f"/api/recipients/{category}")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            self.assertEqual(item['recipient_category'], category)
        logger.debug("Completed test_get_recipient_category_specific with response: %s", response.json())


#pytest /Users/aabharga/Downloads/campaigntest/tests/recepient_users_tests/Unit_Test_recepient_users.py --html=report.html
if __name__ == '__main__':
    unittest.main()
