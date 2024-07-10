# streamlit_app.py

import streamlit as st
import pandas as pd

# Load the merged data
merged_data = pd.read_csv('merged_data.csv')

def adjust_price(price, average_rating):
    """ Adjust the price based on the average rating. """
    if average_rating > 4.0:
        return price * 1.1  # Increase price by 10%
    elif average_rating < 2.0:
        return price * 0.9  # Decrease price by 10%
    else:
        return price  # No change

def query_book_sales(book_title):
    # Find the book in the dataset
    book_data = merged_data[(merged_data['amazon_title'] == book_title) | (merged_data['flipkart_title'] == book_title)]
    
    if book_data.empty:
        return "Book not found in the dataset."
    
    # Calculate total sales based on the ratings count
    total_sales = book_data['demand'].sum()
    
    # Get the average rating
    average_rating = book_data['average_rating'].mean()
    
    # Get prices from Amazon and Flipkart
    amazon_price = book_data['amazon_price'].mean()
    flipkart_price = book_data['flipkart_price'].mean()
    
    # Adjust prices based on the average rating
    adjusted_amazon_price = adjust_price(amazon_price, average_rating)
    adjusted_flipkart_price = adjust_price(flipkart_price, average_rating)
    
    return {
        "total_sales": total_sales,
        "average_rating": average_rating,
        "original_amazon_price": amazon_price,
        "adjusted_amazon_price": adjusted_amazon_price,
        "original_flipkart_price": flipkart_price,
        "adjusted_flipkart_price": adjusted_flipkart_price
    }

# Streamlit app
st.title("Dynamic Pricing for Books")

# Create a dropdown for selecting book titles
book_titles = pd.concat([merged_data['amazon_title'], merged_data['flipkart_title']]).unique()
selected_book = st.selectbox("Select a Book", options=book_titles)

# Display the sales information and adjusted prices
if st.button("Get Sales Info"):
    sales_info = query_book_sales(selected_book)
    
    if isinstance(sales_info, str):
        st.write(sales_info)
    else:
        st.markdown(f"""
        **Book Title:** {selected_book.capitalize()}

        **Total Sales:** {sales_info['total_sales']} times

        **Average Rating:** {sales_info['average_rating']:.2f}

        **Amazon Pricing:**
        - Original Price: ${sales_info['original_amazon_price']:.2f}
        - Adjusted Price: ${sales_info['adjusted_amazon_price']:.2f}

        **Flipkart Pricing:**
        - Original Price: ${sales_info['original_flipkart_price']:.2f}
        - Adjusted Price: ${sales_info['adjusted_flipkart_price']:.2f}
        """)

