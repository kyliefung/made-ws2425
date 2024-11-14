# Project Plan

## Title
<!-- Give your project a short title. -->
Comparative Analysis of Firearm Ownership and Crime Rates Across U.S. States

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. How does the level of firearm ownership and the stringency of restrictions correlate with crime rates across different states in the United States, and what differences can be observed between states with stricter vs. more lenient gun laws?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Firearm ownership is always a controversial topic in the United States, where the right to bear arms is protected by the Constitution. However, individual states vary greatly in the regulations they impose on firearm ownership. Some states, such as California and New York, have stringent licensing requirements, waiting periods, and mandatory background checks, while others, such as Texas and Wyoming, impose minimal restrictions on firearm ownership and carrying.

This project aims to analyze the correlation between firearm ownership levels, the strictness of firearm regulations, and various crime rates—including violent crimes and homicides—across different states in the United States. In this study, California, New York, and Massachusetts are considered strict states, while Texas, Wyoming, and Alaska are considered lenient states. By comparing data from states with both stringent and lenient firearm restrictions, this project will identify patterns and assess whether stricter regulations are associated with different crime rates. The comparative analysis will provide insights into how state-level cultural, legal, and societal differences impact the relationship between gun ownership and crime.

## Datasources
<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->
### Datasource1: United Status - State-Level Estimates of Household Firearm Ownership
* Metadata URL: https://www.rand.org/pubs/tools/TL354.html
* Data Type: CSV
* Description: 
The official data source is from independent and nonprofit organization. It provides annual, state-level estimates of household firearm ownership from 1980 to 2016, which includes the data of household firearm ownership in US, firearm Suicide and other details. 

### Datasource2: United Status - Centers for Disease Control and Prevention (CDC) - National Center for Health Statistics
* Metadata URL: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/explorer/crime/crime-trend
* Data Type: CSV
* Description: 
The official data source is from the FBI. On the website, it provides various characteristics of crime details, such as violent offenses, offender vs. victim demographics, and the type of weapon involved by offense, which can help reflect the relationship between firearms and crime causes.

### Datasource3: FBI NICS Firearm Background Checks
* Metadata URL: https://www.kaggle.com/datasets/masakii/fbi-nics-firearm-background-checks
* Data Type: CSV 
* Description: 
The data source is Kaggle, but the dataset is from the FBI's National Instant Criminal Background Check System. The dataset contains the number of FBI NICS firearm background checks by month, state, and type between November 1998 and 2024.

### Datasource4: US Gun Ownership By State
* Metadata URL: https://www.motherjones.com/politics/2012/12/mass-shootings-mother-jones-full-data/
* Data Type: CSV
* Description: 
The official data source is Mother Jones, which records all the mass shooting cases, originally covered cases from 1982 to 2012. 


## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Creation of Project Structure [#1][i1]
2. Datasource Collection [#2][i2]
3. Modified the creation of Project Structure

[i1]: https://github.com/kyliefung/made-ws2425/issues/1
[i2]: https://github.com/kyliefung/made-ws2425/issues/2
