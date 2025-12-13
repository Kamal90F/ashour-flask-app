# my_script.py - REVISED

# The function now accepts one argument: the question from the user
def run_process(question):
    """
    Takes the user's question and generates a response.
    Replace this logic with your actual script that processes the question.
    """
    
    if "how are you" in question.lower():
        response = "I am a fake AI, but I feel excellent. What else can I help you with?"
    else:
        # Example of incorporating the input into the output
        response = f"Ah, the question you asked was: '{question}'. As fake Mr. Ashour, I decree that the answer is: 42."
        
    return response