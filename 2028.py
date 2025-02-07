import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_swimmer_ids(season):
    """
    Iterates through pages for a given season and extracts swimmer IDs.

    Args:
        season: The season number (e.g., 27, 28).

    Returns:
        A set of swimmer IDs found in the specified season.
    """

    swimmer_ids = set()
    page_num = 1
    previous_page_content = ""  # Keep track of the previous page's content

    while True:
        url = f"https://www.swimcloud.com/times/iframe/?page={page_num}&region=state_nc&orgcode=9&course=Y&hide_gender=0&hide_season=0&event=150&season={season}&gender=M"
        response = requests.get(url,headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404)
        current_page_content = response.text

        if current_page_content == previous_page_content and page_num > 1:  # Check for duplicate content
            break

        soup = BeautifulSoup(current_page_content, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/swimmer/"):
                swimmer_id = href.split("/")[2]  # Extract ID from href
                swimmer_ids.add(swimmer_id)

        previous_page_content = current_page_content
        page_num += 1

    return swimmer_ids



def main():
    """
    Extracts swimmer IDs for two seasons, filters them, and saves the results to a CSV file.
    """

    season_27_ids = get_swimmer_ids(27)
    season_28_ids = get_swimmer_ids(28)

    # Filter out IDs that are in both seasons or only in season 27
    filtered_ids = season_28_ids - season_27_ids  

    # Save the filtered IDs to a CSV file
    with open("filtered_swimmer_ids.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Swimmer ID"])  # Header row
        for swimmer_id in filtered_ids:
            writer.writerow([swimmer_id])


if __name__ == "__main__":
    main()
