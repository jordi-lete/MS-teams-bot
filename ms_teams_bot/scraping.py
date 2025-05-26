# Web scraping libraries
from bs4 import BeautifulSoup
# Other utils
import datetime
import re

import requests

def fetch_filtered_fixtures():
    url = "https://bucs.playwaze.com/fixture/getfixtures"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://bucs.playwaze.com",
        "Referer": "https://bucs.playwaze.com/ims-football---warwick-24-25/cclrwgbo21zv9i/community-details?Tab=Fixtures",
        "User-Agent": "Mozilla/5.0",  # You can use a real user-agent string here
        "X-Requested-With": "XMLHttpRequest"
    }
    
    data = {
        "Id": "CommunityDocuments/cclrwgbo21zv9i",
        "MatchStatus": "1",  # 1 means upcoming fixtures
        "ViewTab": "tableview",
        "TeamIdList": ",teams/624870-B",  # Warwick IFL 24-25 WMG FC Mixed Football 5s
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.text  # You can change this to response.json() if it returns JSON
    else:
        print("Request failed:", response.status_code)
        return None

# Load from a static html file
def load_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def format_date(date):
    date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
    day = date_obj.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return date_obj.strftime(f"%A {day}{suffix}")

def format_pitch(pitch):
    match = re.search(r"Pitch\s+\d+", pitch)
    return match.group(0) if match else "Any pitch"

def format_opponent(opponent):
    opponent_clean = opponent.replace("Warwick IFL 24-25", "").replace("Mixed football 5s", "").strip()
    return opponent_clean

# async def get_fixture():
def get_fixture():
    timeslot = "4pm-6pm"
    team_name = "Warwick IFL 24-25 WMG FC Mixed Football 5s"
    URL = "https://bucs.playwaze.com/ims-football---warwick-24-25/cclrwgbo21zv9i/community-details?Tab=Fixtures#"

    # html = await set_up_website(URL, team_name)
    # html = set_up_website_static(URL, team_name)
    # html = load_html("ms_teams_bot/web3.html")

    html = fetch_filtered_fixtures()
    if not html:
        return "Failed to fetch fixtures."

    soup = BeautifulSoup(html, "html.parser")

    today = datetime.datetime.today()

    rows = soup.find_all("div", class_="grid-row-1")

    date = None
    opponent = None
    pitch = None

    for row in rows:
        lines = [line.strip() for line in row.stripped_strings]

        for i, line in enumerate(lines):
            # Look for format DD/MM/YYYY or D/M/YY
            if re.match(r"\d{1,2}/\d{1,2}/\d{2,4}", line):
                date_obj = datetime.datetime.strptime(line, "%d/%m/%Y")
                if today <= date_obj <= today + datetime.timedelta(days=7):
                    date = format_date(date_obj.strftime("%d/%m/%Y"))

            if "Pitch" in line and "Provider" in line:
                pitch = format_pitch(line)
            
            if "Warwick IFL 24-25" in line and not "WMG" in line:
                opponent = format_opponent(line)

    if date and opponent and pitch:
        print(f"Date: {date}\nOpponent: {opponent}\nPitch: {pitch}")
        return date, opponent, pitch

    print("No game this week")
    return None, None, None