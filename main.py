import nltk
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=".")

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading VADER lexicon...")
    nltk.download('vader_lexicon')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading Punkt tokenizer...")
    nltk.download('punkt')

sid = SentimentIntensityAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(request: Request, amazon_url: str = Form(...)):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    current_url = amazon_url
    all_reviews_soup = []
    page_count = 1

    while current_url:
        print(f"Scraping page {page_count}...")
        response = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        reviews = soup.find_all("li", {"data-hook": "review"})
        all_reviews_soup.extend(reviews)

        next_page_link = soup.find("li", class_="a-last")
        if next_page_link and next_page_link.find("a"):
            current_url = "https://www.amazon.in" + next_page_link.find("a")["href"]
            page_count += 1
        else:
            current_url = None
    
    print("Finished scraping.")

    extracted_reviews = []
    positive_reviews = 0
    negative_reviews = 0
    neutral_reviews = 0
    rating_counts = {"1.0": 0, "2.0": 0, "3.0": 0, "4.0": 0, "5.0": 0}
    
    aspect_keywords = ["battery", "screen", "camera", "performance", "price", "design", "stick", "button", "cable"]
    pros = {keyword: [] for keyword in aspect_keywords}
    cons = {keyword: [] for keyword in aspect_keywords}
    
    all_reviews_text = ""

    for review in all_reviews_soup:
        review_text_element = review.find("span", {"data-hook": "review-body"})
        review_title_element = review.find("a", {"data-hook": "review-title"})
        review_star_rating_element = review.find("i", {"data-hook": "review-star-rating"})
        reviewer_name_element = review.find("span", class_="a-profile-name")

        review_text = review_text_element.get_text(strip=True) if review_text_element else "N/A"
        review_title = review_title_element.get_text(strip=True) if review_title_element else "N/A"
        review_star_rating = review_star_rating_element.get_text(strip=True) if review_star_rating_element else "N/A"
        reviewer_name = reviewer_name_element.get_text(strip=True) if reviewer_name_element else "N/A"
        
        all_reviews_text += review_text + " "

        sentiment_scores = sid.polarity_scores(review_text)

        sentences = nltk.sent_tokenize(review_text)
        for sentence in sentences:
            if sentiment_scores['compound'] >= 0.05:
                for keyword in aspect_keywords:
                    if keyword in sentence.lower():
                        pros[keyword].append(sentence)
            elif sentiment_scores['compound'] <= -0.05:
                for keyword in aspect_keywords:
                    if keyword in sentence.lower():
                        cons[keyword].append(sentence)

        if sentiment_scores['compound'] >= 0.05:
            positive_reviews += 1
        elif sentiment_scores['compound'] <= -0.05:
            negative_reviews += 1
        else:
            neutral_reviews += 1
            
        if review_star_rating and "out of 5 stars" in review_star_rating:
            rating = review_star_rating.split(" ")[0]
            if rating in rating_counts:
                rating_counts[rating] += 1

        extracted_reviews.append({
            "reviewer": reviewer_name,
            "rating": review_star_rating,
            "title": review_title,
            "review": review_text,
            "sentiment": sentiment_scores,
        })

    sentiment_counts = {
        "positive": positive_reviews,
        "negative": negative_reviews,
        "neutral": neutral_reviews,
    }
    
    # Word Cloud Generation
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_reviews_text)
    wordcloud.to_file("static/wordcloud.png")

    return templates.TemplateResponse("results.html", {
        "request": request, 
        "reviews": extracted_reviews, 
        "sentiment_counts": sentiment_counts, 
        "rating_counts": rating_counts, 
        "pros": pros, 
        "cons": cons,
        "wordcloud": "static/wordcloud.png"
    })