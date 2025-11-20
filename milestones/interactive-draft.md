# NBA Player Performance Dashboard

Tina Dou

## Goal

This project, **NBA Player Performance Dashboard**, aims to give users an interactive way to explore a single NBA player’s game-by-game performance across a season.  

By combining web-scraped data from Basketball Reference with interactive charts, the app will help users visualize how a player’s performance changes over time and how consistently they achieve certain scoring, rebounding, or assisting thresholds.  

Users will be able to:
- Select **a player**, **a season**, and a **stat category** (e.g., Points, Assists, Rebounds).  
- Explore a histogram showing the distribution of game outcomes.
- View a ranked probability list with implied betting odds for hitting specific stat lines. (still need to work on this)
- Explore some other charts too (still need to work on this)

The goal is to make player performance patterns intuitive and interactive for basketball fans who want to explore data visually rather than read raw stats.

## Data Challenges

I initially encountered data-matching challenges when trying to map user-entered player names to the entries in my player_index.csv file. The main issue came from inconsistencies such as special characters (e.g., * for Hall of Fame players), accented letters, and variations in name formatting. I resolved this by implementing fuzzy matching to compare input names against the indexed list more flexibly.

After adding the fuzzy-match logic, the name-to-suffix lookup became reliable, and I no longer experience data-matching issues.

## Walk Through

Select **a player**, **a season**, and a **stat category** (e.g., Points, Assists, Rebounds).
![alt text](image.png)

## Questions
{Numbered list of questions for course staff, if any.}

1. Should I add any more explanation on how to use my dashboard, or is it easy enough to understand?
2. 
3. 