import spacy
import tensorflow as tf
from tensorflow.keras import layers
from flask import Flask, request, jsonify, render_template_string

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Create Flask app
app = Flask(__name__)

# Default route to prevent 404 errors on GET /
@app.route('/')
def home():
    return "Flask API is running. Use a POST request to /parse to analyze sentences."

# Sentence-to-logical-form function
def sentence_to_logical_form(sentence):
    doc = nlp(sentence)

    subject = ""
    verb = ""
    obj = ""

    for token in doc:
        if "subj" in token.dep_:
            subject = token.text
        if "VERB" in token.pos_:
            verb = token.text
        if "obj" in token.dep_:
            obj = token.text

    return f"({subject}, {verb}, {obj})"

# HTML Template for the web interface
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Sentence Parser</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        input, button { font-size: 18px; padding: 10px; }
        button { cursor: pointer; }
    </style>
</head>
<body>
    <h2>Sentence Parser</h2>
    <form method="post">
        <label>Enter a sentence:</label><br>
        <input type="text" name="sentence" required><br><br>
        <button type="submit">Parse</button>
    </form>
    {% if sentence %}
        <h3>Input Sentence:</h3>
        <p>{{ sentence }}</p>
        <h3>Logical Form:</h3>
        <p>{{ logical_form }}</p>
    {% endif %}
</body>
</html>
"""

# Route to parse a sentence and display results in the browser
@app.route('/parse', methods=['GET', 'POST'])
def parse_sentence():
    if request.method == 'POST':
        sentence = request.form.get('sentence', '')

        if not sentence:
            return render_template_string(html_template, sentence=None, logical_form="No sentence provided.")

        logical_form = sentence_to_logical_form(sentence)
        return render_template_string(html_template, sentence=sentence, logical_form=logical_form)

    return render_template_string(html_template, sentence=None, logical_form=None)

# Run Flask app
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
