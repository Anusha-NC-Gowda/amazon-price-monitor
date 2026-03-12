import pandas as pd
import datetime

# Load new scraped data
new_data = pd.read_csv("products_advanced.csv")

# Add timestamp
new_data["timestamp"] = datetime.datetime.now()

# Try loading previous history
try:
    history = pd.read_csv("price_history.csv")
    combined = pd.concat([history, new_data], ignore_index=True)
except FileNotFoundError:
    combined = new_data

# Save updated history
combined.to_csv("price_history.csv", index=False)

print("Price history updated successfully!")

# Detect recent prices
price_changes = combined.sort_values("timestamp").groupby("ASIN").tail(2)

print("\nRecent price comparison:")
print(price_changes[["ASIN","Title","Price","timestamp"]])