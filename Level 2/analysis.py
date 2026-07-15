import pandas as pd
import matplotlib.pyplot as plt
import folium

from pathlib import Path
from folium.plugins import MarkerCluster


OUTPUT_DIR = Path("outputs/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAP_DIR = Path("outputs/maps")
MAP_DIR.mkdir(parents=True, exist_ok=True)


def load_data(file_path):
    return pd.read_csv(file_path)


def clean_data(data):

    data = data.dropna(subset=["Cuisines"]).copy()

    return data


def restaurant_ratings(data):

    print("\n" + "=" * 60)
    print("LEVEL 2 - TASK 1 : RESTAURANT RATINGS")
    print("=" * 60)

    average_votes = round(data["Votes"].mean(), 2)

    print("\nAverage Number of Votes")
    print(average_votes)

    rated_restaurants = data[data["Aggregate rating"] > 0]

    rating_distribution = (
        rated_restaurants["Aggregate rating"]
        .value_counts()
        .sort_index()
    )

    print("\nAggregate Rating Distribution")
    print(rating_distribution)

    most_common_rating = rating_distribution.idxmax()

    print("\nMost Common Rating (Excluding Unrated Restaurants)")
    print(most_common_rating)

    plt.figure(figsize=(10, 6))

    plt.hist(
        rated_restaurants["Aggregate rating"],
        bins=10,
        color="steelblue",
        edgecolor="black"
    )

    plt.title(
        "Distribution of Aggregate Ratings",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Aggregate Rating",
        fontsize=12,
        fontweight="bold"
    )

    plt.ylabel(
        "Number of Restaurants",
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

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "rating_distribution.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")
    
def cuisine_combination(data):

    print("\n" + "=" * 60)
    print("LEVEL 2 - TASK 2 : CUISINE COMBINATION")
    print("=" * 60)

    cuisine_count = (
        data["Cuisines"]
        .value_counts()
        .head(10)
    )

    print("\nTop 10 Most Common Cuisine Combinations")
    print(cuisine_count)

    cuisine_rating = (
        data.groupby("Cuisines")["Aggregate rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .round(2)
    )

    print("\nTop 10 Highest Rated Cuisine Combinations")
    print(cuisine_rating)

    plt.figure(figsize=(12, 6))

    colors = [
        "darkorange",
        "gold",
        "goldenrod",
        "peru",
        "sandybrown",
        "chocolate",
        "coral",
        "tomato",
        "lightsalmon",
        "burlywood"
    ]

    bars = plt.barh(
        cuisine_count.index,
        cuisine_count.values,
        color=colors,
        edgecolor="black",
        linewidth=1.2
    )

    plt.title(
        "Top 10 Most Common Cuisine Combinations",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Number of Restaurants",
        fontsize=12,
        fontweight="bold"
    )

    plt.ylabel(
        "Cuisine Combination",
        fontsize=12,
        fontweight="bold"
    )

    plt.grid(
        axis="x",
        linestyle="--",
        alpha=0.4
    )

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    for bar in bars:

        width = bar.get_width()

        plt.text(
            width + 5,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            va="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "cuisine_combination.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")
    
def geographic_analysis(data):

    print("\n" + "=" * 60)
    print("LEVEL 2 - TASK 3 : GEOGRAPHIC ANALYSIS")
    print("=" * 60)

    average_latitude = data["Latitude"].mean()
    average_longitude = data["Longitude"].mean()

    restaurant_map = folium.Map(
        location=[average_latitude, average_longitude],
        zoom_start=2
    )

    marker_cluster = MarkerCluster().add_to(restaurant_map)

    for _, row in data.iterrows():

        popup_text = f"""
        <b>Restaurant:</b> {row['Restaurant Name']}<br>
        <b>Cuisine:</b> {row['Cuisines']}<br>
        <b>Rating:</b> {row['Aggregate rating']}<br>
        <b>City:</b> {row['City']}
        """

        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup_text,
            icon=folium.Icon(color="blue", icon="cutlery", prefix="fa")
        ).add_to(marker_cluster)

    map_path = MAP_DIR / "restaurant_locations.html"

    restaurant_map.save(map_path)

    print("\nInteractive map created successfully.")
    print(f"\nMap saved at:\n{map_path}")

    print("\nObservation")
    print("Restaurant locations are visualized on an interactive map with clustered markers.")

def restaurant_chains(data):

    print("\n" + "=" * 60)
    print("LEVEL 2 - TASK 4 : RESTAURANT CHAINS")
    print("=" * 60)

    chain_data = (
        data.groupby("Restaurant Name")
        .agg(
            Number_of_Outlets=("Restaurant Name", "count"),
            Average_Rating=("Aggregate rating", "mean"),
            Total_Votes=("Votes", "sum")
        )
        .reset_index()
    )

    chain_data = chain_data[
        chain_data["Number_of_Outlets"] > 1
    ]

    chain_data = chain_data.sort_values(
        by="Number_of_Outlets",
        ascending=False
    )

    top_chains = chain_data.head(10)

    print("\nTop 10 Restaurant Chains")
    print(top_chains)

    plt.figure(figsize=(12,6))

    colors = [
        "navy",
        "royalblue",
        "cornflowerblue",
        "steelblue",
        "dodgerblue",
        "deepskyblue",
        "skyblue",
        "cadetblue",
        "slateblue",
        "mediumslateblue"
    ]

    bars = plt.bar(
        top_chains["Restaurant Name"],
        top_chains["Number_of_Outlets"],
        color=colors,
        edgecolor="black",
        linewidth=1.2
    )

    plt.title(
        "Top 10 Restaurant Chains",
        fontsize=18,
        fontweight="bold",
        pad=15
    )

    plt.xlabel(
        "Restaurant Chain",
        fontsize=12,
        fontweight="bold"
    )

    plt.ylabel(
        "Number of Outlets",
        fontsize=12,
        fontweight="bold"
    )

    plt.xticks(
        rotation=45,
        ha="right",
        fontsize=10
    )

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.2,
            int(height),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    plt.tight_layout()

    chart_path = OUTPUT_DIR / "restaurant_chains.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"\nChart saved successfully at:\n{chart_path}")

    print("\nObservation")
    print("Restaurant chains with more outlets generally have higher customer reach and popularity.")

def main():

    df = load_data("Dataset.csv")

    df = clean_data(df)

    print("Dataset loaded successfully.")
    print("Dataset Shape:", df.shape)

    restaurant_ratings(df)
    
    cuisine_combination(df)

    geographic_analysis(df)
    
    restaurant_chains(df)

if __name__ == "__main__":
    main()