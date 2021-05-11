# COVID-19 RELATED DATA ANALYSIS
## PROJECT OVERVIEW

Current days the entire world has the same goals: define the reasons of COVID-19 pandemic starting, propogate coronavirus vaccination and analyze all the factors which can make COVID-19 cases to go to zero. As those goals look rather impressive they can be achived through the regular analysis of COVID-19 statistics including new cases, fatality. testing etc. The goal of this project is analysis of real-life COVID-19 data, defining factors which are important for virus propogation, hospitality and fatality rates.

## DATA DESCRIPTION
As COVID pandemic became the biggest problem of 2020, there are lot of data sources, which collects and organizes different statistics relevant coronavirus disease. This project uses different datsets collected by Epidemic Intelligence team based on different authorized reports. Therefore ECDC's data keep worlwide data on daily and weekly basis, the most complete statistics provided for the European Union (EU) with 7-days frequency. That happens because every week a team of epidemiologists screen up to 500 relevant sources to collect the latest figures for publication. Datasource includes lot of COVID-related parameters, among them testing, new cases, hospitality, fatality etc. Current project uses 3 datasets: hospitality statistics, testing statistics and new cases statistics. Each of the links provided here keeps data link and data glossary also. All files available at csv format have been downloaded to the locally storage. Statistics describes 2020 year, each country started data gathering as far as first episodes appeared.

## CLEANING PROCESS
Cleaning process described below includes lot of steps oriented to the merging provided csv files, removing observations with lower sample size, filtering out part of the data to get statistics in the same time range for the different countries. The first part of the cleaning procedure described at the chunk below. Datafile hospitality includes both daily and weekly statistics. As other files describe COVID cases and tests by week, then hospitality daily data have been filtered out. Besides that information about data source is not used at the next part of the project, so some columns should be also removed. After all transormations hospitality dataset has columns: country, indicator, year_week and value.
Based on the data description above hospitality subset has long format, so it will be reshaped to wide form. For that all rows with NaN values have been removed and hospitlity dataset now includes wekkly new ICU admission per 100k population and weekly new hospital admissions per 100k population.
As hospitality dataset now includes two different parameters by each week per countries, then hospitality could be easy merged with tests dataset by columns country and year of the week. Testing dataset also includes column testing_data_source, which is useless for the further analysis. So, it will be droped. First few rows of the merged dataset are provided below. After merging each week per country includes weekly hospitality parameters (Hospital admission and ICU admission), new_cases, tests_done, testing_rate and positivity_rate. Last two parameters have been calculated as 100 x Number of new confirmed cases divided per population and number of tests done per week respectively. Merged dataset also keeps population information and country code.
The last dataset from proposed called cases includes some columns which also can be dropped. That's why features have been filtered before merging. There is also a need to rename some columns before merging to avoid duplicating. Format of the year_week column also should be changed. All those manipulations described at the chunk below.
Using merging once again all three csv files have been combined to the single dataset. First few lines of the final dataset provided here describe that all columns have appropriate format and meaningfull names. Therefore columns new-cases and cases_weekly have the same information. So, one of them will be omitted.
To make comparison between countries sophisticated we should check if theydescribe the same time periods. Checking number of observations per country we found that they have absolutely different statistics. Using this fact only countries with more than 40 observations have been selected for the further analysis. as almost all countries between 40 : 48
It is also important to check observations per week. Also throght theses 4 initial weeks the virus wasn't spread so much so if we consider them with analysis will affect the observation.
Very important to check data for missing values and to impute them if possible. as almost all the null values come from "Weekly new hospital admissions per 100k" and "Weekly new ICU admissions per 100k"


