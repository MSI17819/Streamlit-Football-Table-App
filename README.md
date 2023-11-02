# Streamlit Football Table App

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/tossingdata.svg?style=social&label=Follow%20%40tossingdata)](https://twitter.com/tossingdata)
[![Github Pages](https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=white)](https://github.com/MSI17819)

### General information
The Streamlit Football Table app showcases Kraków's Class A Group 3 football league and for secound Tramwaj Kraków team playing in Kraków Class B Group 3 (one league level lower than the first team). From a formal point of view, this is the 8th and 9th football league in Poland, if you count from Ekstraklasa (the highest level of football competition in Poland). As you can see it is a more amateur level, but we have a team with young players mainly from our academy.

Club and academy website - [Tramwaj Kraków](https://tramwajkrakow.pl/) 

Club Fb page - [Tramwaj Fb](https://www.facebook.com/tstramwaj)

Streamlit app A Class Kraków in English [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://app-football-table-app.streamlit.app/)

Streamlit app A Class Kraków in Polish [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aklasa.streamlit.app/) 

Streamlit app B Class Kraków in Polish [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([https://aklasa.streamlit.app/](https://bklasa.streamlit.app/)) 

### Dataset
The dataset contains a table with each team's position, wins, losses, draws and goals.
The table is linked to a graph where you can find the position of the team related to the number of matches played. Each point shows the position after matches of round 1, 2, 3 and is updated after each league round. A JSON file with the team position is added after each round of matches. The last number in the file name indicates the round of matches. For example, the ClassA_result_after_8.json file contains the teams' positions in the table after the 8th round of matches. The CSV file contains a list of players who have scored separately in A class and B class. The files are updated after each round of matches.

## Technology stack

### Computing platform
- [Miniconda environment](https://docs.conda.io/en/latest/miniconda.html)
- [Jupyter Notebook](https://jupyter.org/)
- [Visual Code Studio](https://code.visualstudio.com/)

### Packages for data pre-processing
- [Numpy](https://numpy.org/)
- [Pandas](https://numpy.org/)
- [Streamlit](https://streamlit.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [highlight_text](https://github.com/znstrider/highlight_text)
- [mplsoccer](https://mplsoccer.readthedocs.io/en/latest/#)

### Data visualisation library
- [Matplotlib](https://matplotlib.org/)
- [Bumpy Chart](https://mplsoccer.readthedocs.io/en/latest/gallery/bumpy_charts/plot_bumpy.html)
## Status

Project is: _in progress_

## Room for Improvement

In the future project can be improved by:

- adding more information on player and team statistics
- adding different visuals for the league and players
