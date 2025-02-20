import google.generativeai as genai
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="#########")  # Replace with your actual API key

# Function to generate an SQL query from English input using Gemini Pro
def generate_sql_query(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"""
        Convert this request into an SQL query for a SQLite database.
        Table Name: students
        Columns: id (INTEGER), name (TEXT), department (TEXT), age (INTEGER)
        Ensure the SQL query matches this structure exactly.
        Convert this English sentence into an SQL query for the 'students' table. 
        Make sure to use correct column names like 'name' and 'department'. 
        Use WHERE for filtering. 
        Ignore case censitive data in table like ECE in table is same as ece.   



        User Request: {prompt}
        """
    )

    sql_query = response.text.strip() if response.text else None
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    print("Generated SQL Query:", sql_query)  # Debugging print
    return sql_query


# Function to execute the SQL query on SQLite
def execute_sql_query(query):
    try:
        # Prevent dangerous queries
        forbidden_keywords = ["drop", "delete", "update", "insert"]
        if any(keyword in query.lower() for keyword in forbidden_keywords):
            return "Unsafe query detected!"

        conn = sqlite3.connect("records.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        return results
    except Exception as e:
        return str(e)  # Return error message if query fails

# Route to process user input and return query + results
@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    prompt = data.get("prompt")

    # Generate SQL query using Gemini Pro
    sql_query = generate_sql_query(prompt)

    if not sql_query:
        return jsonify({"error": "Failed to generate SQL query"}), 500

    # Execute the generated SQL query
    results = execute_sql_query(sql_query)

    return jsonify({"query": sql_query, "results": results})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
