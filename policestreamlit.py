import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

 #Database connection code

def create_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='policedb',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None
    
# Fetching data from database code

def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()
    
    # Streamlit Code

st.set_page_config(page_title="SecureCheck Police Dashboard", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: red;'>SecureCheck: A Digital Ledger For Police Post Logs</h1>
    <h6 style='text-align: center;'>Law Enforcement Activity Tracker & Insights</h3>
""", unsafe_allow_html=True)

# Show full table

st.header("Police Logs Insights Overview")
query = "SELECT * FROM policetable"
data = fetch_data(query)
st.dataframe(data, use_container_width=True)

#Overal value viewing
st.header("Key Metrics Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_stops = data.shape[0]
    st.metric("Total Police Stops", total_stops)

with col2:
    arrests = data[data['stop_outcome'].str.contains("arrest", case=False, na=False)].shape[0]
    st.metric("Total Arrests", arrests)

with col3:
    warnings = data[data['stop_outcome'].str.contains("warning", case=False, na=False)].shape[0]
    st.metric("Total Warnings", warnings)

with col4:
    drug_related = data[data['drugs_related_stop'] == 1].shape[0]
    st.metric("Drug Related Stops", drug_related)

# Charts Visualization
st.header("Different Visual Insights")

tab1, tab2, tab3, tab4 = st.tabs(["Driver Race Distribution",  "Country Distribution",  "Stops by Violation",  "Driver Gender Distribution"])


with tab1 :
    if not data.empty and 'driver_race' in data.columns:
        race_counts = data['driver_race'].value_counts().reset_index()
        race_counts.columns = ['Race', 'Count'] 
        fig = px.pie(race_counts, names='Race', values='Count', title='Driver Race Distribution')
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for race distribution chart.")

with tab2 :
    if not data.empty and 'country_name' in data.columns:
        race_counts = data['country_name'].value_counts().reset_index()
        race_counts.columns = ['Country', 'Count'] 
        fig = px.pie(race_counts, names='Country', values='Count', title='Country Distribution')
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for race country distribution chart.")



with tab3:
    if not data.empty and 'violation' in data.columns:
        violation_data = data['violation'].value_counts().reset_index()
        violation_data.columns = ['Violation', 'Count']
        fig = px.bar(violation_data, x='Violation', y='Count', title="Stops by Violation Type", color='Violation')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Violation chart.")

with tab4:
    if not data.empty and 'driver_gender' in data.columns:
        gender_data = data['driver_gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']
        fig = px.pie(gender_data, names='Gender', values='Count', title="Driver Gender Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Driver Gender chart.")

 # Advanced Queries With Query Select option
st.header("Advanced Insights With Query Option")

selected_query = st.selectbox("**Select a Query to Run**", [
    "1-Top 10 vehicle numbers involved in drug-related stops",
    "2-Vehicles most frequently searched",
    "3-The driver age group which had the highest arrest rate",
    "4-Gender distribution of drivers that are stopped in each country",
    "5-The race and gender combination that has the highest search rate",
    "6-The time of day that sees the most traffic stops",
    "7-The average stop duration for different violations",
    "8-Are stops during the night more likely to lead to arrests?",
    "9-Violations that are most associated with searches or arrests",
    "10-Violations that are most common among younger drivers (<25)",
    "11-Is there a violation that rarely results in search or arrest?",
    "12-Countries that report the highest rate of drug-related stops",
    "13-Arrest rate by country and violation",
    "14-Country that has the most stops with search conducted",
    "15-Yearly Breakdown of Stops and Arrests by Country",
    "16-Driver Violation Trends Based on Age and Race",
    "17-Time Period Analysis of Stops (Year, Month, Hour)",
    "18-Violations with High Search and Arrest Rates",
    "19-Driver Demographics by Country (Age, Gender, and Race)",
    "20-Top 5 Violations with Highest Arrest Rates"
])
query_map = {
    "1-Top 10 vehicle numbers involved in drug-related stops":"SELECT vehicle_number, COUNT(*) AS drug_stop_count FROM policetable WHERE drugs_related_stop = 1 GROUP BY vehicle_number ORDER BY drug_stop_count DESC LIMIT 10;",
    "2-Vehicles most frequently searched":"SELECT vehicle_number, COUNT(*) AS search_count FROM policetable WHERE search_conducted = 1 GROUP BY vehicle_number ORDER BY search_count DESC LIMIT 10;",
    "3-The driver age group which had the highest arrest rate":"SELECT CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 24 THEN '18-24' WHEN driver_age BETWEEN 25 AND 34 THEN '25-34' WHEN driver_age BETWEEN 35 AND 44 THEN '35-44' WHEN driver_age BETWEEN 45 AND 54 THEN '45-54' ELSE '55+' END AS age_group, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate FROM policetable GROUP BY age_group ORDER BY arrest_rate DESC LIMIT 1;",
    "4-Gender distribution of drivers that are stopped in each country":"SELECT country_name, driver_gender, COUNT(*) AS stop_count FROM policetable GROUP BY country_name, driver_gender ORDER BY country_name, driver_gender;",
    "5-The race and gender combination that has the highest search rate":"SELECT driver_race, driver_gender, COUNT(*) AS total_stops, SUM(search_conducted) AS searches, ROUND(SUM(search_conducted) * 100.0 / COUNT(*), 2) AS search_rate FROM policetable GROUP BY driver_race, driver_gender ORDER BY search_rate DESC LIMIT 1;",
    "6-The time of day that sees the most traffic stops":"SELECT EXTRACT(HOUR FROM stop_time) AS hour_of_day, COUNT(*) AS stop_count FROM policetable GROUP BY hour_of_day ORDER BY stop_count DESC LIMIT 1;",
    "7-The average stop duration for different violations":"SELECT violation, ROUND(AVG(stop_duration), 2) AS avg_duration FROM policetable GROUP BY violation ORDER BY avg_duration DESC;",
    "8-Are stops during the night more likely to lead to arrests?":"SELECT CASE WHEN (SELECT SUM(is_arrested) FROM policetable WHERE EXTRACT(HOUR FROM stop_time) BETWEEN 19 AND 23 OR EXTRACT(HOUR FROM stop_time) BETWEEN 0 AND 5) > (SELECT SUM(is_arrested) FROM policetable WHERE EXTRACT(HOUR FROM stop_time) BETWEEN 6 AND 18) THEN 'Yes' ELSE 'No' END AS night_more_arrests;",
    "9-Violations that are most associated with searches or arrests":"SELECT violation, COUNT(*) AS total_stops, SUM(search_conducted) AS searches, SUM(is_arrested) AS arrests FROM policetable GROUP BY violation ORDER BY searches + arrests DESC;",
    "10-Violations that are most common among younger drivers (<25)":"SELECT violation, COUNT(*) AS stop_count FROM policetable WHERE driver_age < 25 GROUP BY violation ORDER BY stop_count DESC;",
    "11-Is there a violation that rarely results in search or arrest?":"SELECT CASE WHEN EXISTS (SELECT 1 FROM policetable GROUP BY violation HAVING SUM(search_conducted) + SUM(is_arrested) < 0.05 * COUNT(*)) THEN 'Yes' ELSE 'No' END AS rarely_results_in_search_or_arrest;",
    "12-Countries that report the highest rate of drug-related stops":"SELECT country_name, COUNT(*) AS total_stops, SUM(drugs_related_stop) AS drug_stops, ROUND(SUM(drugs_related_stop) * 100.0 / COUNT(*), 2) AS drug_stop_rate FROM policetable GROUP BY country_name ORDER BY drug_stop_rate DESC;",
    "13-Arrest rate by country and violation":"SELECT country_name, violation, COUNT(*) AS total_stops, SUM(is_arrested) AS arrests, ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate FROM policetable GROUP BY country_name, violation ORDER BY arrest_rate DESC;",
    "14-Country that has the most stops with search conducted":"SELECT country_name, COUNT(*) AS total_stops, SUM(search_conducted) AS search_stops FROM policetable GROUP BY country_name ORDER BY search_stops DESC LIMIT 1;",
    "15-Yearly Breakdown of Stops and Arrests by Country":"SELECT DISTINCT country_name, year, COUNT(*) OVER (PARTITION BY country_name, year) AS total_stops, SUM(is_arrested) OVER (PARTITION BY country_name, year) AS arrests FROM (SELECT country_name, EXTRACT(YEAR FROM stop_date) AS year, is_arrested FROM policetable) AS sub ORDER BY country_name, year;",
    "16-Driver Violation Trends Based on Age and Race":"SELECT a.driver_race, b.age_group, a.violation, COUNT(*) AS stop_count FROM policetable a JOIN (SELECT id, CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 24 THEN '18-24' WHEN driver_age BETWEEN 25 AND 34 THEN '25-34' WHEN driver_age BETWEEN 35 AND 44 THEN '35-44' WHEN driver_age BETWEEN 45 AND 54 THEN '45-54' ELSE '55+' END AS age_group FROM policetable) b ON a.id = b.id GROUP BY a.driver_race, b.age_group, a.violation ORDER BY a.driver_race, b.age_group, stop_count DESC;",
    "17-Time Period Analysis of Stops (Year, Month, Hour)":"SELECT a.year, a.month, a.hour, COUNT(*) AS stop_count FROM policetable b JOIN (SELECT id, EXTRACT(YEAR FROM stop_date) AS year, EXTRACT(MONTH FROM stop_date) AS month, EXTRACT(HOUR FROM stop_time) AS hour FROM policetable) a ON a.id = b.id GROUP BY a.year, a.month, a.hour ORDER BY a.year, a.month, a.hour;",
    "18-Violations with High Search and Arrest Rates":"SELECT DISTINCT violation, COUNT(*) OVER (PARTITION BY violation) AS total_stops, SUM(search_conducted) OVER (PARTITION BY violation) AS searches, SUM(is_arrested) OVER (PARTITION BY violation) AS arrests, ROUND(SUM(search_conducted) OVER (PARTITION BY violation) * 100.0 / COUNT(*) OVER (PARTITION BY violation), 2) AS search_rate, ROUND(SUM(is_arrested) OVER (PARTITION BY violation) * 100.0 / COUNT(*) OVER (PARTITION BY violation), 2) AS arrest_rate FROM policetable ORDER BY search_rate DESC, arrest_rate DESC;",
    "19-Driver Demographics by Country (Age, Gender, and Race)":"SELECT country_name, driver_gender, driver_race, ROUND(AVG(driver_age), 1) AS avg_age, COUNT(*) AS stop_count FROM policetable GROUP BY country_name, driver_gender, driver_race ORDER BY country_name, driver_gender, driver_race;",
    "20-Top 5 Violations with Highest Arrest Rates":"SELECT violation, COUNT(*) AS total_stops, SUM(is_arrested) AS arrests, ROUND(SUM(is_arrested) * 100.0 / COUNT(*), 2) AS arrest_rate FROM policetable GROUP BY violation ORDER BY arrest_rate DESC LIMIT 5;"
}
if st.button("Run Query"):
    result = fetch_data(query_map[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.warning("No results found for the selected query.")




st.header("Add New Police Log To Predict Outcome and Violation")


# Input form (unchanged)
with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    country_name = st.selectbox("Country Name",data['country_name'].dropna().unique())
    driver_gender = st.selectbox("Driver Gender",data['driver_gender'].dropna().unique())
    driver_age = st.number_input("Driver Age", min_value=18, max_value=100)
    driver_race = st.selectbox("Driver Race",data['driver_race'].dropna().unique())
    search_conducted = st.selectbox("Was a Search Conducted?", data['search_conducted'].dropna().unique())
    search_type = st.selectbox("Search Type",data['search_type'].dropna().unique())
    drugs_related_stop = st.selectbox("Was it Drug Related?", data['drugs_related_stop'].dropna().unique())
    stop_duration = st.selectbox("Stop Duration", data['stop_duration'].dropna().unique())
    vehicle_number = st.text_input("Vehicle Number")
    #stop_datetime = pd.Timestamp.now()

    submitted = st.form_submit_button("Click Here To Predict Stop Outcome And Violation 🔍 ")

    if submitted:
    # ✅ Convert selectbox values to bools
        search_conducted_bool = True if search_conducted in ["Yes", "1", "True", True] else False
        drugs_related_stop_bool = True if drugs_related_stop in ["Yes", "1", "True", True] else False

    # ✅ Safe filter — compare same types!
        filtered_data = data[
        (data['driver_gender'] == driver_gender) &
        (data['driver_age'] == driver_age) &
        (data['search_conducted'] == search_conducted_bool) &
        (data['stop_duration'] == stop_duration) &
        (data['drugs_related_stop'] == drugs_related_stop_bool)
    ]


        if not filtered_data.empty:
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            predicted_violation = filtered_data['violation'].mode()[0]
        else:
            predicted_outcome = "warning"
            predicted_violation = "speeding"

        search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
        drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"
        st.markdown(f"""
 **Prediction Summary**

- **Predicted Violation:** {predicted_violation}  
- **Predicted Stop Outcome:** {predicted_outcome}

A **{driver_age}**-year-old **{driver_gender}** driver in **{country_name}** was stopped at **{stop_time.strftime('%I:%M %p')}** on **{stop_date}**, **{search_text}** and the stop **{drug_text}**.  
The stop duration is **{stop_duration}** and the vehicle number is **{vehicle_number}**.
""")

        

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 30px; font-weight: bold; color: Red;'>
        Stand for Law--Stand for Respect--Stand for Safety
    </div>
    """,
    unsafe_allow_html=True
)
