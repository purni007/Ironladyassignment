from flask import Flask, render_template, request, redirect, url_for
import json
import os
from collections import Counter

app = Flask(__name__)
FEEDBACK_FILE = 'feedbacks.json'

# Expanded positive/negative words for sentiment
POSITIVE_WORDS = ['good', 'excellent', 'great', 'awesome', 'helpful', 'positive','outstanding', 'amazing', 'fantastic', 'love', 'like', 'enjoyed','inspiring','knowledgeable','creative','unique','worthy']
NEGATIVE_WORDS = ['bad','poor','slow','negative','boring','difficult','disappointing','hate','hard','frustrating','confusing','sad','not worth','useless','unhelpful','worst','not helpful','waste','overhyped','unsatisfcatory']
NEGATIVE_WEIGHTS = { 'bad': 1, 'poor': 1,'slow': 1,'negative': 1,'boring': 1,'difficult': 1, 'disappointing': 2, 'hate': 2,'hard': 1,'frustrating': 2,'confusing': 2,'sad': 2,'not worth': 2,'useless': 2,'unhelpful': 2, 'worst': 2, 'not helpful': 2, 'waste': 2, 'overhyped': 2,'unsatisfcatory': 2}
NEUTRAL_WORDS = [ 'okay', 'fine', 'average', 'normal', 'satisfactory', 'decent', 'alright', 'mediocre', 'standard', 'nothing special','nothing new']


# Load feedbacks
def load_feedbacks():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r') as f:
        return json.load(f)

# Save feedbacks
def save_feedbacks(feedbacks):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=4)

def analyze_feedback_sentiment(text):
    text = text.lower()
    pos_score = sum(text.count(w) for w in POSITIVE_WORDS)
    neg_score = sum(text.count(w) * NEGATIVE_WEIGHTS.get(w,1) for w in NEGATIVE_WORDS)
    neutral_score = sum(text.count(w) for w in NEUTRAL_WORDS)

    if pos_score > neg_score:
        return "Positive"
    elif neg_score > pos_score:
        return "Negative"
    elif neutral_score > 0:
        return "Neutral"
    else:
        return "Neutral"

def generate_summary(feedbacks):
    # Top keywords
    all_text = " ".join([f['feedback'] for f in feedbacks]).lower()
    words = [w.strip('.,!?') for w in all_text.split() if len(w) > 3]
    common_words = Counter(words).most_common(5)

    # Calculate sentiment for each feedback
    sentiments = [analyze_feedback_sentiment(f['feedback']) for f in feedbacks]
    sentiment_counts = Counter(sentiments)
    # Majority sentiment
    overall_sentiment = sentiment_counts.most_common(1)[0][0]

    return {
        "total_feedbacks": len(feedbacks),
        "top_keywords": [w[0] for w in common_words],
        "sentiment": overall_sentiment
    }




# Student form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        feedbacks = load_feedbacks()
        new_feedback = {
            "id": len(feedbacks)+1,
            "name": request.form['name'],
            "feedback": request.form['feedback']
        }
        feedbacks.append(new_feedback)
        save_feedbacks(feedbacks)
        return redirect(url_for('index'))
    return render_template('index.html')

# Admin view
@app.route('/admin')
def admin():
    feedbacks = load_feedbacks()
    summary = generate_summary(feedbacks)
    return render_template('admin.html', feedbacks=feedbacks, summary=summary)

# Edit feedback
@app.route('/edit/<int:fid>', methods=['GET', 'POST'])
def edit_feedback(fid):
    feedbacks = load_feedbacks()
    feedback = next((f for f in feedbacks if f['id']==fid), None)
    if not feedback:
        return "Feedback not found", 404
    if request.method == 'POST':
        feedback['name'] = request.form['name']
        feedback['feedback'] = request.form['feedback']
        save_feedbacks(feedbacks)
        return redirect(url_for('admin'))
    return render_template('index.html', edit_feedback=feedback)

# Delete feedback
@app.route('/delete/<int:fid>')
def delete_feedback(fid):
    feedbacks = load_feedbacks()
    feedbacks = [f for f in feedbacks if f['id'] != fid]
    save_feedbacks(feedbacks)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
