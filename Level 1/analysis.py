import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


OUTPUT_DIR = Path("outputs/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data(file_path):
    return pd.read_csv(file_path)


def explore_data(data):

    print("\nFirst 5 Records")
    print(data.head())

    print("\nDataset Shape")
    print(data.shape)

    print("\nColumns")
    print(data.columns.tolist())

    print("\nData Types")
    print(data.dtypes)

    print("\nMissing Values")
    print(data.isnull().sum())

    print("\nDataset Information")
    data.info()


def clean_data(data):

    print("\nDuplicate Records")
    print(data.duplicated().sum())

    print("\nMissing Values Before Cleaning")
    print(data.isnull().sum())

    data = data.dropna(subset=["Cuisines"]).copy()

    print("\nMissing Values After Cleaning")
    print(data.isnull().sum())

    print("\nDataset Shape After Cleaning")
    print(data.shape)

    return data


def top_cuisines(data):

    cuisine_count = (
        data["Cuisines"]
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
    )

    top_three = cuisine_count.head(3)

    percentage = (top_three / len(data) * 100).round(2)

    result = pd.DataFrame({
        "Cuisine": top_three.index,
        "Restaurants": top_three.values,
        "Percentage (%)": percentage.values
    })

    print("\nTop 3 Most Common Cuisines")
    print(result)

    plt.figure(figsize=(10, 6))

    colors = ["#0F4C81", "#3A86FF", "#8ECAE6"]

    bars = plt.bar(
        result["Cuisine"],
        result["Restaurants"],
        color=colors,
        edgecolor="black",
        linewidth=1.2,
        width=0.6
    )

    plt.title(
        "Top 3 Most Common Cuisines",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Cuisine",
        fontsize=13,
        fontweight="bold"
    )

    plt.ylabel(
        "Number of Restaurants",
        fontsize=13,
        fontweight="bold"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 30,
            f"{height:,}",
            ha="center",
            fontsize=11,
            fontweight="bold"
        )

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "top_3_cuisines.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")

def city_analysis(data):

    restaurant_count = (
        data.groupby("City")
        .size()
        .sort_values(ascending=False)
    )

    average_rating = (
        data.groupby("City")["Aggregate rating"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    print("\nCity with Highest Number of Restaurants")
    print(restaurant_count.head(1))

    print("\nTop 10 Cities by Average Rating")
    print(average_rating.head(10))

    print("\nCity with Highest Average Rating")
    print(average_rating.head(1))

    top_10 = restaurant_count.head(10)

    plt.figure(figsize=(12, 7))

    colors = [
        "#0F4C81",
        "#1E6091",
        "#3A86FF",
        "#4895EF",
        "#4CC9F0",
        "#90E0EF",
        "#8ECAE6",
        "#219EBC",
        "#0077B6",
        "#023E8A"
    ]

    bars = plt.bar(
        top_10.index,
        top_10.values,
        color=colors,
        edgecolor="black"
    )

    plt.title(
        "Top 10 Cities by Number of Restaurants",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("City", fontsize=12, fontweight="bold")
    plt.ylabel("Number of Restaurants", fontsize=12, fontweight="bold")

    plt.xticks(rotation=45, ha="right")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width()/2,
            bar.get_height() + 40,
            f"{int(bar.get_height())}",
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "restaurants_by_city.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")
    
def price_range_distribution(data):

    price_count = (
        data["Price range"]
        .value_counts()
        .sort_index()
    )

    percentage = (
        price_count / len(data) * 100
    ).round(2)

    result = pd.DataFrame({
        "Price Range": price_count.index,
        "Restaurants": price_count.values,
        "Percentage (%)": percentage.values
    })

    print("\nPrice Range Distribution")
    print(result)

    plt.figure(figsize=(10, 6))

    colors = ["#4E79A7", "#59A14F", "#F28E2B", "#E15759"]

    bars = plt.bar(
        result["Price Range"].astype(str),
        result["Restaurants"],
        color=colors,
        edgecolor="black",
        linewidth=1.2,
        width=0.6
    )

    plt.title(
        "Restaurant Distribution by Price Range",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Price Range",
        fontsize=13,
        fontweight="bold"
    )

    plt.ylabel(
        "Number of Restaurants",
        fontsize=13,
        fontweight="bold"
    )

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 40,
            f"{height:,}",
            ha="center",
            fontsize=11,
            fontweight="bold"
        )

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "price_range_distribution.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")
    
def online_delivery_analysis(data):

    delivery_count = (
        data["Has Online delivery"]
        .value_counts()
        .sort_index()
    )

    delivery_percentage = (
        delivery_count / len(data) * 100
    ).round(2)

    result = pd.DataFrame({
        "Online Delivery": delivery_count.index,
        "Restaurants": delivery_count.values,
        "Percentage (%)": delivery_percentage.values
    })

    print("\nOnline Delivery Distribution")
    print(result)

    average_rating = (
        data.groupby("Has Online delivery")["Aggregate rating"]
        .mean()
        .round(2)
    )

    print("\nAverage Rating by Online Delivery")
    print(average_rating)

    plt.figure(figsize=(8, 6))

    colors = ["#E74C3C", "#2ECC71"]

    bars = plt.bar(
        result["Online Delivery"],
        result["Percentage (%)"],
        color=colors,
        edgecolor="black",
        linewidth=1.2,
        width=0.6
    )

    plt.title(
        "Percentage of Restaurants Offering Online Delivery",
        fontsize=17,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Online Delivery",
        fontsize=12,
        fontweight="bold"
    )

    plt.ylabel(
        "Percentage (%)",
        fontsize=12,
        fontweight="bold"
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 1,
            f"{height:.2f}%",
            ha="center",
            fontsize=11,
            fontweight="bold"
        )

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "online_delivery_distribution.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")

    print("\nObservation")

    if average_rating["Yes"] > average_rating["No"]:
        print(
            "Restaurants offering online delivery have a higher average rating."
        )
    else:
        print(
            "Restaurants without online delivery have a higher average rating."
        )
    
def main():

    df = load_data("Dataset.csv")

    explore_data(df)

    df = clean_data(df)

    top_cuisines(df)

    city_analysis(df)
    
    price_range_distribution(df)
    
    online_delivery_analysis(df)

if __name__ == "__main__":
    main()

