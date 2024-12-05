import unittest
import pandas as pd
from io import StringIO
from project.pipeline import transform_kaggle_data, transform_cdc_data

class TestTransformFunctions(unittest.TestCase):

    def test_transform_kaggle_data(self):
        # Sample Kaggle input data
        kaggle_csv = StringIO("""
        month,state,permit,permit_recheck,handgun,long_gun,multiple,redemption_handgun,redemption_long_gun,private_sale_handgun,private_sale_long_gun,return_to_seller_handgun,return_to_seller_long_gun,totals
        2020-01,California,100,5,200,150,10,50,40,5,10,3,2,575
        2020-02,New York,80,3,180,120,15,60,50,10,15,2,1,536
        2020-01,Texas,90,4,150,140,20,55,45,6,12,3,1,526
        2020-02,Wyoming,30,1,50,60,5,20,15,2,4,1,0,188
        2020-01,Florida,120,6,250,220,25,70,60,8,20,4,2,785
        """)
        
        # Load sample Kaggle data into DataFrame
        df = pd.read_csv(kaggle_csv)

        # Run the transformation
        transformed_df = transform_kaggle_data(df)

        # Expected output Kaggle data
        expected_data = {
            'year': [2020, 2020, 2020, 2020],
            'state': ['california', 'new york', 'texas', 'wyoming'],
            'permit': [100, 80, 90, 30],
            'permit_recheck': [5, 3, 4, 1],
            'handgun': [200, 180, 150, 50],
            'long_gun': [150, 120, 140, 60],
            'multiple': [10, 15, 20, 5],
            'redemption_handgun': [50, 60, 55, 20],
            'redemption_long_gun': [40, 50, 45, 15],
            'private_sale_handgun': [5, 10, 6, 2],
            'private_sale_long_gun': [10, 15, 12, 4],
            'return_to_seller_handgun': [3, 2, 3, 1],
            'return_to_seller_long_gun': [2, 1, 1, 0],
            'totals': [575, 536, 526, 188]
        }
        expected_df = pd.DataFrame(expected_data)

        # Assert that the transformed Kaggle DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df.reset_index(drop=True), expected_df)

    def test_transform_cdc_data(self):
        # Sample CDC input data
        cdc_csv = StringIO("""
        YEAR,STATE,DEATHS,URL
        2020,CA,1000,some_url
        2020,NY,900,some_url
        2020,FL,1100,some_url
        2020,TX,800,some_url
        2020,WY,300,some_url
        2020,AK,200,some_url
        2020,MA,400,some_url
        """)
        
        # Load sample CDC data into DataFrame
        df = pd.read_csv(cdc_csv)

        # Run the transformation
        transformed_df = transform_cdc_data(df)

        # Expected output CDC data
        expected_data = {
            'YEAR': [2020, 2020, 2020, 2020, 2020, 2020],
            'STATE': ['CA', 'NY', 'TX', 'WY', 'AK', 'MA'],
            'DEATHS': [1000, 900, 800, 300, 200, 400]
        }
        expected_df = pd.DataFrame(expected_data)

        # Assert that the transformed CDC DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df.reset_index(drop=True), expected_df)

    def test_kaggle_data_with_missing_values(self):
        kaggle_csv = StringIO("""
        month,state,permit,permit_recheck,handgun,long_gun,multiple,redemption_handgun,redemption_long_gun,private_sale_handgun,private_sale_long_gun,return_to_seller_handgun,return_to_seller_long_gun,totals
        2020-01,California,100,5,200,150,10,50,40,5,10,3,,575
        2020-02,New York,80,3,180,120,15,60,50,10,15,2,1,536
        """)
        df = pd.read_csv(kaggle_csv)
        with self.assertRaises(ValueError):
            transform_kaggle_data(df)

    def test_cdc_data_with_invalid_year(self):
        cdc_csv = StringIO("""
        YEAR,STATE,DEATHS,URL
        invalid,CA,1000,some_url
        2020,NY,900,some_url
        """)
        df = pd.read_csv(cdc_csv)
        with self.assertRaises(ValueError):
            transform_cdc_data(df)

if __name__ == "__main__":
    unittest.main()
