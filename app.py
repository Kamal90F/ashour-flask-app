# app.py - REVISED

from flask import Flask, render_template, request 
# We need to import 'request' to handle form data

from my_script import run_process 

app = Flask(__name__)

# --- WEB ADDRESSES (ROUTES) ---

# ROUTE 1: Homepage (URL: /) - Now handles both GET (initial load) and POST (form submission)
@app.route('/', methods=['GET'])
def index():
    # Renders the HTML page with the text field
    return render_template('index.html')

# ROUTE 2: Action (URL: /ask) - Specifically handles the form submission
@app.route('/ask', methods=['POST'])
def ask_ashour():
    # 1. Check if the request is a form submission (which it should be)
    if request.method == 'POST':
        
        # 2. Extract the data from the text field named 'user_question'
        user_question = request.form['user_question']
        
        print(f"--- Question Received: {user_question} ---")
        
        # 3. Call your Python script and pass the user's question to it
        ashour_answer = run_process(user_question)
        
        # 4. Return the result back to the user
        return f"""
        <h1>Fake Mr. Ashour's Answer</h1>
        <p><strong>Your Question:</strong> {user_question}</p>
        <hr>
        <p><strong>Mr. Ashour's Response:</strong> {ashour_answer}</p>
        <p><a href='/'>Ask another question</a></p>
        """

# --- SERVER EXECUTION ---
if __name__ == '__main__':
    app.run(debug=True)