# Comparative Analysis of Firearm Ownership and Crime Rates Across U.S. States

## Project Description
Firearm ownership is always a controversial topic in the United States, where the right to bear arms is protected by the Constitution. However, individual states vary greatly in the regulations they impose on firearm ownership. The strict states typically require more extensive processes and tests to obtain firearm permits. This project analyses the correlation between firearm ownership, regulation strictness, and crime rates across various U.S. states. States like “California”, “Massachusetts” and “New York” have strict regulations, while “Texas”, “Alaska” and “Wyoming” are more lenient.

By comparing data from both types of states, we aim to identify patterns, offering insights into the relationship between gun ownership and crime. In other words, this project seeks to answer:

**“How does the level of firearm ownership and stringency of restrictions correlate with crime rates across different states in the United States, and what differences can be observed between states with stricter vs. more lenient gun laws?”**

## Data Source
**1. FBI NICS Firearm Background Checks**
- **Description:** The dataset is sourced from Kaggle and originally provided by the National Instant Criminal Background Check System (NICS). It contains the number of FBI NICS firearm background checks by month, state, and type from November 1998 to 2023. This dataset provides insights into the stringency of firearm restrictions across different states, as it includes mandatory background checks for citizens wishing to purchase firearms.
- **Licenses:** Licensed under the MIT License. Data is from the FBI's FOIA Library. 

**2. Firearm Mortality by State**
- **Description:** The dataset is sourced from the Centers for Disease Control and Prevention (CDC). It provides firearm mortality statistics at the state level across the United States, including annual data on deaths resulting from firearm-related incidents. The data includes information such as the number of firearm-related deaths, categorized by state and year.
- **Licenses:** Licensed under Section 308(d) of the Public Health Service Act and CIPSEA. Data is used for statistical purposes.
  
**3. FBI Crime Data**
- **Description:** The dataset is sourced from the FBI's Centers for Crime Data Explorer. It contains crime statistics across the United States, including detailed factors associated with the crimes, such as “Type of Weapon Involved by Offense”, “Offense Linked to Another Offense”, and others. This dataset provides valuable insights into crime rates across different U.S. states and helps to identify the factors contributing to various types of offenses.
-  **Licenses:** Available under the FBI's FOIA Library. Data is used for transparency and academic purposes.


## Data Pipeline
- The ETL(Extract, Transform, Load) pipeline is implemented using python to handle both data sources, each downloaded as a CSV directory within a zip archieve. This process involves extracting the right CSV file, transforming, and saving it as CSV format and SQLite databases.
<img width="400" alt="ETL Pipeline" src="https://github.com/user-attachments/assets/106e1dd1-cee5-4028-b7da-abf18a91d1e6" />

## Data Analysis
The correlation among firearm permit, firearm-related crimes across different states is shown below.
More Information can be reviewed in analysis-report.pdf. 
<img width="808" alt="data-analysis" src="https://github.com/user-attachments/assets/42fefc9d-bdcb-4c26-8068-95659fa2eb80" />


# Methods of Advanced Data Engineering

### Exporting a Jupyter Notebook
Jupyter Notebooks can be exported using `nbconvert` (`pip install nbconvert`). For example, to export the example notebook to HTML: `jupyter nbconvert --to html examples/final-report-example.ipynb --embed-images --output final-report.html`


## Exercises
During the semester you will need to complete exercises using [Jayvee](https://github.com/jvalue/jayvee). You **must** place your submission in the `exercises` folder in your repository and name them according to their number from one to five: `exercise<number from 1-5>.jv`.

In regular intervals, exercises will be given as homework to complete during the semester. Details and deadlines will be discussed in the lecture, also see the [course schedule](https://made.uni1.de/).

### Exercise Feedback
We provide automated exercise feedback using a GitHub action (that is defined in `.github/workflows/exercise-feedback.yml`). 

To view your exercise feedback, navigate to Actions → Exercise Feedback in your repository.

The exercise feedback is executed whenever you make a change in files in the `exercise` folder and push your local changes to the repository on GitHub. To see the feedback, open the latest GitHub Action run, open the `exercise-feedback` job and `Exercise Feedback` step. You should see command line output that contains output like this:

```sh
Found exercises/exercise1.jv, executing model...
Found output file airports.sqlite, grading...
Grading Exercise 1
	Overall points 17 of 17
	---
	By category:
		Shape: 4 of 4
		Types: 13 of 13
```
