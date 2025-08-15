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
