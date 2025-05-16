# Web scraping libraries
import requests
from bs4 import BeautifulSoup
# library to simulate user interaction
from playwright.sync_api import sync_playwright
# Other utils
from datetime import datetime

# Make a request to the Playwaze website
def set_up_website(URL):
    with sync_playwright() as p:
        html = None
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.click("text=Fixtures", force=True)
        page.wait_for_timeout(2000) # wait (milliseconds)
        page.click("text=Filter by division", force=True)
        page.wait_for_timeout(2000) # wait (milliseconds)
        page.click("text=4pm-6pm", force=True)
        page.wait_for_timeout(2000) # wait (milliseconds)
        html = page.content()
    return html

# Load from a static html file
def load_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_fixture():
    timeslot = "4pm-6pm"
    team_name = "Warwick IFL 24-25 WMG FC Mixed Football 5s"
    URL = "https://bucs.playwaze.com/ims-football---warwick-24-25/cclrwgbo21zv9i/league-display/Leagues/1kjdxip63mpn"

    html = set_up_website(URL)
    # html = load_html("ms_teams_bot/web.html")

    soup = BeautifulSoup(html, "html.parser")

    today = datetime.today()

    fixture_dates = soup.find_all("div", class_="fixture-list-date")
    for date in fixture_dates:
        date_str = date.get("data-date")
        if not date_str:
            continue
        date_obj = datetime.strptime(date_str, "%d%b%Y")
        if date_obj >= today:
            fixtures = date.find_all_next("div", class_="fixture-list")
            for fixture in fixtures:
                # stop searching when we find the next date
                next_date = fixture.find_previous("div", class_="fixture-list-date")
                if next_date != date:
                    break
                if team_name in fixture.text:
                    team_spans = fixture.find_all("span", function="GetTeamData")
                    opponent = [s.text.strip() for s in team_spans if "WMG FC" not in s.text]
                    if opponent:
                        print(f"Next fixture: {date_str} vs {opponent[0]}")
                        return date_str, opponent[0]
    print("No upcoming fixture found")
    return None, None
