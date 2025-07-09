import datetime
import logging
import azure.functions as func
from playwright.async_api import async_playwright

async def main(mytimer: func.TimerRequest):
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info(f"Python timer trigger function ran at {utc_timestamp}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()

        await page.goto("https://www.offstreet.io/location/8Q05MGGW")
        await page.fill("#plate", "EE02U96")

        await page.get_by_role("button", name="Park").click()

        try:
            await page.get_by_role("button", name="Register").wait_for(timeout=5000)
            await page.get_by_role("button", name="Register").click()
        except:
            logging.info("No modal 'Register' button appeared — proceeding.")

        await page.wait_for_selector(".confirmation-number", timeout=60000)
        confirmation_text = await page.text_content(".confirmation-number")

        logging.info(f"Confirmation number: {confirmation_text}")

        await browser.close()
