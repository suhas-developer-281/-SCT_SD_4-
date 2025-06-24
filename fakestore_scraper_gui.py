import requests
import csv
import tkinter as tk
from tkinter import messagebox

def scrape_products():
    keyword = entry.get().strip().lower()
    if not keyword:
        messagebox.showwarning("Input Missing", "Please enter a product keyword.")
        return

    try:
        url = "https://fakestoreapi.com/products"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Filter by keyword
        filtered = []
        for item in data:
            title = item["title"].lower()
            category = item["category"].lower()
            if keyword in title or keyword in category:
                filtered.append({
                    "Name": item["title"],
                    "Price": f"${item['price']}",
                    "Rating": item.get("rating", {}).get("rate", "N/A")
                })

        if not filtered:
            messagebox.showinfo("No Results", f"No products found matching '{keyword}'.")
            return

        filename = f"{keyword}_products.csv"
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Price", "Rating"])
            writer.writeheader()
            writer.writerows(filtered)

        messagebox.showinfo("Success", f"{len(filtered)} products saved to {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# GUI Setup
window = tk.Tk()
window.title("🛒 Product Scraper - FakeStoreAPI")
window.geometry("400x250")

tk.Label(window, text="Enter Product Keyword:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(window, font=("Arial", 14), width=30)
entry.pack(pady=5)

tk.Button(window, text="Scrape Products", font=("Arial", 14), command=scrape_products).pack(pady=20)

window.mainloop()
