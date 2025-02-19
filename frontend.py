import requests
import streamlit as st

st.title("LLM SQL Query Generator")

user_input = st.text_input("Enter your query in English:")

if st.button("Submit"):
    try:
        # Send request to Flask backend
        response = requests.post("http://127.0.0.1:5000/query", json={"prompt": user_input})
        
        # Debugging logs
        print("Response Status Code:", response.status_code)
        print("Raw Response:", response.text)
        
        if response.status_code != 200:
            st.error(f"Error {response.status_code}: {response.text}")
        else:
            data = response.json()
            #st.subheader("Generated SQL Query:")
            #st.code(data.get("query", ""), language="sql")
            
            st.subheader("Results:")
            results = data.get("results", [])
            
            if results:
                st.table(results)
            else:
                st.write("No results found.")
    
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend. Ensure Flask is running on port 5000.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {e}")
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
