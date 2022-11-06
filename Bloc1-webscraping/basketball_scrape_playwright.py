import os
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
#from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import time
'''Playwright est un outil open-source créer en 2020 qui permet de créer des scénarios de tests sous forme de code, 
puis de les jouer sur différents navigateurs. Cet outil permet donc d’automatiser des tests fonctionnels d’applications / services Web.

Avec Playwright il est possible de directement exécuter les tests depuis l’éditeur de code, par exemple vscode, 
et de voir quelles lignes du fichier fonctionnent et quelles lignes échouent, avec à chaque fois le temps d’exécution en millisecondes.'''

SEASONS = list(range(2016, 2023))
DATA_DIR = "../../../../data2/"
STANDINGS_DIR = os.path.join(DATA_DIR, "standings")
SCORES_DIR = os.path.join(DATA_DIR, "scores")

# in this function I let wait playwright for sleep 5s by 3times, I don't want to be banish from web and not be able to scrap from this site anymore
#I just scrap my pages
#playwright work ascync i can call other function before he finish
def get_html(url, selector, sleep=5, retries=3):
    html = None
    for i in range(1, retries + 1):
        time.sleep(sleep * i)

        try:
           with sync_playwright() as p:
                browser = p.firefox.launch()
                page = browser.new_page()
                page.goto(url)
                print(page.title())
                html = page.inner_html(selector)
        except PlaywrightTimeout:
            print(f"Timeout error on {url}")
            continue
        else:
            break
    return html

def scrape_season(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"
    html = get_html(url, "#content .filter")

    soup = BeautifulSoup(html, features="lxml")
    links = soup.find_all("a")
    href = [l["href"] for l in links]
    standings_pages = [f"https://basketball-reference.com{l}" for l in href]
    #standings_pages = [f"https://www.basketball-reference.com{l['href']}" for l in links]

    for url in standings_pages:
        save_path = os.path.join(STANDINGS_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue
        # defined table with id: all_schedule
        html = get_html(url, "#all_schedule")
        with open(save_path, "w+") as f:
            f.write(html)

for season in SEASONS:
    scrape_season(season)


standings_files = os.listdir(STANDINGS_DIR)

#print(str(standings_files)[0])

def scrape_game(standings_file):

# becouse I make a def:
#standings_file = os.path.join(STANDINGS_DIR, standings_files[0])
    with open(standings_file, 'r') as f:
        html = f.read()
#
# for standings_files in range(len(standings_files)):
#   print(standings_files[standings_files])

    soup = BeautifulSoup(html, features="lxml")
# my "a" tag
    links = soup.find_all("a")
    hrefs = [l.get('href') for l in links]
# l for link
    box_scores = [f"https://www.basketball-reference.com{l}" for l in hrefs if l and "box_score" in l and '.html' in l]
#  box_scores = [l for l in hrefs if l and "boxscore" in l and ".html" in l]
# box_scores = [f"https://www.basketball-reference.com{l}" for l in box_scores]
# url.split("/")[-1] becouse I grab just last part of our url, id= #content from webpage
    for url in box_scores:
        save_path = os.path.join(SCORES_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue
# if program screpded don't do it again just continue
        html = get_html(url, "#content")
        if not html:
            continue
        with open(save_path, "w+", encoding="utf-8") as f:
            f.write(html)
# write to the file in my directory(path)
standings_files = (s for s in standings_files if ".html" in s)

#for standings_files in range(len(standings_files)):
#   print(standings_files[standings_files])

for season in SEASONS:
    files = [s for s in standings_files if str(season) in s]
    for f in files:
        filepath = os.path.join(STANDINGS_DIR, f)
        scrape_game(filepath)

# print(links)

# season = 2016
# html = get_html(url, "#content .filter")
# #print(html)
# soup = BeautifulSoup(html)
# links = soup.find_all("a")
# href = [l["href"] for l in links]
# standings_pages = [f"https://basketball-reference.com{l}" for l in href]
#print(season)