## DATA ANALYSIS AND VISUALIZATIONS
Based on the structure of the final dataset there is a set of questions which arise here.
#####  What is the best way to compare testings?
Testing rate is a great way to compare countries by COVID testings, as it is calculated as number of tests per 100K of population. So, we can compare countries with different population level. Timeline below let us compare testing rate per countries at the different time slices.
We can describe that during first few weeks Malta had the highest testing rate across all countries, probably because it has the smallest population rate. But most of the observed period Denmark was a leader by testing rate. This number increased obviously and the highest testing rate (more than 14000) observed at the 51th week of 2020 year.
##### Is there correlation between testing rate and positivity rate?
That is rather important question which let us decide if it is important to increase testing rate to define more positive COVID cases. To answer this question some manipulations with dataset have been provided. Columns used at this answer have been separated to another data frame. This new dataframe have been reshaped from long to the wide format. Also format of the date have been changed to weeks only, as all data cover the same 2020 year. That makes text at the x-axis more clear. First few row of the new dataset are described below.
Also, we need to standerds the value of test rate and the positive
to make the data stander have the range from 0:1 we create stander function:

inputs :
- data frame name
- column name as string, which need to be standerdize
- 
ouputs:
- same data frame with new columns value range 0:1

As dataset is rather huge there is no chance to make conclusions based on the table format. Scatterplot below demonstrate correlations between testing rate and positivity rate by dates and countries. Plots are separated by facets with different scales to make plot interpretaion easier, as levels are quite different per countries.
##### What is an association between new cases and deaths?
This question involves data along long period so, it is also reasonable to use visualizations for the answer. Columns needed for this answer have been organized to the separate dataset and reshaped to wide format, like for the previous answer. Head of the created dataset describes that both new cases and deaths are combined to the columns of the type variable-value. Year-week format also have been changed to make axis more readable.

Using facet barplot we can easy compare weekly cases and deaths by bountry and week of the year. Plot describes positive association, and we can estimate it numerically using Pearson correlation.

the correlation between  cases_weekly and deaths_weekly  can be as following:

*************************************************************************

strong postive correlations 0.8750 for Czechia
strong postive correlations 0.6234 for Denmark
strong postive correlations 0.8862 for Estonia
strong postive correlations 0.7983 for Germany
strong postive correlations 0.7400 for Greece
strong postive correlations 0.6029 for Italy
strong postive correlations 0.9642 for Latvia
strong postive correlations 0.7722 for Malta
strong postive correlations 0.8858 for Portugal
strong postive correlations 0.6459 for Slovenia

******************************************************

poor correlations 0.2827 for Belgium
poor correlations 0.3194 for France
poor correlations 0.2299 for Ireland
poor correlations 0.3105 for Netherlands
poor correlations 0.3313 for Sweden

##### Which country descibes the highest number of deaths?
This answer supposes some initial calculations. To answer it we need to calculate total number of COVID-associated deaths along observed period. Based on the calculations below Italy describes the highest rate - more than 75 thousand cases for 2020. The lowest number of deaths observed for Malta.
To compare countries by their geographical positions we can use interactive map.
##### Which is the deaths variability across countries?
Previous question let us estimate total number of deaths across 2020 because of COVID pandemic. But it is also important to know what is variability in week deaths across described countries. For that we used boxplot of weekly deaths per countries.
As each country has different population level we estimated fatality rate - number of deaths per population level. Italy still keeps the leader position by median fatality rate and maximum fatality rate. High median levels of fatality observed for france,Belgium, Greece and Latvia also. The lowest median fatality belongs to Estonia, Denmark, Malta and Portugal have the lowest variability of fatality.
## CONCLUSIONS
This project describes end-to-end data analysis of COVID-19 related data, including data uploading, filtering, reshaping, transformation and visualization. The main aspects of the project are relevant to the weekly data of 2020 statistics by 15 countries: Greece Malta,Italy,Portugal,Latvia,Denmark,Czechia ,Sweden ,Belgium,France, Netherlands, Slovenia, Estonia,Germany,Ireland
Along the study there were found that Denmark describes the highest testing rate along 2020 year. There were assosiation between testing rate and positivity rate some countiers is strong postive like Croatia some strong negative like Cyprus and some poor like Italy . like At the same time weekly deaths are positively associated with weekly new cases at the high level. Italy described the highest number of deaths along 2020 with more than 75k defined cases. It also has the highest fatality rate among 15 countries used for the analysis.
## FUTURE WORK
All further steps relevant this project are oriented for the 2021 data analysis, including factors of vaccination. As different virus stamps have been defined during last month it is important to include this information to the further investigations of COVID-related data.