import streamlit as st
import requests
import time

def main():
    #st.set_page_config(page_title='Member Portal Bill Voting', layout='wide', theme={"base": "light"})
    st.title("Member Portal Bill Voting")

    # Text input fields
    name = st.text_input("Name")
    email = st.text_input("Email Address")
    member_org = st.text_input("Member Organization")

    # Create a horizontal layout for "Bill" dropdown and "Bill Number" text input
    col1, col2 = st.columns([1, 1])  # Adjust column width as needed
    with col1:
        # Dropdown for bill type
        bill_type = st.selectbox("Bill", options=["HB", "SB"])

    with col2:
        # Text input field for bill number
        bill_number = st.text_input("Bill Number")

    # Text input field for year
    current_year = "2024"
    selected_year = st.text_input("Year", value=current_year)

    # Radio button for support or oppose
    support = st.radio("Support or Oppose", options=["Support", "Oppose"])

    # Submit button
    if st.button("Submit"):
        # Display a spinner while processing
        with st.spinner(text="Loading, please wait..."):
            # Package the form data into a dictionary
            form_data = {
                "name": name,
                "email": email,
                "member_organization": member_org,
                "year": selected_year,
                "bill_type": bill_type,
                "bill_number": bill_number,
                "support": support
            }

            # Call the FastAPI API
            response = call_api(form_data)

        # After API call completes, update message to "Complete"
        st.success("Complete")

        # Package the form data into a dictionary


        # Call the FastAPI API (commented out for testing)
        #response = call_api(form_data)

        # Display response
        #st.write("API Response:")
        #st.json(response)

def call_api(data):
    # Define API endpoint
    api_url = "http://54.242.92.10:8080/update-bill/"

    try:
        # Extract year and bill_number from data
        year = data.get("year")
        bill_number = data.get("bill_number")

        # Check if year and bill_number are present
        if not year or not bill_number:
            return {"error": "Year and bill_number are required."}

        # Construct query parameters
        params = {"year": year, "bill_number": bill_number}

        # Make POST request to API with query parameters
        response = requests.post(api_url, params=params, json=data)

        # Print response content for debugging
        print(response.content)

        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": f"Error occurred: {str(e)}"}

if __name__ == "__main__":
    main()
