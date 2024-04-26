import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            print(bytes_data)
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")
            # Calculating hash
            # data_to_hash = f"{customer_id}{customer_name}{energy_source}{capacity_generated}{powerhouse_id}{powerhouse_name}{date_of_claim}".encode('utf-8')
            certificate_id = hashlib.sha256(bytes_data).hexdigest()
            # Smart Contract Call

            result = contract.functions.isVerified(certificate_id).call()

            if result:
                st.success("Certificated validated successfully!")
            else:
                st.error("Invalid Certificate! Certificate might be tampered")
        except Exception as e:
            st.error("Invalid Certificate! Certificate might be tampered")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Validate")
    if submit:
        try:
            view_certificate(certificate_id)
            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificated validated successfully!")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")