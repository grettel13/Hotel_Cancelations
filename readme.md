# Classifying Hotel Reservation Cancelations

Demand forecasting is essential for hotel management to accurately meet guest needs while avoiding unnecessary costs. Reliable estimates of net demand are necessary for:
- Preparation of resources including staff and food offered at hotel
- Revenue management
- Pricing and cancelation policy governance

Hotels have the option of implementing strict cancelation policies, but these can be a detriment and result in less bookings.

>## Can hotel reservation cancelations be predicted?

Of course, no prediction can ever be exact, but implementing data science models for this classficiation problem can narrow the degree of uncertainty around reservation cancelations.

>By implementing a random forest model, a precision of 89% for 'canceled' class was achieved on unseen data.

Tuning the classification model for the precision metric allows for a more conservative approach. This sides on higher confidence of predicted cancelations in efforts to avoid situations of under-preparedness for hotel guests.

---
# Approach:

1. Understand/clean data
2. Perform Exploratory Data Analysis (EDA)
3. Metrics selection
4. Implement classification algorithms
4. Model selection

# Data used:

The data is sourced from an article called [Hotel booking demand datasets](https://www.sciencedirect.com/science/article/pii/S2352340918315191#bib6) by Nuno Antonio, Ana Almeida, and Luis Nunes in 2019.

The scrubbed data was made publicly available from the hotels' property management system (PMS) for investigation.

Data contains:
- 2 hotels
- ~120K observations
- 32 features
- data over 2 years

# Features used:

<style>
.heatMap {
}
.heatMap th {
background: white;
}
.heatMap tr:nth-child(1) { background: grey; }
.heatMap tr:nth-child(2) { background: white; }
.heatMap tr:nth-child(3) { background: grey; }
</style>

<div class="heatMap">

| Everything | in this table | is Centered |  and the table will only take up 70% of the screen width  |
| -- | -- | -- | -- |
| This | is | a | Red Row |
| This | is | an | Orange Row |
| This | is | a | Green Row |

</div>

24 features were selected from 190 based on data available for high volumes of schools.

The following features were provided as % of total students (overall), but also broken down by ethnicity.

| Feature | Breakdown
| --------------- | --------------
| Graduation Rates | Overall, Black, White, Hispanic
| Population Rates | Overall, Black, White, Hispanic
| Suspension Rates | Overall, Black, White
| Chronically Absent Rates | Overall, Black, White
<br/>

Additional School Features:
| Feature | Description
| --------------- | --------------
| Grades | Grades offered at school. Traditional 9-12 grade or "other"
| School Type | Public or Public Charter
| Students | Number of students at school
| Dual Enrollment Rate | % of students enrolled in dual enrollment
| AP course rate | % of students enrolled in AP courses
| Teacher experienced rate | % of teachers with 3 years experience or more
| Avg teacher salary | Average teacher salary
| Teacher cert rate | % of teachers with certification
| Student : Teacher Ratio | Number of students per 1 teacher
| Student : Counselor Ratio | Number of students per 1 counselor

<br/>

# Tools Used:

- Selenium
- Beautiful Soup
- Seaborn
- Matplotlib

# File Organization:
- **Hotel Reservation Cancelations.pdf** - 5 minute presentation of project findings
- **hotel_bookings.ipynb** - main notebook
- **hotels.py** - helper functions utilized by main notebook
- **hotel_create_psql_db.ipynb** - notebook used to load original data in CSV formats to a postgres sql database locally
