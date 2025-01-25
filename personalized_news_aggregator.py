import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser

# Global variable to store articles
articles = []

# Function to fetch the news based on category or keyword
def get_news():
    global articles  # Use the global articles variable
    
    api_key = "725e6cf961af4d4c9721c340e215d90a"  # Replace with your actual NewsAPI key
    base_url = "https://newsapi.org/v2/top-headlines?"
    
    # Get search keyword or category from the entry and dropdown
    search_term = keyword_entry.get()
    category = category_var.get()

    if not search_term and category == "Select Category":
        messagebox.showwarning("Input Error", "Please enter a keyword or select a category!")
        return

    # Build the API URL based on the user input
    if category != "Select Category":
        url = f"{base_url}category={category.lower()}&apiKey={api_key}"
    else:
        url = f"{base_url}q={search_term}&apiKey={api_key}"

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            articles = data["articles"]
            
            if not articles:
                messagebox.showinfo("No Results", "No news articles found.")
                return
            
            # Clear previous articles
            listbox.delete(0, tk.END)
            
            # Insert new articles into the listbox
            for article in articles:
                title = article["title"]
                source = article["source"]["name"]
                listbox.insert(tk.END, f"{title} - {source}")
            
        else:
            print(f"Error: {response.status_code}")
            messagebox.showerror("Error", "Failed to retrieve news.")
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open the selected article in the browser
def open_article(event):
    global articles  # Use the global articles variable
    
    selected_article = listbox.get(tk.ACTIVE)
    if selected_article:
        # Extract the URL by splitting the string
        title = selected_article.split(" - ")[0]
        for article in articles:
            if article["title"] == title:
                webbrowser.open(article["url"])

# Tkinter Setup
root = tk.Tk()
root.title("Personal News Aggregator")
root.geometry("500x400")

# Search/Keyword label and entry
keyword_label = tk.Label(root, text="Enter Keyword:", font=("Helvetica", 12))
keyword_label.pack(pady=10)

keyword_entry = tk.Entry(root, font=("Helvetica", 12), width=40)
keyword_entry.pack(pady=5)

# Category selection dropdown
category_var = tk.StringVar(root)
category_var.set("Select Category")  # Default value

categories = ["Select Category", "Business", "Entertainment", "Health", "Science", "Sports", "Technology"]
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.config(font=("Helvetica", 12))
category_menu.pack(pady=10)

# Search button
search_button = tk.Button(root, text="Get News", font=("Helvetica", 12), command=get_news)
search_button.pack(pady=10)

# Listbox to display articles
listbox = tk.Listbox(root, font=("Helvetica", 12), width=60, height=10)
listbox.pack(pady=10)
listbox.bind("<Double-1>", open_article)  # Open article on double-click

# Run the Tkinter main loop
root.mainloop()
