from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def detect_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return "positive" if result['label'] == "POSITIVE" else "negative"
