from playwright.sync_api import sync_playwright, Playwright
import json


def run(playwright: Playwright):
    url = ("https://www.bhphotovideo.com/c/buy/rebates-promotions/ci/22144/N/4019732813/Lenses/ci/15492/N/4288584250"
           "/pn/1")

    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    # block images to load
    page.route("**/*.{png, jpg, jpeg}", lambda route: route.abort())
    page.goto(url)

    while True:
        # details pages
        for link in page.locator('a[data-selenium="miniProductPageDetailsGridViewDetailsLink"]').all()[:1]:
            p = browser.new_page(base_url="https://www.bhphotovideo.com/")
            url = link.get_attribute("href")
            if url:
                p.goto(url)
            else:
                p.close()
            # schema
            data = p.locator('script[type="application/ld+json"]').text_content()
            json_data = json.loads(data)
            print(json_data["name"])
            p.close()

            page.locator('a[data-selenium="listingPagingPageNext"]').click()


with sync_playwright() as playwright:
    run(playwright)
