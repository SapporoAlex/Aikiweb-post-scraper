# Web Scraper for Aikiweb Forum
This project is a web scraper designed to log into the Aikiweb forum, search for posts by a specific username, and extract relevant thread content. The scraper utilizes Playwright for browser automation and BeautifulSoup for HTML parsing.

## Features
- Logs into the Aikiweb forum using Playwright.
- Searches for posts by a specified username.
- Collects URLs of threads containing posts by that username.
- Fetches and parses thread content.
- Saves posts authored by the specified username to a text file.

## Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- Playwright
- Requests
- BeautifulSoup

Edit the script to replace the placeholder username and password with your actual credentials.

```python
# line 30
await page.fill('input[id="navbar_username"]', 'your_username')  # Replace with your actual username
await page.fill('input[id="navbar_password"]', 'your_password')  # Replace with your actual password

# line 44
await page.fill('[id="userfield_txt"]', 'AuthorName')

# line 95
if username_tag and username_tag.text == 'AuthorName':
```
Replace 'your_username' and 'your_password' with your Aikiweb login details.
Replace 'AuthorName' with the username of the author you intend to search for.

Run the Script

Execute the script with:
```bash
pw.py
```

## Notes
Ensure that the Aikiweb forum's structure has not changed, as this may affect the script's functionality.
The script currently uses Chromium; you may need to adjust it if you prefer a different browser.
Feel free to use this script as a guide to scraping blog sites. It has documentation throughout the script explaining each step of the way.
Please only scrape ethically.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
