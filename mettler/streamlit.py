import pandas as pd
import plotly.express as px
import streamlit as st 
import pymssql
import datetime
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Production Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Production Data Analysis:bar_chart:")

#######################################
# SQL connect
#######################################

# SQL server settings
sql_server = "IN01W-JZM1SV3"
sql_user = "sa"
sql_password = "mt"
sql_database = "iot"

# Connect to database
conn = pymssql.connect(sql_server, sql_user, sql_password, sql_database)

# Define a SQL query to select the sales data
sql_query = "SELECT * FROM pi_sql"

# Read the data into a pandas DataFrame
df = pd.read_sql(sql_query, conn)

#######################################
# Side Bar
#######################################

image_file = "C:/Users/karadkar-1/Desktop/python/streamlit dashboard/mettler/logo.png"
image = Image.open(image_file)
sidebar = st.sidebar
sidebar.image(image)

st.sidebar.header("Please Filter Here:")

# Add batch filter
Batch = st.sidebar.multiselect(
    "Select the batch:",
    options=df["batch"].unique(),
    default=list(df["batch"].unique())
)

# Add user filter
User = st.sidebar.multiselect(
    "Select the User:",
    options=df["user"].unique(),
    default=list(df["user"].unique())
)

# Add product filter
Product = st.sidebar.multiselect(
    "Select the Product:",
    options=df["product"].unique(),
    default=list(df["product"].unique())
)

# Add time-based filter
time_filter = st.sidebar.selectbox(
    "Time Filter:",
    ("Hourly", "Daily", "Monthly")
)

# Add a sidebar for date range selection
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
date_range = st.sidebar.date_input('Select date range', value=(today, tomorrow), key='daterange')
# Convert the date range to datetime format
start_date = datetime.datetime.combine(date_range[0], datetime.datetime.min.time())
end_date = datetime.datetime.combine(date_range[1], datetime.datetime.min.time())

