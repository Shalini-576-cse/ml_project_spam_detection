# ---------------- IMPORTS ---------------- #

from flask import Flask, render_template, request   # Flask for web app
import pandas as pd                                 # For dataset handling

from sklearn.model_selection import train_test_split   # To split dataset
from sklearn.feature_extraction.text import TfidfVectorizer  # Convert text to numbers
from sklearn.naive_bayes import MultinomialNB        # ML algorithm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score  # Metrics


# ---------------- APP INITIALIZATION ---------------- #

app = Flask(__name__)   # Create Flask app


# ---------------- TRAIN MODEL FUNCTION ---------------- #

def train_model():
    """
    This function:
    - Loads dataset
    - Converts text to vectors
    - Trains model
    - Calculates performance metrics
    """

    # Load dataset (SMS Spam Collection)
    data = pd.read_csv("SMSSpamCollection", sep='\t', names=["label", "message"])

    # Convert labels: ham = 0, spam = 1
    data['label'] = data['label'].map({'ham': 0, 'spam': 1})

    # Split input (X) and output (y)
    X = data['message']
    y = data['label']

    # Convert text into numerical form (TF-IDF)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # Split into training and testing data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model using Naive Bayes
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    # Calculate evaluation metrics
    accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)
    precision = round(precision_score(y_test, y_pred) * 100, 2)
    recall = round(recall_score(y_test, y_pred) * 100, 2)
    f1 = round(f1_score(y_test, y_pred), 3)

    # Return everything needed
    return model, vectorizer, accuracy, precision, recall, f1, len(vectorizer.vocabulary_), len(data)


# ---------------- SPAM WORD HIGHLIGHT FUNCTION ---------------- #

# Common spam keywords
spam_words = ["free", "win", "urgent", "offer", "click", "prize"]

def highlight_words(message):
    """
    Highlights spam-related words in red color
    """
    words = message.split()
    highlighted = []

    for w in words:
        if w.lower() in spam_words:
            # Highlight spam word in red
            highlighted.append(f"<span style='color:red'>{w}</span>")
        else:
            highlighted.append(w)

    return " ".join(highlighted)


# ---------------- MAIN ROUTE ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Handles:
    - Page load (GET)
    - Form submission (POST)
    """

    result = ""           # Spam / Not Spam result
    spam_prob = ""        # Spam probability
    ham_prob = ""         # Not spam probability
    message = ""          # User input
    highlighted_msg = ""  # Highlighted message

    # Train model every time (for demo purpose)
    model, vectorizer, accuracy, precision, recall, f1, vocab, total = train_model()

    # If user submits form
    if request.method == "POST":
        message = request.form["message"]

        if message.strip() != "":
            # Convert message into vector
            vec = vectorizer.transform([message])

            # Predict result
            pred = model.predict(vec)[0]

            # Get probabilities
            prob = model.predict_proba(vec)[0]
            spam_prob = round(prob[1] * 100, 2)
            ham_prob = round(prob[0] * 100, 2)

            # Convert result into readable form
            result = "Spam" if pred == 1 else "Not Spam"

            # Highlight spam words
            highlighted_msg = highlight_words(message)

    # Send data to HTML page
    return render_template(
        "index.html",
        result=result,
        spam_prob=spam_prob,
        ham_prob=ham_prob,
        message=message,
        highlighted_msg=highlighted_msg,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        vocab=vocab,
        total=total
    )


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)