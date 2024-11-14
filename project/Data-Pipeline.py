import os
import requests # type: ignore
import zipfile
import io
import pandas as pd # type: ignore
import kaggle # type: ignore
import time
from bs4 import BeautifulSoup # type: ignore
# It is used to automate the process of selecting filters and downloading data from a webpage.
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float # type: ignore

# Step 1: Extract: Extracting data - downloading from HTTP into csv file format,
# identifying and reading data from 4 data sources, csv, web and zip files
# Datasource URLs and paths
datasources = {
    "us_firearm_ownership": {
        "url": "https://www.rand.org/content/dam/rand/pubs/tools/TL300/TL354/RAND_TL354.database.zip",
        "filename": "TL-354-State-Level Estimates of Household Firearm Ownership.xlsx",
        "sheet_name": "State-Level Data & Factor Score"
    },
    "cdc_crime_data": {
        "url": "https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/explorer/crime/crime-trend",
        "states": ["California", "New York", "Massachusetts", "Texas", "Wyoming", "Alaska"],
        "time_frame": "10 Years",
        "excluded_files": [
            "Offender ethnicity",
            "Location Type",
            "Victim ethnicity",
            "Victim's Relationship to Offender"
        ],
        "weapon_filter": [
            "Handgun", "Rifle", "Shotgun", "Firearm", "Other Firearm",
            "Firearm (Automatic)", "Handgun (Automatic)", "Other Firearm (Automatic)",
            "Rifle (Automatic)", "Shotgun (Automatic)"
        ]
    },
    "fbi_nics_background": {
        "dataset": "masakii/fbi-nics-firearm-background-checks",
        "states": ["California", "New York", "Massachusetts", "Texas", "Wyoming", "Alaska"],
        "columns_to_drop": ["admin"]
    },
    "gun_ownership_state": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQBEbQoWMn_P81DuwmlQC0_jr2sJDzkkC0mvF6WLcM53ZYXi8RMfUlunvP1B5W0jRrJvH-wc-WGjDB1/pub?gid=0&single=true&output=csv",
        "states": ["California", "New York", "Massachusetts", "Texas", "Wyoming", "Alaska"],
        "columns_to_drop": ["summary", "mental_health_details", "weapon_details", "sources", "mental_health_sources", "sources_additional_age", "latitude", "longitude"]
    }
}

# Create a database engine
def create_database_engine():
    engine = create_engine('sqlite:///../data/firearm_analysis.db')
    return engine

# Step 2: Transform Data from the above datasets
# Define table structures
def create_tables(metadata):
    tables = {
        "us_firearm_ownership": Table(
            "us_firearm_ownership", metadata,
            Column("STATE", String),
            Column("Year", String),
            Column("HFR", Float),
            Column("HFR_se", Float),
        ),
        "fbi_nics_background": Table(
            "fbi_nics_background", metadata,
            Column("month", String),
            Column("state", String),
            Column("permit", Float),
            Column("permit_recheck", Float),
            Column("handgun", Float),
            Column("long_gun", Float),
            Column("other", Float),
            Column("multiple", Float),
            Column("prepawn_handgun", Float),
            Column("prepawn_long_gun", Float),
            Column("prepawn_other", Float),
            Column("redemption_handgun", Float),
            Column("redemption_long_gun", Float),
            Column("redemption_other", Float),
            Column("returned_handgun", Float),
            Column("returned_long_gun", Float),
            Column("returned_other", Float),
            Column("rentals_handgun", Float),
            Column("rentals_long_gun", Float),
            Column("private_sale_handgun", Float),
            Column("private_sale_long_gun", Float),
            Column("private_sale_other", Float),
            Column("return_to_seller_handgun", Float),
            Column("return_to_seller_long_gun", Float),
            Column("return_to_seller_other", Float),
            Column("totals", Float),
        ),
        "gun_ownership_state": Table(
            "gun_ownership_state", metadata,
            Column("case", String),
            Column("location", String),
            Column("date", String),
            Column("fatalities", Float),
            Column("injured", Float),
            Column("total_victims", Float),
            Column("location_type", String),
            Column("age_of_shooter", String),
            Column("prior_signs_mental_health_issues", String),
            Column("weapons_obtained_legally", String),
            Column("where_obtained", String),
            Column("weapon_type", String),
            Column("race", String),
            Column("gender", String),
            Column("type", String),
            Column("year", String),
        ),
    }
    return tables

