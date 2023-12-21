import streamlit as st
import boto3
from jinja2 import Environment, FileSystemLoader
import uuid
import os
from dotenv import load_dotenv


load_dotenv()

# Get AWS S3 credentials from environment variables
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")

# Load HTML template
env = Environment(loader=FileSystemLoader("."))
html_template = env.get_template("report_template.html")

def save_html_to_s3(lead_data, html_content):
    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION
    )

    # Generate a unique identifier for the report
    report_id = str(uuid.uuid4().hex[:6])
    
    # Save HTML content to S3 bucket
    html_file_path = f"lead_reports/report_{report_id}.html"
    s3.put_object(Body=html_content.encode(), Bucket=S3_BUCKET_NAME, Key=html_file_path)

    # Generate a direct link for the uploaded HTML
    html_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{html_file_path}"

    return html_url

def main():
    st.title("Lead Report Generator")

    # User input form
    lead_name = st.text_input("Lead Name")
    company_name = st.text_input("Company Name")
    lead_position = st.text_input("Position")
    logo_path = st.text_input("Image URL")
    lead_phone = st.text_input("Lead Phone No")
    lead_email = st.text_input("Lead Email")
    lead_linkedin = st.text_input("Person Linkedin URL")
    lead_location = st.text_input("Lead Location")
    meeting_date = st.text_input("Meeting Date ( Web, 10 Dec 2023)")
    meeting_time = st.text_input("Meeting Time (10:00 Dubai Time)")
    company_location = st.text_input("Company Location")
    company_linkedin = st.text_input("Company Linkedin URL")
    company_category = st.text_input("Company Category")
    website = st.text_input("Wesbite")
    lead_rating = st.text_input("Lead Rating")
    company_size = st.text_input("company_size")
    decision_maker = st.text_input("Decision Maker")
    have_the_budget = st.text_input("Have the Budget (Yes/No)")
    need = st.text_input("Need")
    revenue = st.text_input("Revenue")
    about_lead = st.text_area("About Lead")
    about_company = st.text_area("About Company")
    comment = st.text_area("Comment")
    pitch = st.text_area("pitch")
    note = st.text_area("note")
    lead_company_logo = st.text_input("Upload Company Image (Path)")

    if st.button("Generate Report"):
        lead_data = {
            "lead_name": lead_name,
            "company_name": company_name,
            "logo_path": logo_path,
            "lead_position": lead_position,
            "lead_phone": lead_phone,
            "lead_email": lead_email,
            "lead_linkedin": lead_linkedin,
            "lead_location": lead_location,
            "meeting_date": meeting_date,
            "meeting_time": meeting_time,
            "company_location": company_location,
            "company_linkedin": company_linkedin,
            "company_category": company_category,
            "website": website,
            "lead_rating": lead_rating,
            "company_size": company_size,
            "decision_maker": decision_maker,
            "have_the_budget": have_the_budget,
            "need": need,
            "revenue": revenue,
            "about_lead": about_lead,
            "about_company": about_company,
            "comment": comment,
            "pitch": pitch,
            "note": note,
            "lead_company_logo": lead_company_logo
        }

        # Render HTML template with lead data
        html_content = html_template.render(**lead_data)

        # Save HTML content to S3 and get direct URL
        html_url = save_html_to_s3(lead_data, html_content)

        # Display link to the user
        st.balloons()
        st.success("Report generated successfully!")
        st.markdown(f"View your report [here]({html_url})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

