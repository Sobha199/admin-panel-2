
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Load Data
login_data = pd.read_csv("Login tracking (2).csv")

# Logo and Theme
st.set_page_config(page_title="S2M Admin Panel", layout="wide")
st.markdown(
    "<style> body { background-color: #f0f8ff; } "
    "input { border: 1px solid black !important; } </style>",
    unsafe_allow_html=True
)
st.image("s2m-logo.png", width=200)

# Page Navigation
page = st.sidebar.selectbox("Select Page", ["Login", "Dashboard", "Production Portal"])

# Page 1: Login
if page == "Login":
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with st.spinner("Authenticating..."):
            st.success("Login Successful")

# Page 2: Dashboard
elif page == "Dashboard":
    st.title("Admin Dashboard")
    st.subheader("Total Headcount")
    total_hc = login_data["Total Member"].count()
    st.metric("Total HC", total_hc)

    st.subheader("Tenurity-wise Deviation")
    today = pd.Timestamp.now()
    login_data["DOJ"] = pd.to_datetime(login_data["DOJ"], errors="coerce")
    login_data["Tenure Months"] = login_data["DOJ"].apply(lambda x: (today - x).days // 30 if pd.notnull(x) else None)
    tenure_0_6 = login_data[login_data["Tenure Months"].between(0, 6)].shape[0]
    tenure_6_12 = login_data[login_data["Tenure Months"].between(6, 12)].shape[0]
    tenure_12_plus = login_data[login_data["Tenure Months"] > 12].shape[0]
    st.write(f"0-6 Months: {tenure_0_6}, 6-12 Months: {tenure_6_12}, >1 Year: {tenure_12_plus}")

    st.subheader("Internal Role-wise HC")
    st.write(login_data["Internal Role"].value_counts())
    login_data["Login Count"] = login_data["Login Count"].count()
    st.metric("Login Count" , Login Count)
    st.subheader("Certified Count")
    st.write("Certified:", login_data[login_data["Certified"] == "Yes"].count()
     st.metric("Certified" ,Certified)

    st.subheader("Inactive Login Count")
    st.write("Inactive:", login_data[login_data["Login Status"] == "Inactive"].count()
     st.metric("Inactive" ,Inactive)

    # Download CSV
    csv = login_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="admin_data.csv", mime="text/csv")

# Page 3: Production Portal (Dummy Data)
elif page == "Production Portal":
    st.title("Production Dashboard")

    dummy_data = pd.DataFrame({
        "Emp ID": ["EMP001", "EMP002", "EMP003"],
        "Charts Completed": [15, 20, 10],
        "Pages Completed": [150, 200, 100],
        "ICD Completed": [5, 8, 3],
        "Working Days": [20, 22, 18]
    })

    search_id = st.text_input("Enter Emp ID to Search")
    if search_id:
        filtered = dummy_data[dummy_data["Emp ID"] == search_id]
        st.write(filtered)
    else:
        st.dataframe(dummy_data)

    # Download Option
    download_csv = dummy_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Production Data", data=download_csv, file_name="production_data.csv", mime="text/csv")
