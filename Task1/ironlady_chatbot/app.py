from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

# Load FAQs
with open('faqs.json') as f:
    faqs = json.load(f)

def find_faq_answer(user_input):
    user_input_lower = user_input.lower()
    for faq in faqs:
        # Match full question
        if faq['question'].lower() in user_input_lower:
            return faq['answer']
        # Match any keyword
        for kw in faq.get("keywords", []):
            if kw.lower() in user_input_lower:
                return faq['answer']
    # Polite fallback
    return "Sorry, I can only answer questions about Iron Lady programs. Please ask about courses, duration, mentors, certificates, or mode of delivery."


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question'].strip()
    answer = find_faq_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
