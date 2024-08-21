import asyncio
from playwright.async_api import async_playwright
import requests
from bs4 import BeautifulSoup

# What this script does
# 1. Logs into aikiweb using Playwright
# 2. Navigates to the Forum, and searches for a username
# 3. Creates a list of all the threads that include that username
# 4. Iterates over the threads, and Uses Requests to get the HTML for each thread
# 5. Parses the HTML using BeautifulSoup to get the text of each thread
# 6. Filters each thread and stores all posts authored by the designated username
# 7. Creates a list of posts from that username, and writes them to a text file
# 8. Saves the text file with every thread post from that username


async def login_aikiweb():
    async with async_playwright() as p:
        # Launch a browser (Chromium)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigates to the login page
        await page.goto('http://www.aikiweb.com/forums/')

        # It waits for the username input field to be loaded
        await page.is_visible("#navbar_username")

        # Enters your username and passwords in each field
        await page.fill('input[id="navbar_username"]', 'jamie yugawa')  # Replace with your actual username
        await page.fill('input[id="navbar_password"]', '95544268')  # Replace with your actual password

        # Clicks the login button
        await page.click('body > table:nth-child(17) > tbody > tr > td:nth-child(3) > table:nth-child(2) > tbody > tr > td > div > div > div > table:nth-child(5) > tbody > tr > td:nth-child(2) > form > table > tbody > tr:nth-child(2) > td:nth-child(3) > input')

        # Waits for 'Search' link then clicks on it
        await page.wait_for_selector('body > table:nth-child(17) > tbody > tr > td:nth-child(3) > table:nth-child(2) > tbody > tr > td > div:nth-child(2) > div > div > div > table > tbody > tr > td:nth-child(3) > a')
        await page.click('body > table:nth-child(17) > tbody > tr > td:nth-child(3) > table:nth-child(2) > tbody > tr > td > div:nth-child(2) > div > div > div > table > tbody > tr > td:nth-child(3) > a')

        # Waits for username field to load
        await page.wait_for_selector('#userfield_txt')

        # You can change DH to any username you want here
        await page.fill('[id="userfield_txt"]', 'DH')

        # presses enter
        await page.keyboard.press("Enter")

        # waits 1 second for the page to load
        await page.wait_for_timeout(1000)

        # creates an empty list for the links to each thread (page) where the user posted
        thread_references = []

        while True:
            # Scrape all <a> tags with id starting with "thread_title_"
            thread_links = await page.locator('a[id^="thread_title_"]').all()
            for link in thread_links:
                href = await link.get_attribute('href')
                thread_references.append(href)

            # Check for the presence of the "Next Page" button
            next_button = page.locator('#inlinemodform > table:nth-child(5) > tbody > tr > td > div > table > tbody > tr > td:nth-child(6) > a')
            if await next_button.is_visible():
                await next_button.click()
                await page.wait_for_timeout(1000)
            else:
                break

        # Close the browser. We should do this when using Playwright.
        await browser.close()
        posts = []

        # Now that we have the URLs for each thread we can just use requests to get the text we want from each page.
        for link in thread_references:
            # This iterates through our URLS to 'request' the text from each thread
            url = f'http://www.aikiweb.com/forums/{link}'

            # Send a GET request to the page
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all table rows
            rows = soup.find_all('tr')

            # List to store the scraped posts


            # Loop through each row
            for row in rows:
                # Find the username in the left column
                username_tag = row.find('a', class_='boldusername')

                # Check if the username text content is "DH"
                if username_tag and username_tag.text == 'DH':
                    # Get the post content from the right column
                    post_content = row.find_all('td')[1].text.strip()
                    posts.append(post_content)

            # Output the scraped posts
            for i, post in enumerate(posts, start=1):
                print(f"Post {i}: {post}")

            # Writes the posts from the current thread to our 'DH_posts.txt'
            # We use the 'with open' method, so we don't need to continually save and open it for each time we add posts
            with open('DH_posts.txt', 'w', encoding='utf-8') as file:
                for post in posts:
                    file.write(post + "\n\n")  # Each post separated by a blank line


# Run the login script
asyncio.run(login_aikiweb())
