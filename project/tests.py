import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import pandas as pd
from project.Data_Pipeline import transform_kaggle_data, transform_cdc_data, kaggle_pipeline, cdc_pipeline, DATA_DIR

class TestPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure the data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def test_transform_kaggle_data(self):
    # Mock Kaggle data
        kaggle_data = {
            "month": ["2020-01", "2020-02", "2020-01", "2020-02"],
            "state": ["California", "New York", "Texas", "Wyoming"],
            "permit": [100, 80, 90, 30],
            "handgun": [200, 180, 150, 50],
            "long_gun": [150, 120, 140, 60],
            "totals": [575, 536, 526, 188],
        }
        df = pd.DataFrame(kaggle_data)

        # Transform the data
        transformed_df = transform_kaggle_data(df)

        # Expected output with all columns
        expected_data = {
            "year": [2020, 2020, 2020, 2020],
            "state": ["california", "new york", "texas", "wyoming"],  # Lowercase states
            "permit": [100, 80, 90, 30],
            "permit_recheck": [0, 0, 0, 0],
            "handgun": [200, 180, 150, 50],
            "long_gun": [150, 120, 140, 60],
            "multiple": [0, 0, 0, 0],
            "redemption_handgun": [0, 0, 0, 0],
            "redemption_long_gun": [0, 0, 0, 0],
            "private_sale_handgun": [0, 0, 0, 0],
            "private_sale_long_gun": [0, 0, 0, 0],
            "return_to_seller_handgun": [0, 0, 0, 0],
            "return_to_seller_long_gun": [0, 0, 0, 0],
            "totals": [575, 536, 526, 188],
        }
        expected_df = pd.DataFrame(expected_data)

        # Ensure the 'year' column is int64 for consistency
        expected_df["year"] = expected_df["year"].astype("int64")

        # Assert the transformation matches the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df.reset_index(drop=True), expected_df)

    def test_transform_cdc_data(self):
        # Mock CDC data
        cdc_data = {
            "YEAR": ["2020", "2020", "2020", "2020"],
            "STATE": ["CA", "NY", "TX", "WY"],
            "DEATHS": ["1,000", "900", "800", "300"],
            "URL": ["url1", "url2", "url3", "url4"],
        }
        df = pd.DataFrame(cdc_data)

        # Transform the data
        transformed_df = transform_cdc_data(df)

        # Expected output
        expected_data = {
            "YEAR": [2020, 2020, 2020, 2020],
            "STATE": ["CA", "NY", "TX", "WY"],
            "DEATHS": [1000, 900, 800, 300],
        }
        expected_df = pd.DataFrame(expected_data)

        # Assert the transformation matches the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df.reset_index(drop=True), expected_df)

    def test_kaggle_pipeline(self):
        # Run the Kaggle pipeline
        kaggle_pipeline()

        # Check if SQLite file is created
        kaggle_db_path = os.path.join(DATA_DIR, "cleaned_kaggle_dataset.sqlite")
        self.assertTrue(os.path.exists(kaggle_db_path), "Kaggle SQLite file not created.")

    def test_cdc_pipeline(self):
        # Run the CDC pipeline
        cdc_pipeline()

        # Check if SQLite file is created
        cdc_db_path = os.path.join(DATA_DIR, "cleaned_cdc_dataset.sqlite")
        self.assertTrue(os.path.exists(cdc_db_path), "CDC SQLite file not created.")

    @classmethod
    def tearDownClass(cls):
        # Clean up test-generated files
        for file in ["cleaned_kaggle_dataset.sqlite", "cleaned_cdc_dataset.sqlite"]:
            file_path = os.path.join(DATA_DIR, file)
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    unittest.main()
