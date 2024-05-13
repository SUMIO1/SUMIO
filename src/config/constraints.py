from typing import Any, Dict


CONSTRAINTS: Dict[str, Any] = {
    "required_columns": ['name', 'surname', 'age_category', 'date_of_birth', 'weight_category', 'weight', 'country', 'image_url'],
    "age_categories": {
        "Jr. Men": {
            "min_age": 13,
            "max_age": 18,
            "Light-weight": {
                "min": 0,
                "max": 80
            },
            "Middle-weight": {
                "min": 80,
                "max": 100
            },
            "Heavy-weight": {
                "min": 100,
                "max": 200
            },
            "Open-weight": None
        },
        "Jr. Women": {
            "min_age": 13,
            "max_age": 18,
            "Light-weight": {
                "min": 0,
                "max": 60
            },
            "Middle-weight": {
                "min": 60,
                "max": 75
            },
            "Heavy-weight": {
                "min": 75,
                "max": 200
            },
            "Open-weight": None
        },
        "Men": {
            "min_age": 19,
            "max_age": 100,
            "Light-weight": {
                "min": 0,
                "max": 85
            },
            "Middle-weight": {
                "min": 85,
                "max": 115
            },
            "Light Heavyweight": {
                "min": 100,
                "max": 115
            },
            "Heavy-weight": {
                "min": 115,
                "max": 200
            },
            "Open-weight": None
        },
        "Women": {
            "min_age": 19,
            "max_age": 100,
            "Light-weight": {
                "min": 0,
                "max": 65
            },
            "Middle-weight": {
                "min": 65,
                "max": 73
            },
            "Light Heavyweight": {
                "min": 73,
                "max": 80
            },
            "Heavy-weight": {
                "min": 80,
                "max": 200
            },
            "Open-weight": None
        }
    }
}
