# MS-teams-bot

A chatbot developed in Python using the [Microsoft Bot Framework](https://dev.botframework.com/).  
This bot is designed to **automate and moderate a 5-a-side football group chat** in Microsoft Teams.

It scrapes fixture data from a specified webpage, parses the relevant information (e.g. date, opponent, and pitch), and posts weekly updates directly into the Teams chat.

## Tech Stack

|        | Tools/Libraries Used                                   |
|----------------|--------------------------------------------------------|
| **Bot Framework** | `botbuilder`, `botframework`                      |
| **Web Scraping**  | [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/), [`Playwright`](https://playwright.dev/python/) |
| **Scheduling**    | [`APScheduler`](https://apscheduler.readthedocs.io/) |
| **Async Runtime** | `asyncio`, `aiohttp.web`                            |
| **Deployment**    | Azure App Service, Azure Bot Service                        |

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jordi-lete/MS-teams-bot.git
   cd MS-teams-bot
   pip install -r requirements.txt
   cd ms-teams-bot
   python app.py
