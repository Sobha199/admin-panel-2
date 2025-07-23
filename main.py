
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
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="S2M Admin Dashboard", layout="wide")
st.title("S2M Admin Dashboard")

# Load and clean data
df = pd.read_csv("Login tracking (2).csv")
df.columns = df.columns.str.strip()  # Remove extra spaces

# Total Headcount (Total Member count)
if "Total Member" in df.columns:
    total_hc = df["Total Member"].count()
else:
    total_hc = "Column not found"

# Tenurity calculation
if "DOJ" in df.columns:
    df["DOJ"] = pd.to_datetime(df["DOJ"], errors="coerce")
    df["Tenure Months"] = df["DOJ"].apply(lambda x: (datetime.now() - x).days // 30 if pd.notnull(x) else None)
    tenure_0_6 = df[df["Tenure Months"].between(0, 6)].shape[0]
    tenure_6_12 = df[df["Tenure Months"].between(6, 12)].shape[0]
    tenure_12_plus = df[df["Tenure Months"] > 12].shape[0]
else:
    tenure_0_6 = tenure_6_12 = tenure_12_plus = "DOJ column missing"

# Internal Role-wise HC
internal_role_data = df["Internal Role"].value_counts() if "Internal Role" in df.columns else "Internal Role column not found"

# Total Login Count
if "Login Count" in df.columns:
    df["Login Count"] = pd.to_numeric(df["Login Count"], errors="coerce")
    login_total = int(df["Login Count"].sum(skipna=True))
else:
    login_total = "Login Count column not found"

# Certified Count
certified_count = df[df["Certified"].str.strip() == "Yes"].shape[0] if "Certified" in df.columns else "Certified column not found"

# Inactive login count
inactive_count = df[df["Login Status"].str.strip() == "Inactive"].shape[0] if "Login Status" in df.columns else "Login Status column not found"

# Display metrics
st.metric("Total HC", total_hc)
st.metric("Login Count", login_total)
st.metric("Certified", certified_count)
st.metric("Inactive Login", inactive_count)

st.subheader("Tenurity Wise Deviation")
st.write(f"0–6 Months: {tenure_0_6} | 6–12 Months: {tenure_6_12} | >1 Year: {tenure_12_plus}")

st.subheader("Internal Role-wise HC")
if isinstance(internal_role_data, pd.Series):
    st.dataframe(internal_role_data.reset_index().rename(columns={'index': 'Role', 'Internal Role': 'Count'}))
else:
    st.write(internal_role_data)

# Download cleaned data
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Data", data=csv, file_name="dashboard_data.csv", mime="text/csv")
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
