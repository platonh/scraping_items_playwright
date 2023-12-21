from playwright.sync_api import sync_playwright, expect
from playwright_stealth import stealth_sync
from random import randint
from time import sleep
from config.logging_config import logger


def extract_html_body(url, button_selector, popup=None):
    """
    Uses Playwright to load page, navigate to its bottom and click on "Load more" button until all the content is
    rendered and the button is no longer visible. Then scrapes the `body` of HTML and returns it.
    :param url: website url
    :param button_selector: CSS selector of "load more" button
    :param popup: dict with popup's `selector` and `close_button` selector (optionally)
    :return: `body` of HTML as a string
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            color_scheme=r"light",
            locale=r"en-US,en;q=0.9",
            extra_http_headers={
                "Accept": "*",
                "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
                "sec-ch-ua-arch": 'arm',
                "sec-ch-ua-platform": 'macOS',
                "sec-ch-ua-platform-version": '14.1.0'
            }
        )
        page = context.new_page()
        stealth_sync(page)

        logger.info("Crawling to " + url)
        response = page.goto(url, referer=r"https://google.com")
        logger.info("Status code: " + str(response.status))

        # close popup window
        if popup is not None:
            try:
                expect(page.locator("css={}".format(popup.get("selector")))).to_be_visible()
                page.locator("css={}".format(popup.get("close_button"))).click()
                logger.info("Popup window was closed. Proceeding.")
            except AssertionError:
                logger.info("Popup window is not visible. Proceeding.")

        while True:
            try:
                # stay until the page is fully loaded
                page.wait_for_load_state("networkidle")

                sleep(randint(1, 3))

                page.evaluate("() => window.scroll(0, document.body.scrollHeight)")

                # expect button to be visible; else AssertionError
                expect(
                    page.locator("css={}".format(button_selector)),
                    "Button is not visible").to_be_visible()

                # playwright locator, click "load more" button
                page.locator("css={}".format(button_selector)).click()

                logger.info("'Load more' button is clicked.")
            except AssertionError:
                logger.warning("'Load more' button is not visible. Proceeding.")
                break

        # capture a screenshot of the page
        # page.screenshot(path="screenshots/foxtrot.png", full_page=True)
        # print("Screenshot captured successfully.")

        html = page.inner_html("body")  # we get a fully rendered html from the page

        context.close()
        browser.close()
        logger.info("Headless browser was closed.")

        return html
