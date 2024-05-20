import pytest
import pandas as pd
from unittest import mock
from unittest.mock import patch
from src.example_package.gui.app import ShowParticipants


data = {
    'name': ['John', 'Alice', 'Michael', 'Emma', 'James', 'Olivia'],
    'surname': ['Doe', 'Smith', 'Johnson', 'Brown', 'Williams', 'Jones'],
    'age_category': ['Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Women'],
    'age': [15, 18, 15, 14, 17, 15],
    'weight_category': ['Light-weight', 'Middle-weight', 'Light-weight', 'Heavy-weight', 'Middle-weight', 'Heavy-weight'],
    'weight': [70, 90, 75, 110, 85, 90],
    'country': ['USA', 'Canada', 'UK', 'USA', 'USA', 'UK']
}

PARTICIPANTS_DATA = pd.DataFrame(data)


class TestShowParticipants:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.participants_data = PARTICIPANTS_DATA
        self.show_participants = ShowParticipants(self.participants_data)

    def test_init_headers(self):
        assert self.show_participants.headers == ['Profile', 'Name', 'Surname', 'Age Category', 'Age', 'Weight Category', 'Weight', 'Country']

    def test_init_filtering_keys(self):
        assert self.show_participants.text_filter_keys == ['name', 'surname', 'age_category', 'weight_category', 'country']

    def test_add_numeric_filter_range(self):
        age_input_range = self.show_participants.add_numeric_filter_range('age')
        min_val = self.show_participants.numeric_data_info['age']['constraints'][0]
        max_val = 100000
        assert isinstance(age_input_range, list)
        assert len(age_input_range) == 2
        assert age_input_range == [min_val, max_val]

    def test_get_filter_inputs_no_filters(self):
        filter_inputs = self.show_participants.get_filter_inputs()
        assert isinstance(filter_inputs, list)
        assert len(filter_inputs) == 0

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_no_filters(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        original_participants_data = self.show_participants.participants_data

        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        assert len(self.show_participants.filtered_data) == len(original_participants_data)
        assert self.show_participants.filtered_data.equals(original_participants_data)

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_age_range_lower_value(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '18', '25', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        age_min = int(self.show_participants.text_inputs[3])
        age_max = int(self.show_participants.text_inputs[4])

        mock_add_participant_labels.assert_called_once_with(
            mock.ANY,
            mock.ANY
        )

        assert len(self.show_participants.filtered_data) == 1
        assert self.show_participants.filtered_data['age'].min() >= age_min
        assert self.show_participants.filtered_data['age'].max() <= age_max

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_age_range_upper_value(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '0', '14', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        age_min = int(self.show_participants.text_inputs[3])
        age_max = int(self.show_participants.text_inputs[4])

        mock_add_participant_labels.assert_called_once_with(
            mock.ANY,
            mock.ANY
        )

        assert len(self.show_participants.filtered_data) == 1
        assert self.show_participants.filtered_data['age'].min() >= age_min
        assert self.show_participants.filtered_data['age'].max() <= age_max

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_weight_range_lower_value(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', '', '100', '250', '']
        ):
            self.show_participants.apply_filters()

        weight_min = int(self.show_participants.text_inputs[6])
        weight_max = int(self.show_participants.text_inputs[7])

        mock_add_participant_labels.assert_called_once_with(
            mock.ANY,
            mock.ANY
        )

        assert len(self.show_participants.filtered_data) == 1
        assert self.show_participants.filtered_data['weight'].min() >= weight_min
        assert self.show_participants.filtered_data['weight'].max() <= weight_max

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_weight_range_upper_value(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', '', '50', '70', '']
        ):
            self.show_participants.apply_filters()

        weight_min = int(self.show_participants.text_inputs[6])
        weight_max = int(self.show_participants.text_inputs[7])

        mock_add_participant_labels.assert_called_once_with(
            mock.ANY,
            mock.ANY
        )

        assert len(self.show_participants.filtered_data) == 1
        assert self.show_participants.filtered_data['weight'].min() >= weight_min
        assert self.show_participants.filtered_data['weight'].max() <= weight_max

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_age_weight(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '18', '24', '', '80', '120', '']
        ):
            self.show_participants.apply_filters()

        age_min = int(self.show_participants.text_inputs[3])
        age_max = int(self.show_participants.text_inputs[4])
        weight_min = int(self.show_participants.text_inputs[6])
        weight_max = int(self.show_participants.text_inputs[7])

        mock_add_participant_labels.assert_called_once_with(
            mock.ANY,
            mock.ANY
        )

        assert len(self.show_participants.filtered_data) == 1
        assert self.show_participants.filtered_data['weight'].min() >= weight_min and \
        self.show_participants.filtered_data['age'].min() >= age_min
        assert self.show_participants.filtered_data['weight'].max() <= weight_max and \
        self.show_participants.filtered_data['age'].max() <= age_max

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_negative_numeric_value(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', '', '-100', '70', '']
        ):
            self.show_participants.apply_filters()

        weight_min = int(self.show_participants.text_inputs[6])
        weight_max = int(self.show_participants.text_inputs[7])

        mock_add_participant_labels.assert_called_once_with(
            mock.ANY,
            mock.ANY
        )

        assert len(self.show_participants.filtered_data) == 1
        assert self.show_participants.filtered_data['weight'].min() >= weight_min
        assert self.show_participants.filtered_data['weight'].max() <= weight_max

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_name(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['John', '', '', '', '', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        filtered_names = self.show_participants.filtered_data['name'].tolist()
        expected_names = ['John']
        
        assert len(self.show_participants.filtered_data) == len(expected_names)
        assert filtered_names == expected_names

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_surname(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', 'Doe', '', '', '', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        filtered_surnames = self.show_participants.filtered_data['surname'].tolist()
        expected_surnames = ['Doe']
        
        assert len(self.show_participants.filtered_data) == len(expected_surnames)
        assert filtered_surnames == expected_surnames

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_age_category(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', 'Jr. Men', '', '', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        filtered_age_categories = self.show_participants.filtered_data['age_category'].tolist()
        expected_age_categories = ['Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Men']
        
        assert len(self.show_participants.filtered_data) == len(expected_age_categories)
        assert filtered_age_categories == expected_age_categories

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_age_category_prefix_search(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', 'en', '', '', '', '', '', '']
        ):
            self.show_participants.apply_filters()

        filtered_age_categories = self.show_participants.filtered_data['age_category'].tolist()
        expected_age_categories = ['Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Men', 'Jr. Women']
        
        assert len(self.show_participants.filtered_data) == len(expected_age_categories)
        assert filtered_age_categories == expected_age_categories

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_weight_category(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', 'Light-weight', '', '', '']
        ):
            self.show_participants.apply_filters()

        filtered_weight_categories = self.show_participants.filtered_data['weight_category'].tolist()
        expected_weight_categories = ['Light-weight', 'Light-weight']
        
        assert len(self.show_participants.filtered_data) == len(expected_weight_categories)
        assert filtered_weight_categories == expected_weight_categories

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_weight_category_prefix_search(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', 'Mid', '', '', '']
        ):
            self.show_participants.apply_filters()

        filtered_weight_categories = self.show_participants.filtered_data['weight_category'].tolist()
        expected_weight_categories = ['Middle-weight', 'Middle-weight']
        
        assert len(self.show_participants.filtered_data) == len(expected_weight_categories)
        assert filtered_weight_categories == expected_weight_categories

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_country(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', '', '', '', 'USA']
        ):
            self.show_participants.apply_filters()

        filtered_countries = self.show_participants.filtered_data['country'].tolist()
        expected_countries = ['USA', 'USA', 'USA']
        
        assert len(self.show_participants.filtered_data) == len(expected_countries)
        assert filtered_countries == expected_countries

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_country_prefix_search(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None
        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['', '', '', '', '', '', '', '', 'U']
        ):
            self.show_participants.apply_filters()

        filtered_countries = self.show_participants.filtered_data['country'].tolist()
        expected_countries = ['USA', 'UK', 'USA', 'USA', 'UK']
        
        assert len(self.show_participants.filtered_data) == len(expected_countries)
        assert filtered_countries == expected_countries

    @patch('example_package.gui.app.ShowParticipants.add_participant_labels')
    def test_apply_filters_specific_participant(self, mock_add_participant_labels):
        mock_add_participant_labels.return_value = None

        wrestler_data = {
        'name': 'John',
        'surname': 'Doe',
        'age_category': 'Jr. Men',
        'age': 15,
        'weight_category': 'Light-weight',
        'weight': 70,
        'country': 'USA'
        }
    
        specific_wrestler = PARTICIPANTS_DATA[
            (PARTICIPANTS_DATA['name'] == wrestler_data['name']) &
            (PARTICIPANTS_DATA['surname'] == wrestler_data['surname']) &
            (PARTICIPANTS_DATA['age_category'] == wrestler_data['age_category']) &
            (PARTICIPANTS_DATA['age'] == wrestler_data['age']) &
            (PARTICIPANTS_DATA['weight_category'] == wrestler_data['weight_category']) &
            (PARTICIPANTS_DATA['weight'] == wrestler_data['weight']) &
            (PARTICIPANTS_DATA['country'] == wrestler_data['country'])
        ]

        with patch.object(
                self.show_participants,
                'get_filter_inputs',
                return_value=['John', 'Doe', 'Jr. Men', '15', '15', 'Light-weight', '70', '70', 'USA']
        ):
            self.show_participants.apply_filters()
        
        mock_add_participant_labels.assert_called_once_with(
        mock.ANY,
        mock.ANY
        )

        assert len(self.show_participants.filtered_data) == len(specific_wrestler)

        assert self.show_participants.filtered_data.iloc[0]['name'] == wrestler_data['name']
        assert self.show_participants.filtered_data.iloc[0]['surname'] == wrestler_data['surname']
        assert self.show_participants.filtered_data.iloc[0]['age_category'] == wrestler_data['age_category']
        assert self.show_participants.filtered_data.iloc[0]['age'] == wrestler_data['age']
        assert self.show_participants.filtered_data.iloc[0]['weight_category'] == wrestler_data['weight_category']
        assert self.show_participants.filtered_data.iloc[0]['weight'] == wrestler_data['weight']
        assert self.show_participants.filtered_data.iloc[0]['country'] == wrestler_data['country']
