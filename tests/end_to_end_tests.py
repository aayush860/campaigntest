import unittest
import pytest
from integration_tests import TestIntegration
from src.api_utility import post, delete, put, patch
from src.campaigns_utilities.campaigns_helper import CONFIG, campaign_patch_data_generator


class TestCampaignEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create recipient category and members
        cls.integration = TestIntegration()
        cls.recipient_category = cls.integration.test_create_recipient_category()
        cls.members = cls.integration.test_create_members()
        cls.email_template = cls.integration.test_create_email_template()
        cls.data = CONFIG['campaign'].copy()
        cls.data['recipient_category'] = cls.recipient_category
        cls.data["template_name"] = cls.email_template

    @pytest.mark.end_to_end
    def test_01_create_campaign_and_verify_scheduled(self):
        # Create a new campaign
        response = post("/api/campaigns", self.data)

        # Assert status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Verify campaign fields
        campaign_data = response.json()
        for field in self.data:
            self.assertEqual(campaign_data[field], self.data[field])

        # Verify campaign status is 'Scheduled'
        self.assertEqual(campaign_data['status'], 'Scheduled')

    @pytest.mark.end_to_end
    def test_02_cancel_campaign_and_verify_cancelled(self):
        response = post("/api/campaigns", self.data)
        self.assertEqual(response.status_code, 201)

        campaign_name = response.json()['name']
        delete_response = delete(f"/api/campaigns/delete?name={campaign_name}")
        message = delete_response.json()['message']
        self.assertEqual(message, f'Campaign "{campaign_name}" has been cancelled')

    @pytest.mark.end_to_end
    def test_03_update_campaign_and_verify_updated(self):
        # Create a new campaign
        response = post("/api/campaigns", self.data)
        self.assertEqual(response.status_code, 201)

        # Get the campaign ID
        campaign_name = response.json()['name']

        # Update campaign details
        update_data = campaign_patch_data_generator(recipient_category=self.recipient_category,
                                                    email_template=self.email_template)
        response = put(f"/api/campaigns/{campaign_name}", update_data)
        self.assertEqual(response.status_code, 200)

        # Verify updated fields
        updated_campaign = response.json()
        for field in update_data:
            self.assertEqual(updated_campaign[field], update_data[field])

    @pytest.mark.end_to_end
    def test_04_update_fields_in_campaign_and_verify_updated(self):
        # Create a new campaign
        response = post("/api/campaigns", self.data)
        self.assertEqual(response.status_code, 201)

        # Get the campaign name
        campaign_name = response.json()['name']

        # Update 2-3 fields in campaign
        update_data = campaign_patch_data_generator(recipient_category=self.recipient_category,
                                                    email_template=self.email_template)
        filtered_data = {
            "campaign_template": update_data["campaign_template"],
            "send_time": update_data["send_time"]
        }
        response = patch(f"/api/campaigns/{campaign_name}", filtered_data)
        self.assertEqual(response.status_code, 200)

        # Verify updated fields
        campaign_data = response.json()
        for field in filtered_data:
            self.assertEqual(campaign_data[field], update_data[field])


#pytest /Users/aabharga/Downloads/campaigntest/tests/end_to_end_tests.py --html=end_to_end_report.html
if __name__ == '__main__':
    unittest.main()
