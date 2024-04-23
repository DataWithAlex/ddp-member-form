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
</style>
"""

def main():
    inject_css(css)

    name = st.text_input("Name")
    email = st.text_input("Email Address")
    member_org = st.text_input("Member Organization")

    current_year = "2024"
    selected_year = st.text_input("Year", value=current_year)

    # Create three columns for "Bill", "Bill Number" and "Support or Oppose"
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        bill_type = st.selectbox("Bill", options=["HB", "SB"])
    with col2:
        bill_number = st.text_input("Bill Number")
    with col3:
        # Convert the radio buttons to a select box
        support = st.selectbox("Support or Oppose", options=["Support", "Oppose"])

    if st.button("SUBMIT"):
        with st.spinner(text="Loading, please wait..."):
            form_data = {
                "name": name,
                "email": email,
                "member_organization": member_org,
                "year": selected_year,
                "bill_type": bill_type,
                "bill_number": bill_number,
                "support": support
            }
            response = call_api(form_data)
        st.success("Complete")

def call_api(data):
    api_url = "http://3.226.54.104:8080/update-bill/"

    try:
        year = data.get("year")
        bill_number = data.get("bill_number")

        if not year or not bill_number:
            return {"error": "Year and bill_number are required."}

        params = {"year": year, "bill_number": bill_number}
        response = requests.post(api_url, params=params, json=data)

        print(response.content)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": f"Error occurred: {str(e)}"}

if __name__ == "__main__":
    main()
