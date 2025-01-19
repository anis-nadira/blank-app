import streamlit as st
from fpdf import FPDF

# Create the Streamlit form
st.title("Health Appointment Booking")

with st.form("appointment_form"):
    name = st.text_input("Name")
    birthdate = st.date_input("Birthdate")
    phone = st.text_input("Phone Number")
    ic = st.text_input("IC")
    email = st.text_input("Email")
    time = st.selectbox("Appointment Time", ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"])
    date = st.date_input("Appointment Date")
    
    submitted = st.form_submit_button("Submit")

if submitted:
    # Display receipt
    st.success("Appointment booked successfully!")
    st.write("### Appointment Receipt")
    st.write(f"*Name:* {name}")
    st.write(f"*IC:* {ic}")
    st.write(f"*Email:* {email}")
    st.write(f"*Phone Number:* {phone}")
    st.write(f"*Birthdate:* {birthdate}")
    st.write(f"*Date:* {date}")
    st.write(f"*Time:* {time}")

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Appointment Receipt", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Birthdate: {birthdate}", ln=True)
    pdf.cell(200, 10, txt=f"Phone Number: {phone}", ln=True)
    pdf.cell(200, 10, txt=f"IC: {ic}", ln=True)
    #pdf.cell(200, 10, txt=f"Clinic: {clinic}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Time: {time}", ln=True)
    pdf.output("appointment_receipt.pdf")

    # Download button
    with open("appointment_receipt.pdf", "rb") as file:
        st.download_button(label="Download Receipt", data=file, file_name="appointment_receipt.pdf")
