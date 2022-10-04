import asyncio
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
     browser = p.firefox.launch(headless=False)
     page = browser.new_page()
     page.goto("https://api.prizepicks.com/projections")
     html = page.inner_html('pre')
     page.goto("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props&subcategory=hits-allowed")
     html2 = page.inner_html('.sportsbook-league-page__body')
     page.goto("https://sportsbook.draftkings.com/leagues/football/nfl?category=passing-props&subcategory=pass-yds")
     html3 = page.inner_html('.sportsbook-league-page__body')
     page.goto("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=pitcher-props")
     html4 = page.inner_html('.sportsbook-league-page__body')
     page.goto("https://sportsbook.draftkings.com/leagues/football/nfl?category=rush/rec-props&subcategory=rush-yds")
     html5 = page.inner_html('.sportsbook-league-page__body')
     page.goto("https://sportsbook.draftkings.com/leagues/baseball/mlb?category=batter-props&subcategory=runs-scored")
     html6 = page.inner_html('.sportsbook-league-page__body')
     page.goto("https://sportsbook.draftkings.com/leagues/football/nfl?category=passing-props&subcategory=pass-tds")
     html7 = page.inner_html('.sportsbook-league-page__body')



prizepicks_json = json.loads(html)

with open('prizepicks_json.json', 'w') as f:
     json.dump(prizepicks_json, f)

draftkings_MLB_HA = open('draftkings_MLB_HA.txt', 'wb')
draftkings_MLB_HA.write(html2.encode("utf-8"))
draftkings_MLB_HA.close()

draftkings_NFL_PASSYDS = open('draftkings_NFL_PassYds.txt', 'wb')
draftkings_NFL_PASSYDS.write(html3.encode("utf-8"))
draftkings_NFL_PASSYDS.close()

draftkings_MLB_SO = open('draftkings_MLB_SO.txt', 'wb')
draftkings_MLB_SO.write(html4.encode("utf-8"))
draftkings_MLB_SO.close()

draftkings_NFL_RUSHYDS = open('draftkings_NFL_RushYds.txt', 'wb')
draftkings_NFL_RUSHYDS.write(html5.encode("utf-8"))
draftkings_NFL_RUSHYDS.close()

draftkings_NBA_PTS = open('draftkings_MLB_Runs_Scored.txt', 'wb')
draftkings_NBA_PTS.write(html6.encode("utf-8"))
draftkings_NBA_PTS.close()

draftkings_NFL_PASSTDS = open('draftkings_NFL_PassTds.txt', 'wb')
draftkings_NFL_PASSTDS.write(html7.encode("utf-8"))
draftkings_NFL_PASSTDS.close()
