# Amazon Review Analyzer

This project is a web application that analyzes customer reviews for any given Amazon product. It scrapes the reviews, performs sentiment analysis, and visualizes the results to provide insights into customer feedback.

## Features

-   **Real-time Scraping:** Scrapes all the reviews for a given Amazon product URL in real-time.
-   **Sentiment Analysis:** Performs sentiment analysis on each review to determine if it's positive, negative, or neutral.
-   **Data Visualization:**
    -   **Sentiment Distribution:** Displays a bar chart showing the distribution of positive, negative, and neutral reviews.
    -   **Rating Distribution:** Displays a pie chart showing the distribution of star ratings (1 to 5).
    -   **Word Cloud:** Generates a word cloud from the reviews to visualize the most frequent words.
    -   **Pros and Cons:** Identifies and displays the most common pros and cons mentioned in the reviews.

## How to Run

1.  **Install the dependencies:**
    ```
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```
    uvicorn main:app --reload
    ```
3.  **Open the application in your browser:**
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

## How it Works

The Amazon Review Analyzer is built with a client-server architecture, leveraging Python for the backend logic and standard web technologies for the frontend.

### Frontend

The user interface consists of two main HTML pages:

-   **`index.html`**: This is the landing page where users input the Amazon product review URL. It includes a simple form and a loading spinner that activates when the analysis begins, providing visual feedback to the user.
-   **`results.html`**: This page displays the comprehensive analysis of the product reviews. It presents the data in a structured and visually appealing manner, utilizing charts and organized lists.

### Backend (FastAPI)

The core logic of the application resides in `main.py`, which is a FastAPI application. FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.

-   **Request Handling**: The `main.py` handles incoming requests from the frontend.
    -   The root endpoint (`/`) serves the `index.html` page.
    -   The `/analyze` endpoint receives the Amazon product URL submitted by the user.
-   **Web Scraping**: Upon receiving a URL, the backend uses the `requests` library to fetch the HTML content of the Amazon product review page. `BeautifulSoup` is then employed to parse this HTML content, allowing for the extraction of individual reviews, including reviewer names, star ratings, review titles, and the full review text. The scraper is designed to navigate through all available review pages to ensure a comprehensive dataset.
-   **Sentiment Analysis**: For each extracted review, the Natural Language Toolkit (NLTK) with its VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon is used to perform sentiment analysis. VADER provides a compound score indicating the overall sentiment (positive, negative, or neutral) of the review.
-   **Data Processing**: The backend processes the scraped and analyzed data to generate various insights:
    -   Counts of positive, negative, and neutral reviews.
    -   Distribution of star ratings (1 to 5 stars).
    -   Identification and grouping of common pros and cons based on keywords found within the review text.
    -   Generation of a word cloud from all review texts combined.
-   **Data Delivery**: Finally, the processed data, including the generated word cloud image (saved as a static file), is passed to the `results.html` template, which is then rendered and sent back to the user's browser.

### Static Files

The application serves static files (like the generated `wordcloud.png` image) from a `static/` directory, making them accessible to the frontend.