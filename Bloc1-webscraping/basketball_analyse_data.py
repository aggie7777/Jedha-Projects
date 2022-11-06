import os
import pandas as pd
from bs4 import BeautifulSoup

SCORE_DIR = "../../../../data2/scores"
box_scores = os.listdir(SCORE_DIR)
#print(len(box_scores)) # it is over 1316
box_scores = [os.path.join(SCORE_DIR, f) for f in box_scores if f.endswith(".html")]

def parse_html(box_score):
    with open(box_score, encoding='unicode_escape') as f:
        html = f.read()
# features='lxml' to not see warnings
    soup = BeautifulSoup(html, features='lxml')

    [s.decompose() for s in soup.select("tr.over_header")]
    [s.decompose() for s in soup.select("tr.thead")]
    return soup

# id #bottom_nav_container and I find all links in it that I need
def read_season_info(soup):
    nav = soup.select("#bottom_nav_container")[0]
    hrefs = [a["href"] for a in nav.find_all('a')]
    season = os.path.basename(hrefs[1]).split("_")[0]
    return season

def read_line_score(soup):
    line_score = pd.read_html(str(soup), attrs={'id': 'line_score'})[0]
    cols = list(line_score.columns)
    cols[0] = "team"
    cols[-1] = "total"
    line_score.columns = cols

    line_score =line_score[["team", "total"]]
    return line_score


#    line_score = line_score[["team", "total"]]
#  return line_score
# i look for two tabels with two id, index first col of data 0 and it will be our first col
def read_stats(soup, team, stat):
    df = pd.read_html(str(soup), attrs = {'id': f'box-{team}-game-{stat}'}, index_col=0)[0]
    df = df.apply(pd.to_numeric, errors="coerce")
    return df

#box_score = box_scores[0]
games = []
base_cols = None
for box_score in box_scores:
    soup = parse_html(box_score)
    line_score = read_line_score(soup)
    teams = list(line_score["team"])

    summaries = []
    for team in teams:
        basic = read_stats(soup, team, "basic")
        advanced = read_stats(soup, team, "advanced")

        totals = pd.concat([basic.iloc[-1, :], advanced.iloc[-1, :]])
        totals.index = totals.index.str.lower()

        maxes = pd.concat([basic.iloc[:-1].max(), advanced.iloc[:-1].max()])
        maxes.index = maxes.index.str.lower() + "_max"

        summary = pd.concat([totals, maxes])

        if base_cols is None:
            base_cols = list(summary.index.drop_duplicates(keep="first"))
            base_cols = [b for b in base_cols if "bpm" not in b]

        summary = summary[base_cols]
        summaries.append(summary)

    summary = pd.concat(summaries, axis=1).T

    game = pd.concat([summary, line_score], axis=1)
    game["home"] = [0, 1]
    game_opp = game.iloc[::-1].reset_index()
    # I add _opp for opponets
    game_opp.columns += "_opp"

    full_game = pd.concat([game, game_opp], axis=1)
    full_game["season"] = read_season_info(soup)
    full_game["date"] = os.path.basename(box_score)[:8]
    full_game["date"] = pd.to_datetime(full_game["date"], format="%Y%m%d")
    full_game["won"] = full_game["total"] > full_game["total_opp"]
    games.append(full_game)
# I want to see work progress
    if len(games) % 100 == 0:
        print(f"{len(games)} / {len(box_scores)}")

games_df = pd.concat(games, ignore_index=True)

print(games_df)
games_df.to_csv("../../Desktop/nba_games.csv")


'''  

#print(games_df)

games_df.to_csv("../../PycharmProjects/webNbaScraping/data2/nba_games.csv")

'''

'''my commands to my code of scraping web of nba
    # I take just last row from basic and advanced iloc[-1,:] and concat it
    totals = pd.concat([basic.iloc[-1,:], advanced.iloc[-1,:]])
    totals.index = totals.index.str.lower()
    maxes = pd.concat([basic.iloc[:-1,:].max(), advanced.iloc[:-1,:].max()])
    # I make a new index becouse this cols have this name as in totals, diffrent then pandas see them
    maxes.index = maxes.index.str.lower() + "_max"
    #summary has 72 numbers and it's stats
    summary = pd.concat([totals, maxes])'''
# if I need to check if I have this some number of columns ([g.shape for g in games])
