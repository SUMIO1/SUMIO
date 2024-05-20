import pytest
import pandas as pd
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch
from src.example_package.gui.app import ProfileButton, WrestlerProfile, WrestlerSelectedStatus
from src.example_package.gui.ParticipantsManager import ParticipantsManager


@pytest.fixture
def mock_wrestler_data():
    return pd.Series({
        'name': 'John',
        'surname': 'Doe',
        'age_category': 'Jr. Men',
        'age': 18,
        'date_of_birth': '2006-01-01',
        'weight_category': 'Middle-weight',
        'weight': 80,
        'country': 'USA'
    })


class TestProfileButton:
    @pytest.fixture(autouse=True)
    def setup(self, mock_wrestler_data):
        self.mock_main_screen = MagicMock()
        self.profile_button = ProfileButton(mock_wrestler_data, self.mock_main_screen)

    def test_on_press(self, mock_wrestler_data):
        self.profile_button.on_press()
        self.mock_main_screen.update_content_and_show_wrestler.assert_called_once_with(mock_wrestler_data)


data_profile = {
    'name': ['Alice'],
    'surname': ['Smith'],
    'age_category': ['Jr. Women'],
    'date_of_birth': ['2006-01-01'],
    'age': [18],
    'weight_category': ['Middle-weight'],
    'weight': [90],
    'country': ['Canada']
}

df = pd.DataFrame(data_profile)
TEST_DATA_PROFILE = df.iloc[0]


class MockLabel:
    def __init__(self):
        self.text = ''
        self.bind_mock = Mock()

    def bind(self, **kwargs):
        return self.bind_mock(**kwargs)


class TestWrestlerProfile(TestCase):

    def setUp(self):
        self.participants = ParticipantsManager()
        self.wrestler_status = self.participants.is_selected(TEST_DATA_PROFILE)

        self.mock_ids = {
            'name_surname': MockLabel(),
            'age_category': MockLabel(),
            'date_of_birth': MockLabel(),
            'age': MockLabel(),
            'weight_category': MockLabel(),
            'weight': MockLabel(),
            'country': MockLabel(),
            'image': MockLabel(),
            'btn_edit_profile': MockLabel(),
            'btn_add_to_tournament': MockLabel()
        }

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_name_surname(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Participant: Alice Smith"

        assert wrestler_profile.ids['name_surname'].text == expected_text

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_age_category(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Age Category: Jr. Women"

        assert wrestler_profile.ids['age_category'].text == expected_text

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_date_of_birth(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Date of Birth: 2006-01-01"

        assert wrestler_profile.ids['date_of_birth'].text == expected_text

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_age(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Age: 18"

        assert wrestler_profile.ids['age'].text == expected_text

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_weight_category(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Weight: Middle-weight"

        assert wrestler_profile.ids['weight_category'].text == expected_text

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_weight(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Weight: 90 kg"

        assert wrestler_profile.ids['weight'].text == expected_text

    @patch.object(WrestlerProfile, 'ids', new_callable=lambda: {})
    def test_wrestler_profile_country(self, mock_ids):
        mock_ids.update(self.mock_ids)
        wrestler_profile = WrestlerProfile(TEST_DATA_PROFILE, self.wrestler_status, self.participants)
        expected_text = "Country: Canada"

        assert wrestler_profile.ids['country'].text == expected_text


class TestWrestlerSelectedStatus(TestCase):

    def test_initialization_selected(self):
        status = WrestlerSelectedStatus(True)
        self.assertTrue(status.selected)
        self.assertEqual(status.participation_message, "THIS PARTICIPANT IS SELECTED FOR THE TOURNAMENT")

    def test_initialization_not_selected(self):
        status = WrestlerSelectedStatus(False)
        self.assertFalse(status.selected)
        self.assertEqual(status.participation_message, "THIS PARTICIPANT IS [b]NOT[/b] SELECTED FOR THE TOURNAMENT")
