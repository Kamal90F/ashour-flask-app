# app.py

from flask import Flask, render_template, request
# Import the function from your renamed script (AiTool.py)
from AiTool import get_ai_response

app = Flask(__name__)

# --- ROUTE 1: The Homepage ---
# This just shows the form (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# --- ROUTE 2: The Logic ---
# This runs when the user clicks "Ask fake Mr. Ashour"
@app.route('/ask', methods=['POST'])
def ask_ashour():
    # 1. Get the question the user typed
    # The name 'user_question' must match the name="..." in your HTML input
    user_input = request.form['user_question']

    print(f"--- Received Question: {user_input} ---")

    # 2. Call your AI Script and pass the input to it
    # This runs the function you just modified in AiTool.py
    ai_answer = get_ai_response(user_input)

    # 3. Display the result
    # We return a simple HTML string with the question and the answer.
    return f"""
    <div style="font-family: Arial; padding: 20px;">
        <h1>Result</h1>
        <p><strong>You asked:</strong> {user_input}</p>
        <hr>
        <p><strong>AI Answer:</strong></p>
        <p>{ai_answer}</p>
        <br>
        <a href="/">Ask another question</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)