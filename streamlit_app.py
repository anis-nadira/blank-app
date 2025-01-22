import streamlit as st
from fpdf import FPDF
from datetime import date

# Initialize session state for appointments
if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Function to display appointments
def display_appointments():
    st.write("### Your Appointments")
    if st.session_state.appointments:
        for idx, appt in enumerate(st.session_state.appointments):
            st.write(f"**{idx + 1}.** {appt['date']} at {appt['time']} - {appt['name']} ({appt['email']})")
            cancel_button = st.button(f"Cancel Appointment {idx + 1}", key=f"cancel_{idx}")
            if cancel_button:
                st.session_state.appointments.pop(idx)
                st.success("Appointment cancelled!")
                # Set a flag to avoid multiple reruns
                st.session_state.cancelled = True
                return  # Exit loop to avoid issues with state changes
    else:
        st.info("No appointments booked yet.")

# Main content
st.title("Health Appointment Booking")

# Add new appointment button
if st.button("Add New Appointment"):
    st.session_state.show_form = True

# Display the form if the user wants to add a new appointment
if st.session_state.show_form:
    with st.form("appointment_form"):
        name = st.text_input("Name")
        birthdate = st.date_input("Birthdate")
        phone = st.text_input("Phone Number")
        ic = st.text_input("IC")
        email = st.text_input("Email")
        appt_date = st.date_input("Appointment Date", min_value=date.today())
        appt_time = st.selectbox("Appointment Time", ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"])
        submitted = st.form_submit_button("Submit")

    if submitted:
        appointment = {
            "name": name,
            "birthdate": str(birthdate),
            "phone": phone,
            "ic": ic,
            "email": email,
            "date": str(appt_date),
            "time": appt_time,
        }
        st.session_state.appointments.append(appointment)
        st.success("Appointment booked successfully!")
        st.session_state.show_form = False

# Display existing appointments
display_appointments()

# Check if a cancellation occurred to rerun the script
if "cancelled" in st.session_state and st.session_state.cancelled:
    st.session_state.cancelled = False
    st.experimental_rerun()

# Generate PDF for the latest appointment if available
if st.session_state.appointments:
    latest_appt = st.session_state.appointments[-1]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Appointment Receipt", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Booking Date: {date.today()}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Thank you for booking your appointment!", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {latest_appt['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Birthdate: {latest_appt['birthdate']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone Number: {latest_appt['phone']}", ln=True)
    pdf.cell(200, 10, txt=f"IC: {latest_appt['ic']}", ln=True)
    pdf.cell(200, 10, txt=f"Appointment Date: {latest_appt['date']}", ln=True)
    pdf.cell(200, 10, txt=f"Time: {latest_appt['time']}", ln=True)
    pdf_path = "appointment_receipt.pdf"
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as file:
        st.download_button(label="Download Receipt", data=file, file_name="appointment_receipt.pdf")
