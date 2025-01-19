import streamlit as st
from fpdf import FPDF
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Function to send email
def send_confirmation_email(recipient_email, pdf_path):
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_email_password"  # Replace with your email password
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server (e.g., Gmail)
    smtp_port = 587  # SMTP port for TLS

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Appointment Confirmation"

    # Email body
    body = "Thank you for booking your appointment. Please find your receipt attached."
    message.attach(MIMEText(body, "plain"))

    # Attach the PDF file
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=appointment_receipt.pdf")
        message.attach(part)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(message)
            st.success(f"Confirmation email sent successfully to {recipient_email}!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")


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
    reminder = st.checkbox("Send me a reminder for this appointment")
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
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    pdf.cell(200, 10, txt=f"Time: {time}", ln=True)
    pdf_path = "appointment_receipt.pdf"
    pdf.output(pdf_path)

    # Download button
    with open(pdf_path, "rb") as file:
        st.download_button(label="Download Receipt", data=file, file_name="appointment_receipt.pdf")

    # Send confirmation email
    if reminder and email:
        send_confirmation_email(email, pdf_path)
