import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Environmental Compliance Monitoring System",
    page_icon="🌱"
)

# Database
conn = sqlite3.connect("environment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aqi REAL,
    co2 REAL,
    water REAL,
    waste REAL,
    status TEXT
)
""")
conn.commit()

# Title
st.title("🌱 Environmental Compliance Monitoring System")
st.write("Monitor environmental parameters and check compliance status.")

st.divider()

# Input fields
aqi = st.number_input("AQI Value", min_value=0.0, step=1.0)
co2 = st.number_input("CO2 Level (ppm)", min_value=0.0, step=1.0)
water = st.number_input("Water Usage (Liters)", min_value=0.0, step=1.0)
waste = st.number_input("Waste Generated (kg)", min_value=0.0, step=1.0)

# Check compliance
if st.button("Check Compliance"):

    violations = []

    if aqi > 100:
        violations.append("AQI")

    if co2 > 400:
        violations.append("CO2")

    if water > 1000:
        violations.append("Water Usage")

    if waste > 50:
        violations.append("Waste Generation")

    if len(violations) == 0:
        status = "COMPLIANT"

        st.success("✓ COMPLIANT")
        st.write("All environmental parameters are within the permitted limits.")

    else:
        status = "NON-COMPLIANT"

        st.error("⚠ NON-COMPLIANT")

        st.write("Violations detected:")

        for violation in violations:
            st.write("•", violation)

    # Save record
    cursor.execute(
        """
        INSERT INTO records
        (aqi, co2, water, waste, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (aqi, co2, water, waste, status)
    )

    conn.commit()

st.divider()

# View records
st.subheader("📊 Stored Records")

if st.button("View Records"):

    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()

    if rows:
        st.table(
            {
                "ID": [row[0] for row in rows],
                "AQI": [row[1] for row in rows],
                "CO2": [row[2] for row in rows],
                "Water": [row[3] for row in rows],
                "Waste": [row[4] for row in rows],
                "Status": [row[5] for row in rows]
            }
        )
    else:
        st.info("No records found.")