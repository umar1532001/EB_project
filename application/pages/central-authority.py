import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
import pyrebase
import time
from datetime import datetime

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

# Load environment variables
load_dotenv()

# Initialize Firebase
firebaseConfig = {
   "apiKey": "AIzaSyAIeaWiceVeYOWQSjTu1nSNNq_xDbcivpE",
  "authDomain": "recmpr-c4916.firebaseapp.com",
  "projectId": "recmpr-c4916",
  "storageBucket": "recmpr-c4916.appspot.com",
  "messagingSenderId": "289811255339",
  "appId": "1:289811255339:web:9dedb735efaf22dc815a6e",
  "measurementId": "G-N709H0H235",
  "databaseURL":"https://recmpr-c4916-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

# Get a reference to the database service
db = firebase.database()

# Initialize counters
transaction_count = 0
block_size = 6  # Define the size of each block

# Streamlit app
st.title('Certificate Requests')

# Retrieve all data from Firebase
all_data = db.child("users").get()

options = ("Validate Certificate", "View Certificates")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    if all_data:
        for user in all_data.each():
            if user.val()['status'] != 'Accepted' and user.val()['status'] != 'Rejected':
                customer_id = user.val()['customer_id']
                customer_name = user.val()['customer_name']
                energy_source = user.val()['energy_source']
                capacity_generated = user.val()['capacity_generated']
                powerhouse_id = user.val()['powerhouse_id']
                powerhouse_name = user.val()['powerhouse_name']
                date_of_claim = user.val()['date_of_claim']

                st.write("Transaction ID:", hashlib.sha256(f"{customer_id}-{datetime.now()}".encode()).hexdigest()[:8])

                accept_key = f"accept_{user.key()}"
                reject_key = f"reject_{user.key()}"

                accept = st.button("Accept", key=accept_key)
                reject = st.button("Reject", key=reject_key)

                if accept:
                    transaction_count += 1
                    # Your certificate generation and blockchain interaction code here
                    # ...
                    st.success("Certificate accepted!")

                    if transaction_count >= block_size:
                        st.info("Block completed!")
                        transaction_count = 0

                elif reject:
                    st.warning(f"{customer_name} has been rejected!")

                st.write("-" * 30)

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