df_selection = df.query(
    "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

#display table data with expand feature
with st.expander("Data Preview"):   #st.expander for useful for table data 
    df_selection = df_selection.sort_values('id', ascending=False)
    st.dataframe(df_selection)

#######################################
# KPI
#######################################

# TOP KPI's
total_prod = int(df_selection["is_valid"].sum())
total_rej = int(df_selection["is_underweight"].sum() + df_selection["is_overweight"].sum())

#######################################
# time selection
#######################################

df_selection["rejected"] = df_selection["is_overweight"] + df_selection["is_underweight"]
# Group data by hour and sum the values
if time_filter == "Hourly":
    df_selection["created_at"] = pd.to_datetime(df_selection["created_at"])
    df_selection = df_selection.set_index("created_at")
    df_selection = df_selection.resample("1H").sum()
elif time_filter == "Daily":
    df_selection["created_at"] = pd.to_datetime(df_selection["created_at"])
    df_selection = df_selection.set_index("created_at")
    df_selection = df_selection.resample("D").sum()
elif time_filter == "Monthly":
    df_selection["created_at"] = pd.to_datetime(df_selection["created_at"])
    df_selection = df_selection.set_index("created_at")
    df_selection = df_selection.resample("M").sum()

#######################################
# BAR CHART
#######################################

# Create a grouped bar chart using Plotly Express
fig = px.bar(df_selection, x=df_selection.index, y=["is_valid", "rejected"], 
             color_discrete_sequence=["green", "orange"],
             labels={"value": "Quantity", "variable": "Status"}, barmode="group", width=800, height=500)
fig.update_layout(title="Production Status per " + time_filter, xaxis_title="Time", yaxis_title="Product Status Quantity")

#######################################
# LINE CHART
#######################################

# Create a line chart using Plotly Express
fig3 = px.line(df_selection, x=df_selection.index, y=["is_valid","rejected"], color_discrete_sequence=["green", "orange"],
               labels={"value": "Quantity"}, width=800, height=500)
fig3.update_layout(title="Valid Production per " + time_filter + " by Product", xaxis_title="Time", yaxis_title="Product Status Quantity")

#######################################
# PIE CHART
#######################################

pie_df_selection = df.query(
    "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date & is_valid == 1"
)
# Define a dictionary to map the colors to product lines
color_map = {"Apple": "#FF5733", "Banana": "#DAF7A6", "Cherry": "#FFC300"}
# Filter the data by is_valid status and group by product
df_pie = pie_df_selection[pie_df_selection["is_valid"] == 1].groupby("product")["is_valid"].count().reset_index()
df_pie = df_pie[df_pie["product"].isin(Product)]
# Create a pie chart using Plotly Express
fig2 = px.pie(df_pie, values="is_valid", names="product", width=800, height=500,
              color="product", color_discrete_map=color_map)
fig2.update_layout(title="Valid Production per Product Line")

#######################################
# LAST UPDATE
#######################################
last_updated_date = df['created_at'].max()
# Format the last updated date
last_updated_date_str = last_updated_date.strftime("%Y-%m-%d %H:%M:%S")
# Display the last updated date at the top right corner
st.markdown(f'<div style="position:absolute; top:2px; right: 2px; color: #888888;">Last Updated: {last_updated_date_str}</div>', unsafe_allow_html=True)
# Add some space below the last updated date
st.write("")

#######################################
# PERCENTAGE CHANGE
#######################################
# Group data by day and calculate the percentage change in valid production
df_day = df_selection.groupby(df_selection.index.date)["is_valid"].agg(["count", "sum"])
df_day["percentage_change"] = round(df_day["sum"].pct_change()*100,2)

#######################################
# PREDICTIVE MODELING
#######################################

# Define the features and target variable
#X = df_selection[["net", "product"]]
#y = df_selection["is_valid"]
#Convert categorical variables to dummy variables
#X = pd.get_dummies(X, columns=["product"])

# Split the data into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Fit a logistic regression model
#lr = LogisticRegression()
#lr.fit(X_train, y_train)

# Make predictions on the testing data
#y_pred = lr.predict(X_test)

# Calculate the accuracy of the model
#accuracy = lr.score(X_test, y_test)
#st.write(accuracy)

#######################################
# SUM OF VALID AND REJECT WEIGHT
#######################################

valid_df_selection = df.query(
    "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date & is_valid == 1"
)
# Calculate the total net weight for the selected date range only when is_valid is 1
total_net_weight = valid_df_selection["net"].sum()
# Calculate the rejected total net weight for the selected date range where is_valid is 0 and is_overweight is 1
rejected_df_selection = df.query(
    "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date & is_valid == 0 & (is_overweight == 1 | is_underweight == 1)"
)
rejected_net_weight = rejected_df_selection["net"].sum()

#######################################
# INDIVIDUAL COUNT CAL
#######################################

# Get a list of the unique products in the dataset
prod_selection = df.query(
    "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date"
    )['product'].unique()

# Loop through the products and count the number of valid and rejected entries for each
valid_counts = {}
reject_counts = {}
for product in prod_selection:
    product_data_valid = df.query(
        "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date & product == @product & is_valid == 1"
    )
    valid_count = len(product_data_valid.index)
    valid_counts[product] = valid_count
    
    product_data_reject = df.query(
        "batch == @Batch & product == @Product & user  ==@User & created_at >= @start_date & created_at <= @end_date & product == @product & is_valid == 0 & (is_overweight == 1 | is_underweight == 1)"
    )
    reject_count = len(product_data_reject.index)
    reject_counts[product] = reject_count

#######################################
# SCATTER CHART
#######################################

# Define the colors for each product category
colors = {'Apple': 'red', 'Banana': 'blue', 'Cherry': 'green'}

# Create a scatter plot using Plotly Express
fig4 = px.scatter(x=list(valid_counts.values()), y=list(reject_counts.values()), 
                  text=list(valid_counts.keys()), color=list(valid_counts.keys()),
                  color_discrete_map=colors, size_max=100, width=800, height=500,
                  trendline='ols', trendline_color_override='black')

fig4.update_traces(textposition='top center', textfont=dict(color='black', size=12),
                   marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))

fig4.update_layout(title="Valid vs Rejected Entries per Product", xaxis_title="Valid Entries",
                   yaxis_title="Rejected Entries", legend_title='Product')

#######################################
# STREAMLIT LAYOUT
#######################################

left_0,right_0 = st.columns(2)
with left_0:
    # Display the results in a Streamlit app
    st.write("Total count of valid entries for each product:")
    for product, count in valid_counts.items():
        st.write(f"{product}: {count}")
with right_0:
    # Display the results in a Streamlit app
    st.write("Total count of reject entries for each product:")
    for product, count in reject_counts.items():
        st.write(f"{product}: {count}")

left_1, middle_1, right_1,right_1_2= st.columns(4)
with left_1:
    #st.metric(label="Total production:",value=total_prod)
    st.write("Total production:")
    st.subheader(total_prod)
with middle_1:
    st.write("Total Rejected:")
    st.subheader(total_rej)

with right_1:
    st.write("Accepted NET Weight:")
    st.subheader(str(total_net_weight)+ " kg")

with right_1_2:
    st.write("Rejected NET Weight:")
    if rejected_net_weight > total_net_weight:
        st.markdown(f'<h3 style="color: red;">{rejected_net_weight} kg</h3>', unsafe_allow_html=True)
    else:
        st.subheader(f'{rejected_net_weight} kg')

st.markdown("""---""")


left_2, middle_2 = st.columns((2,1))
with left_2:
    # Display the scatter plot in the Streamlit app
    st.plotly_chart(fig4, use_container_width=True)

with middle_2:
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""---""")

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""---""")

left_3,middle_3 = st.columns((1,2))
with left_3:
    st.write("Percentage of Valid Production per Day:")
    st.dataframe(df_day)

with middle_3:
    st.plotly_chart(fig, use_container_width=True)
    