# Save data to SQLite database
def save_to_database(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Data saved to table '{table_name}' in SQLite database.")


# Step 2.1: since it is the zip file, open the zip file, extract excel file and excel sheet"State-Level Data & Factor Score"
def download_us_firearm_ownership(data_path, engine):
    url = datasources["us_firearm_ownership"]["url"]
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        with z.open(os.path.join("RAND_TL354", datasources["us_firearm_ownership"]["filename"])) as f:
            df = pd.read_excel(f, sheet_name=datasources["us_firearm_ownership"]["sheet_name"])
            # Transform process: Clean data by replacing '-9' with NaN, convert columns to appropriate data types, and filter specific states
            df.replace(-9, pd.NA, inplace=True)
            df["HFR"] = df["HFR"].str.replace(',', '.').astype(float)
            df["HFR_se"] = df["HFR_se"].str.replace(',', '.').astype(float)
            filtered_states = ["California", "New York", "Massachusetts", "Texas", "Wyoming", "Alaska"]
            df_filtered = df[df["STATE"].isin(filtered_states)]
            save_to_database(df_filtered, "us_firearm_ownership", engine)

# Step 2.2: since it is the web sources, set the specific option, Time Frame: 10 years & specific 6 states.
def download_cdc_crime_data(data_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(datasources["cdc_crime_data"]["url"])
    
    for state in datasources["cdc_crime_data"]["states"]:
        # Select state from dropdown menu
        state_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='location']"))
        )
        state_dropdown.click()
        state_option = driver.find_element(By.XPATH, f"//option[text()='{state}']")
        state_option.click()
        time.sleep(2)

        # Set Time Frame to 10 Years
        time_frame_dropdown = driver.find_element(By.XPATH, "//select[@id='time-frame']")
        time_frame_dropdown.click()
        time_frame_option = driver.find_element(By.XPATH, "//option[text()='10 Years']")
        time_frame_option.click()
        time.sleep(2)

        # Click download button
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='download-button']"))
        )
        download_button.click()
        # Adjust sleep time as needed to allow for download completion
        time.sleep(5)  

        # Save the file
        downloaded_file = max([f for f in os.listdir(".") if f.endswith(".csv")], key=os.path.getctime)
        file_name = os.path.basename(downloaded_file)
        if not any(excluded in file_name for excluded in datasources["cdc_crime_data"]["excluded_files"]):
            os.rename(downloaded_file, os.path.join(data_path, f"cdc_crime_data_{state}_{file_name}"))

            # Additional filtering for weapon types if the file is "Type of Weapon Involved by Offense"
            if "Type of Weapon Involved by Offense" in file_name:
                df = pd.read_csv(os.path.join(data_path, f"cdc_crime_data_{state}_{file_name}"))
                filtered_df = df[df['key'].isin(datasources["cdc_crime_data"]["weapon_filter"])]
                filtered_df.to_csv(os.path.join(data_path, f"cdc_crime_data_{state}_{file_name}_filtered.csv"), index=False)

    driver.quit()

# Step 2.3: download the zipfile from Kaggle
def download_fbi_nics_background(data_path, engine):
    kaggle.api.dataset_download_files(datasources["fbi_nics_background"]["dataset"], path=data_path, unzip=True)
    csv_file = os.path.join(data_path, "fbi_nics_firearm_background_checks.csv")
    df = pd.read_csv(csv_file)
    # Filter specific states and drop the 'admin' column
    filtered_states = datasources["fbi_nics_background"]["states"]
    df_filtered = df[df["state"].isin(filtered_states)].drop(columns=datasources["fbi_nics_background"]["columns_to_drop"])
    # Change date format to mm-yyyy
    df_filtered["month"] = pd.to_datetime(df_filtered["month"]).dt.strftime("%m-%Y")
    save_to_database(df_filtered, "fbi_nics_background", engine)

# Step 2.4: download the csv files
def download_gun_ownership_state(data_path, engine):
    response = requests.get(datasources["gun_ownership_state"]["url"])
    df = pd.read_csv(io.StringIO(response.text))
    # Filter specific states
    filtered_states = datasources["gun_ownership_state"]["states"]
    df_filtered = df[df["location"].isin(filtered_states)]
    # Drop unnecessary columns
    df_filtered = df_filtered.drop(columns=datasources["gun_ownership_state"]["columns_to_drop"])
    # Change date format to DDMMYYYY
    df_filtered["date"] = pd.to_datetime(df_filtered["date"], format="%m/%d/%y").dt.strftime("%d%m%Y")
    save_to_database(df_filtered, "gun_ownership_state", engine)


def main():
    data_path = "../data"
    os.makedirs(data_path, exist_ok=True)

    # Create database engine and metadata
    engine = create_database_engine()
    metadata = MetaData()
    tables = create_tables(metadata)
    metadata.create_all(engine)

    print("Downloading US Firearm Ownership Data...")
    download_us_firearm_ownership(data_path, engine)

    print("Downloading CDC Crime Data...")
    download_cdc_crime_data(data_path)

    print("Downloading FBI NICS Background Data...")
    download_fbi_nics_background(data_path, engine)

    print("Downloading Gun Ownership State Data...")
    download_gun_ownership_state(data_path, engine)

    print("Data download completed!")

if __name__ == "__main__":
    main()


