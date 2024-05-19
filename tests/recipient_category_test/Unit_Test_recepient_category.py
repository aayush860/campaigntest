import unittest
import pytest
import logging
from src.api_utility import get, post
from src.recipient_category_utilities.recipient_category_helper import REQUIRED_FIELDS, EXPECTED_MESSAGES

logger = logging.getLogger(__name__)


class TestRecipientCategory(unittest.TestCase):

    @pytest.mark.recipient_category
    def test_01_get_recipient_lists_success(self):
        logger.debug("Starting test_get_recipient_lists_success")
        response = get("/api/recipient_lists")
        self.assertEqual(response.status_code, 200)
        logger.debug("Completed test_get_recipient_lists_success with status code: %s", response.status_code)

    @pytest.mark.recipient_category
    def test_02_get_recipient_lists_fields(self):
        logger.debug("Starting test_get_recipient_lists_fields")
        response = get("/api/recipient_lists")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            for field in REQUIRED_FIELDS:
                self.assertIn(field, item)
        logger.debug("Completed test_get_recipient_lists_fields with response: %s", response.json())

    @pytest.mark.recipient_category
    def test_03_post_recipient_list_success(self):
        logger.debug("Starting test_post_recipient_list_success")
        data = {"recipient_category": "TestList", "description": "I am automated testlist"}
        response = post("/api/recipient_lists", data)
        self.assertEqual(response.status_code, 201)
        logger.debug("Completed test_post_recipient_list_success with status code: %s", response.status_code)

    @pytest.mark.recipient_category
    def test_04_recipient_category_unique(self):
        logger.debug("Starting test_recipient_category_unique")
        data = {"recipient_category": "uniqueCat", "description": "I am automated unique category test"}
        response1 = post("/api/recipient_lists", data)
        self.assertEqual(response1.status_code, 201)

        response2 = post("/api/recipient_lists", data)
        self.assertEqual(response2.status_code, 409)  # Assuming 400 Bad Request for duplicate
        self.assertEqual(response2.json(), EXPECTED_MESSAGES["duplicate_entry"])
        logger.debug("Completed test_recipient_category_unique with status code: %s", response2.status_code)

    @pytest.mark.recipient_category
    @pytest.mark.xfail(reason="Expected to fail as special character is not handled by Mock APIs")
    def test_05_recipient_category_no_special_characters(self):
        logger.debug("Starting test_recipient_category_no_special_characters")
        data = {"recipient_category": "specialCat#@%$", "description": "I am automated special category test"}
        response = post("/api/recipient_lists", data)
        self.assertEqual(response.status_code, 400)  # Assuming 400 Bad Request for invalid name
        logger.debug("Completed test_recipient_category_no_special_characters with status code: %s", response.status_code)

    @pytest.mark.recipient_category
    def test_06_recipient_category_not_null(self):
        logger.debug("Starting test_recipient_category_not_null")
        data = {"recipient_category": "", "description": "I am automated null category test"}
        response = post("/api/recipient_lists", data)
        self.assertEqual(response.status_code, 400)  # Assuming 400 Bad Request for null name
        self.assertEqual(response.json(), EXPECTED_MESSAGES["invalid_input"])
        logger.debug("Completed test_recipient_category_not_null with status code: %s", response.status_code)

    @pytest.mark.recipient_category
    @pytest.mark.skip(reason="Skipping this test as further development is required")
    def test_07_recipient_category_max_length(self):
        logger.debug("Starting test_recipient_category_max_length")
        long_name = {"recipient_category": "a"*40, "description": "I am automated max length category test"}
        data = {"name": long_name}
        response = post("/api/recipient_lists", data)
        self.assertEqual(response.status_code, 400)  # Assuming 400 Bad Request for name too long
        logger.debug("Completed test_recipient_category_max_length with status code: %s", response.status_code)


#pytest /Users/aabharga/Downloads/campaigntest/tests/recipient_category_test/Unit_Test_recepient_category.py --html=report.html
if __name__ == '__main__':
    unittest.main()

