import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
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

# Function to check compliance
def check_compliance():
    try:
        aqi = float(aqi_entry.get())
        co2 = float(co2_entry.get())
        water = float(water_entry.get())
        waste = float(waste_entry.get())

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
            result_label.config(
                text="✓ COMPLIANT",
                fg="green"
            )
        else:
            status = "NON-COMPLIANT"
            result_label.config(
                text="⚠ NON-COMPLIANT\n" + "\n".join(violations),
                fg="red"
            )

        cursor.execute(
            "INSERT INTO records(aqi,co2,water,waste,status) VALUES(?,?,?,?,?)",
            (aqi, co2, water, waste, status)
        )
        conn.commit()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers."
        )

# Function to view records
def view_records():
    records = tk.Toplevel(root)
    records.title("Stored Records")

    text = tk.Text(records, width=70, height=20)
    text.pack()

    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()

    text.insert(tk.END,
                "ID | AQI | CO2 | WATER | WASTE | STATUS\n")
    text.insert(tk.END,
                "-" * 60 + "\n")

    for row in rows:
        text.insert(tk.END, str(row) + "\n")

# Main Window
root = tk.Tk()
root.title("Environmental Compliance Monitoring System")
root.geometry("450x450")

title = tk.Label(
    root,
    text="Environmental Compliance Monitoring System",
    font=("Arial", 14, "bold")
)
title.pack(pady=10)

tk.Label(root, text="AQI Value").pack()
aqi_entry = tk.Entry(root)
aqi_entry.pack()

tk.Label(root, text="CO2 Level (ppm)").pack()
co2_entry = tk.Entry(root)
co2_entry.pack()

tk.Label(root, text="Water Usage (Liters)").pack()
water_entry = tk.Entry(root)
water_entry.pack()

tk.Label(root, text="Waste Generated (kg)").pack()
waste_entry = tk.Entry(root)
waste_entry.pack()

tk.Button(
    root,
    text="Check Compliance",
    command=check_compliance
).pack(pady=10)

tk.Button(
    root,
    text="View Records",
    command=view_records
).pack()

result_label = tk.Label(
    root,
    text="",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=20)

root.mainloop()