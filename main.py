import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Header to set the requests as a browser requests
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

def get_product_name(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_title_element = soup.select_one('span#productTitle')
    if product_title_element:
        product_name = product_title_element.get_text(strip=True)
    else:
        product_name = "Product Name Not Found"
    return product_name

def analyze_sentiment(reviews):
    if not reviews:
        return "No reviews found", 0, 0
    
    analyzer = SentimentIntensityAnalyzer()
    positive_count = sum(1 for review in reviews if analyzer.polarity_scores(review)['compound'] > 0)
    negative_count = len(reviews) - positive_count
    
    positive_percentage = (positive_count / len(reviews)) * 100
    negative_percentage = (negative_count / len(reviews)) * 100
    
    overall_sentiment_score = sum(analyzer.polarity_scores(review)['compound'] for review in reviews) / len(reviews)
    overall_sentiment = "This product is good" if overall_sentiment_score > 0 else "This product is bad"
    
    return overall_sentiment, positive_percentage, negative_percentage

def analyze_product():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    
    product_name = get_product_name(url)
    product_name_label.config(text=f"Product Name: {product_name}")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    amazon_reviews = [review.get_text(strip=True) for review in soup.select('span[data-hook="review-body"]')]
    
    amazon_sentiment, positive_percentage, negative_percentage = analyze_sentiment(amazon_reviews)
    sentiment_label.config(text=f"Amazon Reviews Sentiment: {amazon_sentiment}")
    positive_percentage_label.config(text=f"Percentage of Positive Reviews: {round(positive_percentage, 2)} %")
    negative_percentage_label.config(text=f"Percentage of Negative Reviews: {round(negative_percentage, 2)} %")
    
    # Create a pie chart
    labels = ['Positive', 'Negative']
    sizes = [positive_percentage, negative_percentage]
    colors = ['#66c2a5', '#fc8d62']
    explode = (0.1, 0)  # explode 1st slice
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Amazon Reviews Sentiment')
    plt.show()

# Create GUI
root = tk.Tk()
root.title("Amazon Product Sentiment Analysis")

url_label = tk.Label(root, text="Enter Amazon Product URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

analyze_button = tk.Button(root, text="Analyze", command=analyze_product)
analyze_button.pack(pady=5)

product_name_label = tk.Label(root, text="")
product_name_label.pack(pady=5)

sentiment_label = tk.Label(root, text="")
sentiment_label.pack(pady=5)

positive_percentage_label = tk.Label(root, text="")
positive_percentage_label.pack(pady=5)

negative_percentage_label = tk.Label(root, text="")
negative_percentage_label.pack(pady=5)

root.mainloop()
