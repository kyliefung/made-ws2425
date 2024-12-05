import os
import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import kagglehub

# Global configurations
DATA_DIR = "./data"
KAGGLE_DATA_PATH = kagglehub.dataset_download("masakii/fbi-nics-firearm-background-checks")
KAGGLE_OUTPUT_FILE = "cleaned_kaggle_dataset.sqlite"
CDC_OUTPUT_FILE = "cleaned_cdc_dataset.sqlite"

# Function to create directories if they do not exist
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Kaggle data pipeline
def kaggle_pipeline():
    def load_dataset(path):
        for file in os.listdir(path):
            if file.endswith(".csv"):
                return pd.read_csv(os.path.join(path, file))
        raise FileNotFoundError("No CSV file found in Kaggle dataset directory.")

    def transform_kaggle_data(df):
        states_to_keep = ['california', 'new york', 'massachusetts', 'texas', 'wyoming', 'alaska']
        df = df[df['state'].str.strip().str.lower().isin(states_to_keep)]
        df['year'] = pd.to_datetime(df['month']).dt.year
        df = df.groupby(['year', 'state']).sum(numeric_only=True).reset_index()
        columns_to_keep = [
            "year", "state", "permit", "permit_recheck", "handgun", "long_gun", 
            "multiple", "redemption_handgun", "redemption_long_gun", 
            "private_sale_handgun", "private_sale_long_gun", 
            "return_to_seller_handgun", "return_to_seller_long_gun", "totals"
        ]
        df = df[columns_to_keep]
        for col in columns_to_keep[2:]:
            df[col] = df[col].astype(int)
        return df

    def save_to_sqlite(df, output_file):
        conn = sqlite3.connect(os.path.join(DATA_DIR, output_file))
        df.to_sql("kaggle_data", conn, if_exists="replace", index=False)
        conn.close()

    print("Processing Kaggle dataset...")
    df = load_dataset(KAGGLE_DATA_PATH)
    transformed_df = transform_kaggle_data(df)
    save_to_sqlite(transformed_df, KAGGLE_OUTPUT_FILE)
    print(f"Kaggle data saved to {os.path.join(DATA_DIR, KAGGLE_OUTPUT_FILE)}.")

# CDC data pipeline
def cdc_pipeline():
    def download_csv():
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": os.path.abspath(DATA_DIR)}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=service, options=options)
        try:
            url = "https://www.cdc.gov/nchs/pressroom/sosmap/firearm_mortality/firearm.htm"
            driver.get(url)
            download_button = driver.find_element(By.XPATH, "//a[contains(text(),'Download Data (CSV)')]")
            download_button.click()
            time.sleep(10)  # Adjust based on internet speed
        finally:
            driver.quit()

    def load_csv():
        for file in os.listdir(DATA_DIR):
            if file.endswith(".csv"):
                return pd.read_csv(os.path.join(DATA_DIR, file))
        raise FileNotFoundError("CDC CSV file not found in data directory.")

    def transform_cdc_data(df):
        states_to_keep = ["CA", "NY", "WY", "TX", "AK", "MA"]
        df = df[df['STATE'].isin(states_to_keep)]
        df = df.drop(columns=['URL'], errors='ignore')
        df['YEAR'] = pd.to_datetime(df['YEAR'], format='%Y').dt.year
        df['DEATHS'] = df['DEATHS'].replace({',': ''}, regex=True).astype(int)
        return df

    def save_to_sqlite(df, output_file):
        conn = sqlite3.connect(os.path.join(DATA_DIR, output_file))
        df.to_sql("cdc_data", conn, if_exists="replace", index=False)
        conn.close()

    print("Downloading CDC dataset...")
    download_csv()
    df = load_csv()
    transformed_df = transform_cdc_data(df)
    save_to_sqlite(transformed_df, CDC_OUTPUT_FILE)
    print(f"CDC data saved to {os.path.join(DATA_DIR, CDC_OUTPUT_FILE)}.")

# Main pipeline function
def run_pipeline():
    ensure_dir(DATA_DIR)
    kaggle_pipeline()
    cdc_pipeline()
    print("All datasets processed successfully.")

if __name__ == "__main__":
    run_pipeline()
