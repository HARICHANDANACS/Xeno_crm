import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Dummy Data for Campaigns (In a real-world scenario, this would be in a DB)
customers = []
orders = []
campaigns = []

# Function to simulate sending messages (Vendor API)
def send_message(customer_name):
    success = random.choice([True, False])
    return success

# Dummy Function to simulate AI Rule Parsing (replaces OpenAI API)
def generate_segment_rule(prompt):
    return "spend > 10000 AND visits < 3"

# Dummy AI-powered message suggestion (replaces OpenAI API)
def ai_message_suggestion(campaign_objective):
    return [
        "Get 20% off your next purchase!",
        "We appreciate your loyalty—here’s something special!",
        "Thank you for being with us. Enjoy this exclusive deal!"
    ]

# Data Ingestion (Customer & Orders)
def ingest_data():
    st.subheader("Ingest Customer and Order Data")
    customer_name = st.text_input("Customer Name")
    customer_email = st.text_input("Customer Email")
    customer_spend = st.number_input("Customer Spend", min_value=0)

    if st.button("Save Customer"):
        customer = {
            "name": customer_name,
            "email": customer_email,
            "spend": customer_spend,
            "status": "Active"
        }
        customers.append(customer)
        st.success(f"Customer {customer_name} saved!")

    order_id = st.text_input("Order ID")
    order_amount = st.number_input("Order Amount", min_value=0)

    if st.button("Save Order"):
        order = {
            "order_id": order_id,
            "amount": order_amount,
            "status": "Processed"
        }
        orders.append(order)
        st.success(f"Order {order_id} saved!")

# Campaign Creation (Audience Segmentation)
def create_campaign():
    st.subheader("Create Campaign")
    spend_threshold = st.number_input("Min Spend for Audience", value=10000)
    visits_threshold = st.number_input("Max Visits for Audience", value=3)

    if st.button("Preview Audience"):
        audience_size = random.randint(50, 200)
        st.write(f"Audience size: {audience_size}")
    
    prompt = st.text_input("Enter segmentation rule (e.g., 'Customers who spent > 10000 and visited < 3 times')")
    segment_rule = ""
    if prompt:
        segment_rule = generate_segment_rule(prompt)
        st.write(f"Generated Rule: {segment_rule}")

    if st.button("Save Campaign"):
        if segment_rule:
            campaign = {
                "spend": spend_threshold,
                "visits": visits_threshold,
                "rule": segment_rule,
                "status": "Created",
                "created_at": datetime.now()
            }
            campaigns.append(campaign)
            st.success("Campaign Created Successfully!")
        else:
            st.error("Please enter a valid segmentation rule.")

# Campaign Delivery & Logging
def campaign_delivery():
    st.subheader("Campaign Delivery & Logging")
    for campaign in campaigns:
        if st.button(f"Send Campaign with Spend: {campaign['spend']}"):
            result = send_message("Customer")
            delivery_status = "Sent" if result else "Failed"
            campaign["status"] = delivery_status

            st.write(f"Message Sent/Failed for Audience! Status: {delivery_status}")
            log_entry = {
                "campaign_id": len(campaigns),
                "status": delivery_status,
                "delivery_time": datetime.now()
            }
            st.write(f"Logged: {log_entry}")

# Display Campaign History
def show_campaign_history():
    st.subheader("Campaign History")
    if campaigns:
        for campaign in campaigns:
            st.write(f"Spend: {campaign['spend']}, Visits: {campaign['visits']}, Status: {campaign['status']}, Rule: {campaign['rule']}")
    else:
        st.write("No campaigns yet.")

# Authentication (Basic Session Handling)
def authenticate_user():
    st.subheader("Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid credentials!")
            return False
    return False

# Main App
def main():
    st.title("Mini CRM Platform")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        if not authenticate_user():
            return

    menu = ["Data Ingestion", "Create Campaign", "Campaign Delivery", "Campaign History"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Data Ingestion":
        ingest_data()
    elif choice == "Create Campaign":
        create_campaign()
    elif choice == "Campaign Delivery":
        campaign_delivery()
    elif choice == "Campaign History":
        show_campaign_history()

if __name__ == '__main__':
    main()
