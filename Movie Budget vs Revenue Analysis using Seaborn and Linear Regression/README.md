\# Day 78 – Movie Budget vs Revenue Analysis



Course project from a Udemy Python course.



\## Overview



In this project, I analyzed a movie dataset containing production budgets, domestic gross revenue, worldwide gross revenue, and release dates.



The goal was to investigate whether higher production budgets lead to higher box office revenue and to build a simple Linear Regression model capable of estimating movie earnings based on budget.



The project combines data cleaning, exploratory data analysis (EDA), visualization using Seaborn, and predictive modeling using Scikit-Learn.



\---



\## Technologies Used



\- Python

\- Pandas

\- NumPy

\- Matplotlib

\- Seaborn

\- Scikit-Learn

\- Google Colab / Jupyter Notebook



\---



\## Dataset Information



The dataset contains:



\- Movie title

\- Release date

\- Production budget

\- Domestic revenue

\- Worldwide revenue

\- Ranking information



\---



\## Key Concepts Learned



\### Data Cleaning



\- Checked for missing values

\- Checked for duplicate records

\- Converted currency strings into numeric values

\- Converted date columns into Pandas datetime format



\### Exploratory Data Analysis (EDA)



\- Calculated descriptive statistics

\- Identified highest and lowest budget films

\- Investigated zero-revenue movies

\- Analyzed unreleased films

\- Calculated percentage of loss-making movies



\### Data Filtering



\- Multiple-condition filtering

\- Query-based filtering

\- Creation of cleaned datasets

\- Separation of old and modern movies



\### Feature Engineering



Created a new:



\- Decade column from release dates



Used this feature to compare:



\- Films released before 1970

\- Films released from 1970 onwards



\---



\## Data Visualization



\### Seaborn Scatter Plots



Visualized relationships between:



\- Production budget

\- Worldwide revenue

\- Release year



\### Bubble Charts



Used:



\- Color encoding

\- Size encoding



to highlight movie revenue performance.



\### Regression Plots



Created regression visualizations to study:



\- Budget vs Revenue relationship

\- Trend comparison between older and newer films



\---



\## Machine Learning



\### Linear Regression



Built predictive models using:



```python

from sklearn.linear\_model import LinearRegression

```



Learned how to calculate:



\- Intercept (θ₀)

\- Slope (θ₁)

\- R² Score



Model Formula:



Revenue = θ₀ + θ₁ × Budget



\---



\## Key Findings



\- Higher budgets generally correlate with higher worldwide revenue.

\- Around 37% of movies in the dataset lost money.

\- Modern films show a much stronger budget-revenue relationship than older films.

\- The regression model explained roughly 56% of revenue variance for modern films.

\- Older films showed a much weaker correlation between budget and revenue.



\---



\## Skills Practiced



\- Data Cleaning

\- Data Transformation

\- Exploratory Data Analysis

\- Feature Engineering

\- Statistical Analysis

\- Data Visualization

\- Seaborn

\- Linear Regression

\- Predictive Modeling

\- Machine Learning Fundamentals



\---



\## Project Type



Data Analysis and Machine Learning Fundamentals Project

