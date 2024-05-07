# Airlines Analysis (Oceania Region Dataset)

## Overview

In this analysis, I aim to explore a dataset containing information about airline bookings in the Oceania region. The focus will be on understanding customer preferences regarding extra baggage options and creating a predictive model to forecast the number of bags purchased based on various parameters. By identifying flights that underperform in selling baggage options, this could help target poorly performing customer segments for the creation of effective marketing campaigns.

## Research Question

How can we use statistical methods to identify flights that are underperforming on selling baggage options, and how can we create a predictive model to forecast the number of bags purchased based on other parameters in the dataset?

## Data

| Column Name          | Description                                               |
|----------------------|-----------------------------------------------------------|
| num_passengers       | Number of passengers travelling                            |
| sales_channel        | Sales channel booking was made on                          |
| trip_type            | Type of trip (Round Trip, One Way, Circle Trip)           |
| purchase_lead        | Number of days between travel date and booking date       |
| length_of_stay       | Number of days spent at destination                       |
| flight_hour          | Hour of flight departure                                  |
| flight_day           | Day of the week of flight departure                       |
| route                | Origin -> Destination flight route                        |
| booking_origin       | Country from where booking was made                       |
| wants_extra_baggage  | Whether the customer wanted extra baggage in the booking  |
| wants_preferred_seat | Whether the customer wanted a preferred seat in the booking|
| wants_in_flight_meals| Whether the customer wanted in-flight meals in the booking|
| flight_duration      | Total duration of flight (in hours)                       |
| booking_complete     | Flag indicating if the customer completed the booking     |

## Experimental Design

Data Cleaning and Preprocessing: Remove any missing or inconsistent data, and encode categorical variables.
Exploratory Data Analysis (EDA): Analyze the distribution of variables, identify correlations, and explore patterns related to baggage options.
Statistical Analysis: Conduct hypothesis testing or other statistical methods to identify flights underperforming on selling baggage options.
Feature Selection: Select relevant features for building the predictive model.
Model Development: Train predictive models such as regression, decision trees, or neural networks to forecast the number of bags purchased.
Model Evaluation: Evaluate the performance of the models using appropriate metrics such as mean squared error or R-squared.
Interpretation: Interpret the results to identify key factors influencing baggage purchases and flights that require targeted marketing campaigns.

## Analysis

Through the use of statistical methods, we address : Do all flight paths have an equal distribution of baggage purchases. 
Operationalization : 
- Remove high-variance small sample flight routes, conduct analysis with remaining flights.
- We remove added variance and create a binary target variable. Of course, this removes information from our analysis but we instead simplify the interpretation of our analysis.

### Top flights that are underperforming
- Count of flights for analysis
- X-Y point plot of different flights (which quadrant seems to be underperforming on these)

### Predictive Model Development
- Feature Selection
- Model Creation
- Accuracy



## Conclusion
- This could be used by companies to create better marketing campaigns in the sale pipeline. This model can identify customers that have a willingness to buy a bag but do not, and thus effectively market to increase baggage conversion rate.
