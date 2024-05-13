import pandas as pd
import pytest
import copy
from src.example_package.csv_reader.csv_reader import validateCSV, processCSV


VALID_DATA = pd.DataFrame({
    'name': ['John', 'Alice'],
    'surname': ['Doe', 'Smith'],
    'age_category': ['Jr. Men', 'Jr. Women'],
    'date_of_birth': ['2008-09-28', '2007-03-11'],
    'weight_category': ['Light-weight', 'Middle-weight'],
    'weight': [80, 70],
    'country': ['USA', 'Canada'],
    'image_url': ['https://example.com/john_doe.jpg', 'https://example.com/alice_smith.jpg']
})

WRONG_WEIGHT_CATEGORY_DATA = pd.DataFrame({
    'name': ['John', 'Alice'],
    'surname': ['Doe', 'Smith'],
    'age_category': ['Jr. Men', 'Jr. Women'],
    'date_of_birth': ['2008-09-28', '2007-03-11'],
    'weight_category': ['Light-weight', 'Middle-weight'],
    'weight': [150, 90],
    'country': ['USA', 'Canada'],
    'image_url': ['https://example.com/john_doe.jpg', 'https://example.com/alice_smith.jpg']
})


def test_validateCSV_valid_data():
    assert validateCSV(VALID_DATA) is None


def test_validateCSV_missing_column():
    MISSING_COLUMN_DATA = copy.deepcopy(VALID_DATA)
    MISSING_COLUMN_DATA.drop(columns=['weight_category'], inplace=True)
    with pytest.raises(ValueError):
        validateCSV(MISSING_COLUMN_DATA)


def test_validateCSV_wrong_column_name():
    WRONG_COLUMN_DATA = VALID_DATA
    WRONG_COLUMN_DATA.rename(columns={"country": "cntr"}, inplace=True)
    with pytest.raises(ValueError):
        validateCSV(WRONG_COLUMN_DATA)


def test_validateCSV_wrong_age_category():
    WRONG_AGE_CATEGORY_DATA = copy.deepcopy(VALID_DATA)
    WRONG_AGE_CATEGORY_DATA.loc[1, 'age_category'] = 'child'
    with pytest.raises(ValueError):
        validateCSV(WRONG_AGE_CATEGORY_DATA)


def test_validateCSV_wrong_weight_category():
    with pytest.raises(ValueError):
        validateCSV(WRONG_WEIGHT_CATEGORY_DATA)


def test_validateCSV_age_out_of_range():
    AGE_OUT_OF_RANGE_DATA = copy.deepcopy(VALID_DATA)
    AGE_OUT_OF_RANGE_DATA.loc[0, 'date_of_birth'] = '2004-09-28'
    with pytest.raises(ValueError):
        validateCSV(AGE_OUT_OF_RANGE_DATA)


def test_validateCSV_weight_out_of_range():
    WEIGHT_OUT_OF_RANGE_DATA = copy.deepcopy(VALID_DATA)
    WEIGHT_OUT_OF_RANGE_DATA.loc[0, 'weight'] = -10
    WEIGHT_OUT_OF_RANGE_DATA.loc[1, 'weight'] = 500
    with pytest.raises(ValueError):
        validateCSV(WEIGHT_OUT_OF_RANGE_DATA)


def test_processCSV():
    processCSV(VALID_DATA)
