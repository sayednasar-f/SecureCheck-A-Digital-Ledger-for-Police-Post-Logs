
# 🚓 SecureCheck: Police Vehicle Check & Insights Dashboard

**SecureCheck** is a powerful and interactive Streamlit-based dashboard that allows law enforcement agencies and data analysts to visualize and analyze police stop data in real-time. It supports insights, predictions, and data-driven decision-making from large-scale vehicle stop logs.

---

## 📊 Key Features

- **Live Dashboard** for monitoring police stop data from MySQL database.
- **Searchable Table** view of all police stop records.
- **Key Metrics** such as total stops, arrests, warnings, and drug-related incidents.
- **Visual Charts** including pie and bar charts for race, gender, violation, and region distributions.
- **Advanced SQL Queries** to extract deep insights into law enforcement behavior and trends.
- **Predictive Tool** for estimating likely stop outcome and violation based on new entry data.
- **Mobile & Desktop Friendly UI** powered by Streamlit and Plotly.

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** MySQL
- **Visualization:** Plotly Express
- **Libraries:** 
  - `pandas`
  - `pymysql`
  - `streamlit`

---

## 🏁 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/securecheck-dashboard.git
cd securecheck-dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Make Sure MySQL is Running

Ensure a MySQL server is running and accessible locally:
- Host: `localhost`
- User: `root`
- Password: `root`
- Database: `policedb`
- Table: `policetable`

Update these settings in `create_connection()` if different.

### 4. Run the Streamlit App
```bash
streamlit run app.py
```

---

## 📌 SQL Schema Example

Ensure your MySQL table `policetable` contains at least the following columns:

- `id` (Primary Key)
- `stop_date` (DATE)
- `stop_time` (TIME)
- `country_name`
- `driver_gender`
- `driver_age`
- `driver_race`
- `search_conducted` (BOOLEAN or TINYINT)
- `search_type`
- `drugs_related_stop` (BOOLEAN or TINYINT)
- `stop_duration`
- `vehicle_number`
- `stop_outcome`
- `violation`

---

## 📷 Screenshots

<img src="screenshots/dashboard_overview.png" width="600"/>
<img src="screenshots/query_result.png" width="600"/>
<img src="screenshots/prediction_form.png" width="600"/>

---

## 🔍 Predictive Analysis

Users can input new stop information (e.g., age, gender, duration, etc.), and the app predicts:
- **Likely violation**
- **Likely stop outcome** (e.g., warning, arrest)

Predictions are based on existing dataset patterns using mode frequency.

---

## 🛡️ Motto

> **Stand for Law — Stand for Respect — Stand for Safety**

---

## 🧑‍💻 Author

**Sayed Nasar**  
📧 Contact: [your-email@example.com]  
🔗 GitHub: [github.com/your-username](https://github.com/your-username)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
