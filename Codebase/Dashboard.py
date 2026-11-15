
import pandas as pd
import matplotlib.pyplot as plt
import math


#load CSV file
def loaddata():
    name = input("Enter CSV filename: ")
    try:
        df = pd.read_csv(name, dtype=str, skipinitialspace=True)
        df.columns = df.columns.str.strip()

    except FileNotFoundError:
        print("Error: File '" + name + "' not found.")
        return None

    except Exception:
        print("Error: Unable to read CSV file.")
        return None

    cols = ["Date", "Item", "Category", "Quantity", "Price"]

    for col in cols:
        if col not in df.columns:
            print("Error: Missing column -", col)
            return None

    rows = []
    for i, row in df.iterrows():

        qty = pd.to_numeric(row["Quantity"],errors="coerce")
        price = pd.to_numeric(row["Price"], errors="coerce")
        date = pd.to_datetime(row["Date"], errors="coerce")

        item = str(row["Item"]).strip() if pd.notna(row["Item"]) else ""
        cat = str(row["Category"]).strip() if pd.notna(row["Category"])else ""

        if pd.isna(qty) or not math.isfinite(qty):
            print("Warning: Row", i + 2, "Quantity must be a number.")
            continue
        if qty < 0 or qty % 1 != 0:
            print("Warning: Row", i + 2, "Quantity must be a non-negative whole number.")
            continue
        if pd.isna(price) or not math.isfinite(price) or price < 0:
            print("Warning: Row", i + 2, "Price must be a valid non-negative number.")
            continue
        if pd.isna(date):
            print("Warning: Row", i + 2, "Invalid date.")
            continue
        if item == "" or cat == "":
            print("Warning: Row", i + 2, "Item or Category ismissing.")
            continue
        rows.append({
            "Date": date,
            "Item": item,
            "Category": cat,
            "Quantity": int(qty),
            "Price": float(price)
        })

    if len(rows) == 0:
        print("No valid sales records found.")
        return None

    df = pd.DataFrame(rows)

    df["Sales"] = df["Quantity"] * df["Price"]

    return df


# total sales
def totalsales(df):
    total = df["Sales"].sum()
    qty = df["Quantity"].sum()

    print("\n||--- Total-Sales ---||")
    print("Total Sales: Rs.", f"{total:g}")
    print("Total Quantity Sold:", qty)


#sales by category
def catsales(df):

    data = df.groupby("Category")["Sales"].sum()
    print("\n||--- Sales by Category ---||")

    order = ["Main", "Starter", "Dessert"]

    for cat in order:
        if cat in data.index:
            print(cat + ": Rs.", f"{data[cat]:g}")

    for cat, sales in data.items():
        if cat not in order:
            print(cat + ": Rs.", f"{sales:g}")

    print("Total sales: Rs.", f"{df['Sales'].sum():g}")


#Top items
def topitems(df):

    qty = df.groupby("Item")["Quantity"].sum()
    sales = df.groupby("Item")["Sales"].sum()

    topqty = qty.idxmax()
    topsales = sales.idxmax()

    print("\n--- Top Items ---")

    print(f"Top item by quantity: {topqty} ({qty[topqty]} units)")

    print(f"Top item by revenue: {topsales} (Rs. {sales[topsales]:g})")


#daily sales
def dailysales(df):

    data = df.groupby("Date")["Sales"].sum().sort_index()

    print("\n--- Daily Sales ---")

    for date, sales in data.items():
        print(date.strftime("%Y-%m-%d") + ": Rs.", f"{sales:g}")

    best = data.idxmax()

    print("Best day:", best.strftime("%Y-%m-%d"))


#show graphs
def graphs(df):
    # Bar chart
    data = df.groupby("Item")["Sales"].sum()
    plt.bar(data.index, data.values)
    plt.title("Item Wise Sales")
    plt.xlabel("Food Items")
    plt.ylabel("Sales (Rs.)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # Line chart
    data = df.groupby("Date")["Sales"].sum().sort_index()
    plt.plot(data.index, data.values, marker="o")
    plt.title("Day Wise Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales (Rs.)")
    plt.grid(True)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # Pie chart
    data = df.groupby("Category")["Sales"].sum()

    plt.pie(data.values, labels=data.index, autopct="%1.1f%%")
    plt.title("Category Wise Sales")
    plt.axis("equal")
    plt.show()
#menu
def main():
    df = loaddata()
    if df is None:
        return
    while True:
        print("\n||---- Restaurant Sales DashBoard----||")
        print("1 Total sales")
        print("2 Sales by category")
        print("3 Top items")
        print("4 Daily sales")
        print("5 Show graphs")
        print("6 Exit")

        choice = input("Enter your number: ")
        if choice == "1":
            totalsales(df)
        elif choice == "2":
            catsales(df)
        elif choice == "3":
            topitems(df)
        elif choice == "4":
            dailysales(df)
        elif choice == "5":
            graphs(df)
        elif choice == "6":
            print("Thank you for using Restaurant Sales Dashboard!")
            break

        else:
            print("Invalid choice! Please try again.")


main()
