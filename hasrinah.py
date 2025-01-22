import streamlit as st
from fpdf import FPDF
from datetime import date
import firebase_admin
from firebase_admin import credentials, db, auth

# Firebase Admin SDK credentials embedded directly
firebase_creds = {
    "type": "service_account",
    "project_id": "cloud-project-e22b5",
    "private_key_id": "9fcb9ef8925acc11116a530ee832f3b9329f1f0a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCnbrko/0qCA2/v\nlMMUlQA2OngO0IO4qcTj7Tvcn5NS5BSNd12klB0zQRofOqOZsEUjH2c1xpBZq3KR\nTISIS3xNChyB5y0drk6o9R2uWkRIMh6RNFAR7PsPVCbqLMfDUKsuMh9cnVbUBhUG\nXOsmRjCB4ntP+4Pm1wihEvr3QzW7CZnrlu3xor2AW8neOTBM0WACjdtVi1swT38N\noFocd2JmoiUa+jJ2ppxtwh027ubLBd3fh9es8rsS8XYo2ao7B1spQ67IQF+haHLJ\n0f7bgPAmuhF0kYlcRqmJU8WtJUcM+V4HB7O4oZxkBsutw2uAcfrvjh8GMPk38RA5\ncOP33b/HAgMBAAECggEAOP1MEvNKRhSrbg3hlMjeqJagNNKucxV+CeK+5GqAd89g\nW4KMoi8z/TUkkgqgkvhXoAvZUomCqrLbrS8xUT74UTSm3WR1i8u/xGyiLK1W3ogI\ntX3r3x4dmmsXT8/sMsPrcC7pU9nOKx7i2yaXd5CehCc1t9SxYcpBiqnuOGltCXs/\nEnd8GMR2Js2Kh4fNKXFS8sjeg3u0Qq+Oycng8zpTGpq8s7TZd2xpmR5cv1FCKQuh\n7dPA2MmfHHRhJYcUvpRuC5WhRQq0M0HBsKVTS1b4PhYFM1oF9OXie0hAG3W3WiL+\nLK9G3TDVxNj1Id/FHUhboRm6cbGU6V3ELNdEISNMcQKBgQDYFOHyOL/3l66gjKv/\nIRSClNKSdiOoH+jspxlx/9qxPxCfgeamnjmGq+kHfZ9YJ79YVP0bMojlwOfi4SLl\n4Wl96QuYCRTxECvJ99YtIYm+qaNMYDqyRTEJK3Ywcar5SQYM0O3iAkqE/Ba85mad\njHRt9R82RnoTfRuHmiojL9dk3wKBgQDGXRZLjzKjE1ZIWXRw/6+7TwAXt0sOyfwU\nH6pHhhkrtbzXUKTDrJC9yTF2+h3ttAtrXsCZDm2lATRrrUC+EKMrqu2/Yc+Yr30f\nOi0Ta46allJ3QUQbgyV4ggHa09OaNdBD6gIjMCQIwSgwKj4j4ut89rMJiBbDRHAL\nE6yyVvHaGQKBgE8cRiTidhX16K9LEWWU/OdaCUYqDp/tHuAVxZEhNTYTesiLTKDP\n6QvPQL/HVGF4G+wBIbGlbM2BNOSxvI8hWfgJLH97Q7mGTCHjpPxc/QtbHDhIOvUt\ns+hBi0HtO8WM4LQsggtu/0105fY+/G7OD4p6ZfT/FI6yDTQ2UxsS1u9NAoGAchfS\nng00Q+X4Z87EEcaPDj5nQDzV+CCnU+/Ooir4SVLT1kh1LHMSIYcaY2ODWViIhO5P\n+vj4icLCovhY17l8EL7U1pJstFajshVlHdlsgW/a6OrqQKTTJZgpdvMFr5oqOxXa\nuuCSqVJoSiPR8BQx/INtARt8dD3l8AkV+NHXc+kCgYAz+AV2/BQxMFladFhNfH93\nwQVNQusbOibGmnECqaMaE1boAmgIN+7nClmDRC2WYJ5WEkb2yT6RZSqoxfS9edtg\ngClI3RpmWZUgYArE7wlvfSxqg77C8xR+kiiIwJeRJWNcOKYDq/mqTIsj04jJmsNZ\nuGAInBuxzF5G5RELyfH6fw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-d4sdc@cloud-project-e22b5.iam.gserviceaccount.com",
    "client_id": "110215200426610128996",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-d4sdc%40cloud-project-e22b5.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://cloud-project-e22b5-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Access the database
ref = db.reference('appointments')

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
    # Data to send to Firebase Realtime Database
    data = {
        "name": name,
        "birthdate": str(birthdate),
        "phone": phone,
        "ic": ic,
        "email": email,
        "clinic": clinic,
        "date": str(appointment_date),
        "time": appointment_time
    }

    # Store the data in Firebase Realtime Database
    try:
        ref.push(data)
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

        # Cancel appointment button
    if st.button("Cancel Appointment"):
        st.session_state.submitted = False
        st.warning("Your appointment has been canceled.")
        st.rerun()

