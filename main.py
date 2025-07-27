
import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
df = pd.read_csv("Login tracking (2).csv")
df.columns = df.columns.str.strip()  # Clean column names

# Page config
st.set_page_config(page_title="S2M Admin Panel", layout="wide")
st.markdown("<style> body { background-color: #f0f8ff; } input { border: 1px solid black !important; } </style>", unsafe_allow_html=True)
st.image("s2m-logo.png", width=200)

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Page 1: Login
if not st.session_state.logged_in:
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with st.spinner("Authenticating..."):
            if username and password:
                st.session_state.logged_in = True
                st.success("Login Successful")
            else:
                st.error("Invalid credentials")

# Page 2 & 3: Only after login
if st.session_state.logged_in:
    page = st.sidebar.selectbox("Navigate", ["Dashboard", "Production Portal"])

    if page == "Dashboard":
        st.title("Admin Dashboard")

        total_hc = df["Total Member"].count() if "Total Member" in df.columns else "Column not found"

        if "DOJ" in df.columns:
            df["DOJ"] = pd.to_datetime(df["DOJ"], errors="coerce")
            df["Tenure Months"] = df["DOJ"].apply(lambda x: (datetime.now() - x).days // 30 if pd.notnull(x) else None)
            tenure_0_6 = df[df["Tenure Months"].between(0, 6)].shape[0]
            tenure_6_12 = df[df["Tenure Months"].between(6, 12)].shape[0]
            tenure_12_plus = df[df["Tenure Months"] > 12].shape[0]
        else:
            tenure_0_6 = tenure_6_12 = tenure_12_plus = "Missing DOJ"

        role_df = df["Internal Role"].value_counts() if "Internal Role" in df.columns else "Missing Internal Role"

        login_total = "Missing Column"
        if "Login Count" in df.columns:
            df["Login Count"] = pd.to_numeric(df["Login Count"], errors="coerce")
            login_total = int(df["Login Count"].sum(skipna=True))

        certified_count = df[df["Certified"].str.strip() == "Yes"].shape[0] if "Certified" in df.columns else "Missing Certified"
        inactive_count = df[df["Login Status"].str.strip() == "Inactive"].shape[0] if "Login Status" in df.columns else "Missing Login Status"

        st.metric("Total HC", total_hc)
        st.metric("Login Count", login_total)
        st.metric("Certified", certified_count)
        st.metric("Inactive Login", inactive_count)

        st.subheader("Tenurity Wise Deviation")
        st.write(f"0–6 Months: {tenure_0_6} | 6–12 Months: {tenure_6_12} | >1 Year: {tenure_12_plus}")

        st.subheader("Internal Role-wise HC")
        if isinstance(role_df, pd.Series):
            st.dataframe(role_df.reset_index().rename(columns={'index': 'Role', 'Internal Role': 'Count'}))
        else:
            st.write(role_df)

        st.download_button("Download Dashboard Data", data=df.to_csv(index=False).encode("utf-8"),
                           file_name="dashboard_data.csv", mime="text/csv")

import io

elif page == "Production Portal":
    st.title("Production Dashboard")
    try:
        # Load and clean CSV
        prod_df = pd.read_csv("Data (1).csv")
        prod_df.columns = prod_df.columns.str.strip()

        # Rename short headers to full consistent format
        prod_df = prod_df.rename(columns={
            "Date of Jo": "Date of Joining",
            "No Of Cha": "No Of Charts",
            "No Of Wo": "No Of Working Days"
        })

        # Define expected columns after renaming
        required_columns = ["Emp ID", "Emp Name", "Date of Joining", "No Of Charts", "No Of Working Days", "ICD", "Quality"]
        if not all(col in prod_df.columns for col in required_columns):
            st.error("One or more required columns are missing in the production CSV.")
        else:
            filtered_data = prod_df[required_columns]

            # Search by Emp ID
            emp_id = st.text_input("Enter Emp ID")
            if emp_id:
                emp_filtered = filtered_data[filtered_data["Emp ID"].astype(str).str.strip() == emp_id.strip()]
                st.write(emp_filtered if not emp_filtered.empty else "No data found for this ID")
            else:
                st.dataframe(filtered_data)

            # Download full data as Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_data.to_excel(writer, index=False, sheet_name='ProductionData')
            st.download_button("Download Excel", data=output.getvalue(),
                               file_name="production_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
