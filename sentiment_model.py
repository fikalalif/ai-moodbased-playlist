# from transformers import pipeline

# sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# def detect_sentiment(text):
#     result = sentiment_pipeline(text)
#     label = result[0]['label'].lower()
#     if 'positive' in label:
#         return 'happy'
#     elif 'negative' in label:
#         return 'sad'
#     else:
#         return 'neutral'

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def detect_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return "positive" if result['label'] == "POSITIVE" else "negative"
