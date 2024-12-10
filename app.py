import streamlit as st
import requests
import time

def inject_css(css):
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

css = """
<style>
/* Base styles for inputs, selects, and text areas */
.stTextInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea, .stSelectbox > div > select {
    color: #333 !important;
    vertical-align: middle !important;
    background-color: #fff !important;
    border: 1px solid #ccc !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    width: 100% !important;
    height: 38px !important;
    margin-bottom: 10px !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    line-height: 1.42857 !important;
    display: block !important;
    box-sizing: border-box !important;
}

/* Specific styles for Streamlit input labels */
.stTextInput > label, .stSelectbox > label, .stDateInput > label, .stRadio > label, .stLabel > label {
    color: #333333 !important;
    font-size: 14px !important;
    font-family: Arial, sans-serif !important;
    margin: 0px 0px 5px 0px !important;
    font-weight: bold !important;
    display: block !important;
}

/* Style for the dropdown arrow in the select element */
.stSelectbox > div > div[class^="select"]::after {
    border-color: #333 transparent transparent !important;
}

/* Style for the select element when it is focused */
.stSelectbox select:focus {
    outline: none !important;
}

/* Modify the submit button styling */
button, .stButton > button {
    background-color: #308133 !important;
    border: none !important;
    color: white !important;
    padding: 15px 20px !important;
    margin-top: 20px !important;
    font-size: 14px !important;
    line-height: 1.42857 !important;
    display: block !important;
    width: 100% !important;
    box-sizing: border-box !important;
    border-radius: 0 !important;
}

/* Global font style */
* {
    font-family: Arial, sans-serif !important;
}

/* Custom styles for support and oppose dropdown */
.support-select select {
    background-color: #d4edda !important;
    color: #155724 !important;
}

.oppose-select select {
    background-color: #f8d7da !important;
    color: #721c24 !important;
}

/* Status message styles */
.status-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 4px;
}

.status-processing {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
}

.status-completed {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status-failed {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
</style>
"""

def check_status(base_url, submission_id):
    """Check the status of a submitted request."""
    try:
        response = requests.get(f"{base_url}/bill-status/{submission_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error checking status: {str(e)}")
        return None

def display_status_message(status_data):
    """Display a formatted status message based on the status response."""
    if not status_data:
        return

    status = status_data.get('status', '').lower()
    message = status_data.get('message', 'Processing request...')
    
    if status == 'processing':
        st.markdown(f'<div class="status-message status-processing">{message}</div>', unsafe_allow_html=True)
    elif status == 'completed':
        st.markdown(f'<div class="status-message status-completed">{message}</div>', unsafe_allow_html=True)
    elif status == 'failed':
        st.markdown(f'<div class="status-message status-failed">{message}</div>', unsafe_allow_html=True)
    else:
        st.info(message)

def main():
    inject_css(css)

    # Initialize session state for tracking submissions
    if 'submission_id' not in st.session_state:
        st.session_state.submission_id = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # Columns for Name and Email
    col1, col2 = st.columns([1, 1])
    with col1:
        name = st.text_input("Name")
    with col2:
        email = st.text_input("Email Address")

    # Columns for Member Organization and Year
    col1, col2 = st.columns([1, 1])
    with col1:
        member_org = st.text_input("Member Organization (If None Leave Blank)")
    with col2:
        years = [str(year) for year in range(2025, 2017, -1)]
        selected_year = st.selectbox("Year", options=years, index=0)

    # Columns for Type and Link button
    col1, col2 = st.columns([1, 1])
    with col1:
        legislation_type = st.selectbox("Type", options=["Florida Bills", "Federal Bills"])
    with col2:
        link = None
        if legislation_type == "Federal Bills":
            if st.button("Federal Bills Website"):
                link = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%7D"
        else:
            if st.button("Florida Bills Website"):
                link = "https://www.flsenate.gov/Session/Bills/2024"

        if link:
            st.markdown(f'[Click here to visit the website]({link})')

    if legislation_type == "Federal Bills":
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            sessions = [str(i) for i in range(118, 99, -1)]
            session = st.selectbox("Congress Session Number", options=sessions, index=0)
        with col2:
            bill_number = st.text_input("Bill Number")
        with col3:
            federal_bill_type = st.selectbox("Bill Prefix", options=["HR", "S", "H.Res", "S.Res", "H.J.Res", "S.J.Res", "H.Con.Res", "S.Con.Res"])
    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            bill_type = st.selectbox("Bill Prefix", options=["HB", "SB"])
        with col2:
            bill_number = st.text_input("Bill Number")

    # Support or Oppose section
    support = st.selectbox("Organization's Position", options=["N/A", "Support", "Oppose"], key="support_oppose", index=0)

    # Apply custom class based on selection
    support_class = "support-select" if support == "Support" else "oppose-select"
    inject_css(f".stSelectbox select {{ background-color: {'#d4edda' if support == 'Support' else '#f8d7da'} !important; color: {'#155724' if support == 'Support' else '#721c24'} !important; }}")

    if st.button("SUBMIT"):
        with st.spinner("Submitting request..."):
            form_data = {
                "name": name,
                "email": email,
                "member_organization": member_org,
                "year": selected_year,
                "legislation_type": legislation_type,
                "session": session if legislation_type == "Federal Bills" else "N/A",
                "bill_number": bill_number,
                "bill_type": federal_bill_type if legislation_type == "Federal Bills" else bill_type,
                "support": support,
                "lan": "en"
            }

            base_url = "http://3.226.54.104:8080"
            api_url = f"{base_url}/process-federal-bill/" if legislation_type == "Federal Bills" else f"{base_url}/update-bill/"

            try:
                response = requests.post(api_url, json=form_data)
                if response.status_code == 202:  # Accepted
                    response_data = response.json()
                    st.session_state.submission_id = response_data.get('submission_id')
                    st.session_state.processing = True
                    
                    # Display initial status message
                    st.info(response_data.get('message'))
                    st.info(response_data.get('note', ''))
                    
                    # Create a placeholder for status updates
                    status_placeholder = st.empty()
                    
                    # Poll for status updates
                    while st.session_state.processing:
                        status_data = check_status(base_url, st.session_state.submission_id)
                        if status_data:
                            with status_placeholder:
                                display_status_message(status_data)
                            
                            if status_data.get('status').lower() in ['completed', 'failed']:
                                st.session_state.processing = False
                                break
                        
                        time.sleep(5)  # Wait 5 seconds before checking again
                        
                else:
                    st.error(f"Request failed with status code: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")

    # Display current status if there's an ongoing process
    if st.session_state.submission_id and st.session_state.processing:
        status_data = check_status(base_url, st.session_state.submission_id)
        if status_data:
            display_status_message(status_data)

if __name__ == "__main__":
    main() 