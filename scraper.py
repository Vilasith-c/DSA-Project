import nltk
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')

with open("Amazon.in_Customer reviews_ Sony Dualsense Edge Wireless Controller (Playstation 5).html", "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

reviews = soup.find_all("li", {"data-hook": "review"})

sid = SentimentIntensityAnalyzer()

for review in reviews:
    review_text_element = review.find("span", {"data-hook": "review-body"})
    review_title_element = review.find("a", {"data-hook": "review-title"})
    review_star_rating_element = review.find("i", {"data-hook": "review-star-rating"})
    reviewer_name_element = review.find("span", class_="a-profile-name")

    review_text = review_text_element.get_text(strip=True) if review_text_element else "N/A"
    review_title = review_title_element.get_text(strip=True) if review_title_element else "N/A"
    review_star_rating = review_star_rating_element.get_text(strip=True) if review_star_rating_element else "N/A"
    reviewer_name = reviewer_name_element.get_text(strip=True) if reviewer_name_element else "N/A"

    sentiment_scores = sid.polarity_scores(review_text)

    print(f"Reviewer: {reviewer_name}")
    print(f"Rating: {review_star_rating}")
    print(f"Title: {review_title}")
    print(f"Review: {review_text}")
    print(f"Sentiment: {sentiment_scores}")
    print("-" * 20)
