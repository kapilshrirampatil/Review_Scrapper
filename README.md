# Review_Scrapper
This project is a Python-based web scraper that extracts user reviews from IMDb for a specified movie. It uses Selenium to automate browser interactions and retrieves review ratings, titles, and text, storing them in a CSV file for further analysis.

# Features

1) Automates IMDb movie review extraction.

2) Navigates to the user review page and removes spoilers.

3) Loads all reviews dynamically by scrolling.

4) Extracts ratings, review titles, and review text.

5) Cleans and saves data in a structured CSV format.

6) Assigns sentiment labels based on review ratings (positive for ratings >5, otherwise negative)

# Requirements

To run this scraper, ensure you have the following installed:

Python 3.x

Google Chrome browser

ChromeDriver (compatible with your Chrome version)

# Required Python libraries:
pip install selenium pandas numpy

# Usage

1. Clone the Repository

git clone https://github.com/kapilshrirampatil/Review_Scrapper.git

2. Update ChromeDriver Path (if needed)
Ensure that chromedriver is installed and added to the system PATH. If required, update the driver path in the script.

3. Run the Script

python review_scraper.py

This will extract reviews for the movie Adipurush and save them in adipurush_reviews.csv.

4. Modify for Other Movies

To scrape reviews for a different movie, change the following line in review_scraper.py:

review.access_movie('Movie Name Here')

Replace 'Movie Name Here' with the desired movie title

File Structure

|-- review_scraper.py  # Main script
|-- requirements.txt   # List of dependencies
|-- README.md          # Documentation
|-- adipurush_reviews.csv  # Output file (generated after running script)

Notes

This script interacts with a live website, so IMDb may update its structure, requiring XPath adjustments.

Excessive scraping may result in temporary IP blocking; use delays (time.sleep) responsibly.

License

This project is open-source and No License.