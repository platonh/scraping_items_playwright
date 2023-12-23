from playwright.sync_api import sync_playwright, expect
from playwright_stealth import stealth_sync
from random import randint
from time import sleep
from config.logging_config import logger
from fake_useragent import UserAgent


def extract_html_body(url, button_selector, popup=None):
    """
    Uses Playwright to load page, navigate to its bottom and click on "Load more" button until all the content is
    rendered and the button is no longer visible. Then scrapes the `body` of HTML and returns it.
    If popup appears, closes it and proceeds.
    :param url: website url
    :param button_selector: CSS selector of "load more" button
    :param popup: dict with popup's `selector` and `close_button` selector (optionally)
    :return: `body` of HTML as a string
    """
    with sync_playwright() as p:
        # imitate different user-agents
        ua = UserAgent().getChrome

        browser = p.chromium.launch()
        context = browser.new_context(
            user_agent=ua['useragent'],
            color_scheme=r"light",
            locale=r"en-US,en;q=0.9",
            extra_http_headers={
                "Accept": "*",
                "sec-ch-ua": '"Not_A Brand";v="{}", "Chromium";v="{}"'.format(randint(5, 9), str(int(ua['version']))),
                "sec-ch-ua-platform": ua['os']
            }
        )
        page = context.new_page()
        stealth_sync(page)

        logger.info("Crawling to " + url)
        response = page.goto(url, referer=r"https://google.com")
        logger.info("Status code: " + str(response.status))

        # close popup window
        if popup:
            try:
                expect(page.locator("css={}".format(popup.get("selector")))).to_be_visible()
                page.locator("css={}".format(popup.get("close_button"))).click()
                logger.info("Popup window was closed. Proceeding.")
            except AssertionError:
                logger.info("Popup window is not visible. Proceeding.")

        # loading content
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

        # get a fully rendered html from the page
        html = page.inner_html("body")

        context.close()
        browser.close()
        logger.info("Headless browser was closed.")

        return html
