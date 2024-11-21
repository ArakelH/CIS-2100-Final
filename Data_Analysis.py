import pandas as pd
import matplotlib.pyplot as plt

# Assuming 'df' is the DataFrame created in your previous code
# If not, replace 'df' with the correct DataFrame variable

# 1. The most prevalent products in customer baskets
product_counts = df.explode('Products')['Products'].value_counts()
print("\nMost Prevalent Products:\n", product_counts)

# 2. The frequency by which customers were large buyers, or filled up large baskets
# Define a threshold for large baskets (e.g., total order value > $500)
large_basket_threshold = 500
df['LargeBasket'] = df['Total'] > large_basket_threshold
large_basket_counts = df.groupby('CustomerID')['LargeBasket'].sum()
print("\nFrequency of Large Basket Buyers:\n", large_basket_counts)

# 3. Which stores contained the large-basket buyers, and by how much
store_large_basket_counts = df[df['LargeBasket']].groupby('StoreID')['Total'].sum()
print("\nStores with Large Basket Buyers:\n", store_large_basket_counts)


# 4. A visualization that ranks the top, large-basket customer stores, by frequency
top_stores_large_baskets = df[df['LargeBasket']].groupby('StoreID')['CustomerID'].nunique().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top_stores_large_baskets.index, top_stores_large_baskets.values)
plt.xlabel('Store ID')
plt.ylabel('Number of Large Basket Customers')
plt.title('Top Stores with Large Basket Customers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 5. A top-n list of products, which were typical to customers in this demographic
# Find the top 10 products purchased by large basket customers
top_products_large_baskets = df[df['LargeBasket']].explode('Products')['Products'].value_counts().head(10)
print("\nTop 10 Products purchased by Large Basket Customers:\n", top_products_large_baskets)

# 6. A categorical approach to the above demographic – what is the categoric makeup of their baskets, on average?
# Convert Products to a list of strings
df['Products'] = df['Products'].apply(lambda x: [str(product) for product in eval(x)])
# Extract product categories (assuming it's the first part of the product name before the space)
df['ProductCategories'] = df['Products'].apply(lambda x: [product.split(' ')[0] for product in x])

# Get the average count of product categories for large basket customers
average_category_counts = df[df['LargeBasket']].explode('ProductCategories')['ProductCategories'].value_counts() / len(df[df['LargeBasket']])

print("\nAverage Category Makeup of Large Basket Customers:\n", average_category_counts)

# 7. Formulate a visualization for item 6, above
plt.figure(figsize=(10, 6))
plt.pie(average_category_counts, labels=average_category_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Average Product Category Makeup of Large Basket Customers')
plt.show()
