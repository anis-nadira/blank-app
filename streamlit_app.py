import streamlit as st
from fpdf import FPDF
from datetime import date

# Create the Streamlit form
st.title("Health Appointment Booking")

with st.form("appointment_form"):
    name = st.text_input("Name")
    birthdate = st.date_input("Birthdate")
    phone = st.text_input("Phone Number")
    ic = st.text_input("IC")
    email = st.text_input("Email")
    date = st.date_input("Appointment Date", min_value=date.today())
    time = st.selectbox("Appointment Time", ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"])
    submitted = st.form_submit_button("Submit")

if submitted:
    # Display receipt in Streamlit
    st.success("Appointment booked successfully!")
    st.write("### Appointment Receipt")
    st.markdown("---")  # Fine straight line under the title
    st.write(f"*Booking Date:* {date.today()}")
    st.write("**Thank you for booking your appointment!**")  # Thank you message
    
    # Display appointment details
    st.write(f"*Name:* {name}")
    st.write(f"*IC:* {ic}")
    st.write(f"*Email:* {email}")
    st.write(f"*Phone Number:* {phone}")
    st.write(f"*Birthdate:* {birthdate}")
    st.write(f"*Appointment Date:* {date}")
    st.write(f"*Time:* {time}")

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Appointment Receipt", ln=True, align="C")
    pdf.ln(5)  # Adds space between title and line
    pdf.line(10, 30, 200, 30)  # Fine straight line under title
    pdf.ln(10)
    
    # Smaller font for the booking date below the line
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Booking Date: {date.today()}", ln=True, align="C")
    pdf.ln(10)  # Adds space before other details

    # Thank you message in the PDF
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Thank you for booking your appointment!", ln=True, align="C")
    pdf.ln(10)  # Adds space before details

    # Details in the PDF
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Birthdate: {birthdate}", ln=True)
    pdf.cell(200, 10, txt=f"Phone Number: {phone}", ln=True)
    pdf.cell(200, 10, txt=f"IC: {ic}", ln=True)
    pdf.cell(200, 10, txt=f"Appointment Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Time: {time}", ln=True)
    pdf_path = "appointment_receipt.pdf"
    pdf.output(pdf_path)

    # Download button
    with open(pdf_path, "rb") as file:
        st.download_button(label="Download Receipt", data=file, file_name="appointment_receipt.pdf")

    
    # Cancel appointment button
    if st.button("Cancel Appointment"):
        st.session_state.submitted = False
        st.warning("Your appointment has been canceled.")
        st.rerun()

