import streamlit as st
from fpdf import FPDF
from datetime import date
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Firebase Authentication
web_api_key = "AIzaSyAFnX93fKXWLyH1sZ4loXu1-we28PrJcs0"
email = "moonnazole@gmail.com"
password = "12345678"

try:
    # Check if the user exists or create a new user
    user = auth.get_user_by_email(email)
    st.write(f"Authenticated as {user.email}")
except auth.UserNotFoundError:
    user = auth.create_user(
        email=email,
        email_verified=False,
        password=password,
        display_name="Moon Nazole",
    )
    st.write(f"New user created: {user.email}")

# Create the Streamlit form
st.title("Health Appointment Booking")

with st.form("appointment_form"):
    name = st.text_input("Name")
    birthdate = st.date_input("Birthdate")
    phone = st.text_input("Phone Number")
    ic = st.text_input("IC")
    email = st.text_input("Email")
    clinic = st.selectbox("Clinic", ["Clinic A", "Clinic B", "Clinic C"])
    appointment_date = st.date_input("Appointment Date", min_value=date.today())
    appointment_time = st.selectbox("Appointment Time", ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"])
    submitted = st.form_submit_button("Submit")

if submitted:
    # Data to send to Firestore
    data = {
        "name": name,
        "birthdate": str(birthdate),
        "phone": phone,
        "ic": ic,
        "email": email,
        "clinic": clinic,
        "appointment_date": str(appointment_date),
        "appointment_time": appointment_time,
        "created_at": firestore.SERVER_TIMESTAMP
    }

    # Store the data in Firestore
    try:
        db.collection("appointments").add(data)
        st.success("Appointment booked successfully!")
        st.write("### Appointment Receipt")
        st.markdown("---")
        st.write(f"Booking Date: {date.today()}")
        st.write("Thank you for booking your appointment!")
        st.write(f"Name: {name}")
        st.write(f"IC: {ic}")
        st.write(f"Email: {email}")
        st.write(f"Phone Number: {phone}")
        st.write(f"Birthdate: {birthdate}")
        st.write(f"Clinic: {clinic}")
        st.write(f"Appointment Date: {appointment_date}")
        st.write(f"Time: {appointment_time}")

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Appointment Receipt", ln=True, align="C")
        pdf.ln(5)
        pdf.line(10, 30, 200, 30)
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Booking Date: {date.today()}", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="Thank you for booking your appointment!", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Birthdate: {birthdate}", ln=True)
        pdf.cell(200, 10, txt=f"Phone Number: {phone}", ln=True)
        pdf.cell(200, 10, txt=f"IC: {ic}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
        pdf.cell(200, 10, txt=f"Clinic: {clinic}", ln=True)
        pdf.cell(200, 10, txt=f"Appointment Date: {appointment_date}", ln=True)
        pdf.cell(200, 10, txt=f"Time: {appointment_time}", ln=True)
        pdf_path = "appointment_receipt.pdf"
        pdf.output(pdf_path)

        # Download button
        with open(pdf_path, "rb") as file:
            st.download_button(label="Download Receipt", data=file, file_name="appointment_receipt.pdf")
    except Exception as e:
        st.error(f"Failed to save appointment: {e}")

# Optional: Cancel Appointment button
if st.button("Cancel Appointment"):
    st.warning("Your appointment has been canceled.")
    st.rerun()
