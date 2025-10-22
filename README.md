# RepoMiner
Gather pull request information 

## Setup Steps:
1.) clone repo<br>
2.) create a python environment<br>
3.) create a new file named .env<br>
4.) within the .env file make a new varible: GITHUB_TOKEN="<your_github_token>"<br>

## Executing the Script:
In the terminal run `python Mining.py <repo_owner>/<repo_name> <nickname>`<br>
The nickname is used in naming output files.

# Backloggd Web Scraper

## Setup:
1.) Make sure you have installed Selenium in your python environment<br>
2.) Edit browser configuration in backloggd-web-scraping notebook if needed in the selenium set up cell (default = Chrome)<br>
3.) Run all of the cells!<br>

## Note:
The main loop for html scraping includes a wait and webpage interaction simulation since the ratings are loaded in afterwards
with javascript (not in main html file) so this may take 3-5 minutes!