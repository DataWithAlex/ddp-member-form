import streamlit as st
import requests

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
    border-radius: 0 !important; /* Make input boxes square */
    box-shadow: none !important; /* Remove shadows */
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
    color: #333333 !important; /* Font color */
    font-size: 14px !important; /* Font size */
    font-family: Arial, sans-serif !important; /* Font family */
    margin: 0px 0px 5px 0px !important; /* Margin around the label */
    font-weight: bold !important; /* Bold font weight */
    display: block !important; /* Ensure the label is displayed as a block */
}

/* Style for the dropdown arrow in the select element */
.stSelectbox > div > div[class^="select"]::after {
    border-color: #333 transparent transparent !important; /* Adjust the color as needed */
}

/* Style for the select element when it is focused */
.stSelectbox select:focus {
    outline: none !important;
}

/* Modify the submit button styling */
button, .stButton > button {
    background-color: #308133 !important; /* The green background */
    border: none !important;
    color: white !important;
    padding: 15px 20px !important;
    margin-top: 20px !important;
    font-size: 14px !important;
    line-height: 1.42857 !important;
    display: block !important;
    width: 100% !important;
    box-sizing: border-box !important;
    border-radius: 0 !important; /* Make the button square */
}

/* Global font style */
* {
    font-family: Arial, sans-serif !important; /* Use Arial font for consistency */
}

/* Custom styles for support and oppose dropdown */
.support-select select {
    background-color: #d4edda !important; /* Light green background */
    color: #155724 !important; /* Dark green text */
}

.oppose-select select {
    background-color: #f8d7da !important; /* Light red background */
    color: #721c24 !important; /* Dark red text */
}
</style>
"""

def main():
    inject_css(css)

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
        current_year = "2024"
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
    support = st.selectbox("Organization’s Position", options=["N/A", "Support", "Oppose"], key="support_oppose", index=0)

    # Apply custom class based on selection
    support_class = "support-select" if support == "Support" else "oppose-select"
    inject_css(f".stSelectbox select {{ background-color: {'#d4edda' if support == 'Support' else '#f8d7da'} !important; color: {'#155724' if support == 'Support' else '#721c24'} !important; }}")

    if st.button("SUBMIT"):
        with st.spinner(text="Loading, please wait... This process may take a few minutes, so do not click Submit again"):
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
                "lan": "en"  # Default language to "en"
            }

            response = call_api(form_data, legislation_type)
            if "error" in response and response["error"] != "Error occurred: Expecting value: line 1 column 1 (char 0)":
                st.error(response["error"])
            else:
                st.success("Complete")
                if "url" in response:
                    st.markdown(f"### [View the bill details here]({response['url']})")

def call_api(data, legislation_type):
    if legislation_type == "Federal Bills":
        api_url = "http://3.226.54.104:8080/process-federal-bill/"
    else:
        api_url = "http://3.226.54.104:8080/update-bill/"

    try:
        response = requests.post(api_url, json=data)
        print(response.content)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        if str(e) == "Expecting value: line 1 column 1 (char 0)":
            return {"success": "Complete"}
        else:
            return {"error": f"Error occurred: {str(e)}"}

if __name__ == "__main__":
    main()
