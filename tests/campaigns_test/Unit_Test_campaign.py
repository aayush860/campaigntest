import json
import unittest
import pytest
import logging
from datetime import datetime, timedelta
from src.api_utility import get, post
from src.campaigns_utilities.campaigns_helper import TEST_DATA_CAMPAIGN, REQUIRED_FIELDS_CAMPAIGN, EXPECTED_MESSAGES_CAMPAIGN

logger = logging.getLogger(__name__)

class TestCampaigns(unittest.TestCase):

    @pytest.mark.campaigns
    def test_01_get_campaigns_success(self):
        logger.debug("Starting test_get_campaigns_success")
        response = get("/api/campaigns")
        self.assertEqual(response.status_code, 200)
        logger.debug("Completed test_get_campaigns_success with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_02_get_campaigns_fields(self):
        logger.debug("Starting test_get_campaigns_fields")
        response = get("/api/campaigns")
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            for field in REQUIRED_FIELDS_CAMPAIGN:
                self.assertIn(field, item)
        logger.debug("Completed test_get_campaigns_fields with response: %s", response.json())

    @pytest.mark.campaigns
    def test_03_post_campaign_success(self):
        logger.debug("Starting test_post_campaign_success")
        data = TEST_DATA_CAMPAIGN["valid_post_data"].copy()
        response = post("/api/campaigns", data)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        logger.debug("Completed test_post_campaign_success with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_04_campaign_name_unique(self):
        logger.debug("Starting test_campaign_name_unique")
        data = TEST_DATA_CAMPAIGN["valid_post_data"]
        response1 = post("/api/campaigns", data)
        self.assertEqual(response1.status_code, 201)

        response2 = post("/api/campaigns", data)
        self.assertEqual(response2.status_code, 409)
        self.assertEqual(response2.json(), EXPECTED_MESSAGES_CAMPAIGN["duplicate_name"])
        logger.debug("Completed test_campaign_name_unique with status code: %s", response2.status_code)

    @pytest.mark.campaigns
    @pytest.mark.xfail(reason="Expected to fail as special characters are not handled by Mock APIs")
    def test_05_campaign_name_no_special_characters(self):
        logger.debug("Starting test_campaign_name_no_special_characters")
        data = TEST_DATA_CAMPAIGN["special_character_name"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["invalid_name_format"])
        logger.debug("Completed test_campaign_name_no_special_characters with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_06_campaign_name_not_null(self):
        logger.debug("Starting test_campaign_name_not_null")
        data = TEST_DATA_CAMPAIGN["missing_name"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["name_required"])
        logger.debug("Completed test_campaign_name_not_null with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_07_campaign_name_max_length(self):
        logger.debug("Starting test_campaign_name_max_length")
        data = TEST_DATA_CAMPAIGN["long_name"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["name_too_long"])
        logger.debug("Completed test_campaign_name_max_length with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_08_send_time_not_null(self):
        logger.debug("Starting test_send_time_not_null")
        data = TEST_DATA_CAMPAIGN["missing_send_time"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["send_time_required"])
        logger.debug("Completed test_send_time_not_null with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_09_send_time_past(self):
        logger.debug("Starting test_send_time_past")
        data = TEST_DATA_CAMPAIGN["past_send_time"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["past_send_time"])
        logger.debug("Completed test test_send_time_past with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_10_template_name_not_null(self):
        logger.debug("Starting test_template_name_not_null")
        data = TEST_DATA_CAMPAIGN["missing_template_name"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["template_name_required"])
        logger.debug("Completed test_template_name_not_null with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_11_recipient_category_not_null(self):
        logger.debug("Starting test_recipient_category_not_null")
        data = TEST_DATA_CAMPAIGN["valid_post_data"].copy()
        data["recipient_category"] = None
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), EXPECTED_MESSAGES_CAMPAIGN["recipient_category_required"])
        logger.debug("Completed test_recipient_category_not_null with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_12_status_default_scheduled(self):
        logger.debug("Starting test_status_default_scheduled")
        data = TEST_DATA_CAMPAIGN["valid_post_data"]
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "Scheduled")
        logger.debug("Completed test_status_default_scheduled with status code: %s", response.status_code)

    @pytest.mark.campaigns
    def test_13_status_passed_null(self):
        logger.debug("Starting test_status_passed_null")
        data = TEST_DATA_CAMPAIGN["valid_post_data"].copy()
        data["status"] = None
        response = post("/api/campaigns", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "Scheduled")
        logger.debug("Completed test_status_passed_null with status code: %s", response.status_code)


#pytest /Users/aabharga/Downloads/campaigntest/tests/campaigns_test/Unit_Test_campaign.py --html=report.html
if __name__ == '__main__':
    unittest.main()
