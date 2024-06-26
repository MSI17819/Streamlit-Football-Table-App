# Importing the necessary libraries
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from bs4 import BeautifulSoup
import requests
from highlight_text import fig_text
from mplsoccer import Bumpy, FontManager, add_image
import json
import urllib.request
from urllib.request import urlopen

st.set_page_config(layout='wide')

st.title('Kraków A Klasa Grupa 3 sezon 2023/2024 jesień')

st.markdown("""
Aplikcja pokazuje aktualną pozycję w tabeli MZPN Kraków A Klasa Grupa 3 oraz klasyfikację strzelców.

* **Biblioteki Python:** base64, pandas, streamlit, request, BeautifulSoup, highlight_text, mplsoccer
* **Dane źródłowe:** [https://www.mzpnkrakow.pl/terminarze/2023-2024/seniorzy/a_krakow_3/](https://www.mzpnkrakow.pl/terminarze/2023-2024/seniorzy/a_krakow_3/)
""")

c1, c2 = st.columns((60,40))

with c1:
    
    st.markdown("""Tabela""")
    
    # MZPN url website
    url = 'https://www.mzpnkrakow.pl/terminarze/2023-2024/seniorzy/a_krakow_3/'

    response = requests.get(url)

    # parse text
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id' : 'tabela', 'class' : 'table'})

    # append header and rows lists from table object
    header = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 1:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    # Remowe empty list from start of rows list
    rows.remove([])

    # create dataframe from rows and header list
    df = pd.DataFrame([row for row in rows], columns=header)

    # slice dataframe for desired columns
    df_slice = df.iloc[:, 0:8]

    # Rename each column
    df_slice.rename(columns={'Drużyna' : 'Drużyna', 'M' : 'Mecz', 
                            'Pkt' : 'Punkty', 'Z' : 'Zwycięstwo', 
                            'R' : "Remis", 'P' : "Przegrana", 
                            'Bramki' : 'Bramki', 'Poz' : 'Pozycja'}, inplace=True)

    # Display dataframe in stremlit
    st.dataframe(df_slice, hide_index=True, width=650, height=528)

with c2:
    
    st.markdown("""Klasyfikacja strzelców""")
    
    df_players = pd.read_csv(r'https://raw.githubusercontent.com/MSI17819/Streamlit-Football-Table-App/main/ClassA_goals.csv',
                         encoding='utf-8', delimiter=';')

    df_players = df_players.rename(columns={'Sum' : 'Bramki', 'Player' : 'Zawodnik',
                                            'Team' : 'Drużyna', 'Goals' : 'Bramki'})

    df_players_slice = df_players.loc[:, ['Zawodnik', 'Drużyna', 'Bramki']]

    st.sidebar.header('Wybierz drużynę')

    sorted_unique_team = sorted(df_players_slice['Drużyna'].unique())

    select_team = st.sidebar.multiselect('Drużyna', sorted_unique_team, sorted_unique_team)

    df_selected_team = df_players_slice[(df_players_slice['Drużyna'].isin(select_team))]

    st.dataframe(df_selected_team, hide_index=True, width=490, height=388)

# Open json file from github url
with urllib.request.urlopen(r'https://raw.githubusercontent.com/MSI17819/Streamlit-Football-Table-App/main/Data/ClassA_result_after_13.json') as url:
    data_after_6 = json.load(url)

# Display of notes to the chart
st.markdown("""Diagram pokazuje aktualną pozycję w tabeli oraz rozegrane kolejki.""")

# Start button
if st.button('Diagram jesień'):
    
    # Use bumpy chart from mplsoccer library
    
    # match-week
    match_day = [str(num) for num in range(1, 14)]

    # highlight dict --> team to highlight and their corresponding colors
    highlight_dict = {'FAIRANT KRAKÓW' : "#fe0000",
                    'NADWIŚLAN KRAKÓW' : "#800001",
                    'TRZEBOL WIELKIE DROGI' : "#d65b02",
                    'BOREK KRAKÓW' : "#9c5d63",
                    'RADZISZOWIANKA II RADZISZÓW' : "#ffd800",
                    'PŁOMIEŃ KOSTRZE' : "#806b00",
                    'TRAMWAJ KRAKÓW' : "#0026ff",
                    'GAJOWIANKA GAJ' : "#029615",
                    'STRZELCY KRAKÓW' : "#005909",
                    'CEDRONKA WOLA RADZISZOWSKA' : "#012742",
                    'PODGÓRZE KRAKÓW' : "#00497e",
                    'ZWIERZYNIECKI KRAKÓW' : "#001280",
                    'DĄBSKI KRAKÓW' : "#b100fe",
                    'ISKRA KRZĘCIN' : "#7f2b0a"
                    }
     
    # instantiate object
    bumpy = Bumpy(
        background_color="#9a9a9a", scatter_color="#a6a6a6",
        label_color="#000000", line_color="#C0C0C0",
        rotate_xticks=None,  # rotate x-ticks by 90 degrees
        ticklabel_size=20, label_size=22,  # ticklable and label font-size
        scatter_points='D',   # other markers
        scatter_primary='o',  # marker to be used for teams
        scatter_size=150,   # size of the marker
        show_right=True,  # show position on the rightside
        plot_labels=True,  # plot the labels
        alignment_yvalue=0.1,  # y label alignment
        alignment_xvalue=0.065  # x label alignment
        )

    # plot bumpy chart
    fig, ax = bumpy.plot(
        x_list=match_day,  # match-day or match-week
        y_list=np.linspace(1, 14, 14).astype(int),  # position value from 1 to 20
        values=data_after_6,  # values having positions for each team
        secondary_alpha=0.4,   # alpha value for non-shaded lines/markers
        highlight_dict=highlight_dict,  # team to be highlighted with their colors
        figsize=(18, 8),  # size of the figure
        x_label='Kolejka', y_label='Pozycja w tabeli',  # label name
        ylim=(-0.1, 15),  # y-axis limit
        lw=2.0 # linewidth of the connecting lines
        )

    # title
    TITLE = "Klasyfikacja A Klasa Grupa 3 Kraków sezon 2023/2024 jesień"
    
    # add title
    fig.text(0.5, 0.99, TITLE, size=30, color="#222222", ha="center")
    
    # add color from highlite_dict to assigned team
    for idx, val in enumerate(df_slice['Drużyna']):
        # Using only the first word of the team name
        team_name = val.split()[0]
        for key, value in highlight_dict.items():
            if val == key:
                if idx == 0:
                    fig.text(0.92, 0.820, team_name, size=20, ha="left", color=value)
                elif idx == 1:
                    fig.text(0.92, 0.765, team_name, fontsize=20, ha="left", color=value)
                elif idx == 2:
                    fig.text(0.92, 0.710, team_name, fontsize=20, ha="left", color=value)
                elif idx == 3:
                    fig.text(0.92, 0.660, team_name, fontsize=20, ha="left", color=value)
                elif idx == 4:
                    fig.text(0.92, 0.610, team_name, fontsize=20, ha="left", color=value)
                elif idx == 5:
                    fig.text(0.92, 0.560, team_name, fontsize=20, ha="left", color=value)
                elif idx == 6:
                    fig.text(0.92, 0.510, team_name, fontsize=20, ha="left", color=value)
                elif idx == 7:
                    fig.text(0.92, 0.458, team_name, fontsize=20, ha="left", color=value)
                elif idx == 8:
                    fig.text(0.92, 0.408, team_name, fontsize=20, ha="left", color=value)
                elif idx == 9:
                    fig.text(0.925, 0.355, team_name, fontsize=20, ha="left", color=value)
                elif idx == 10:
                    fig.text(0.925, 0.305, team_name, fontsize=20, ha="left", color=value)
                elif idx == 11:
                    fig.text(0.925, 0.255, team_name, fontsize=20, ha="left", color=value)
                elif idx == 12:
                    fig.text(0.925, 0.205, team_name, fontsize=20, ha="left", color=value)
                else:
                    fig.text(0.925, 0.150, team_name, fontsize=20, ha="left", color=value)
    
    st.pyplot(fig)

with urllib.request.urlopen(r'https://raw.githubusercontent.com/MSI17819/Streamlit-Football-Table-App/main/Data/ClassA_result_after_13_spring.json') as url_spring:
    data_spring = json.load(url_spring)

if st.button('Diagram wiosna'):
    
    # Use bumpy chart from mplsoccer library
    
    # match-week
    match_day = [str(num) for num in range(1, 14)]

    # highlight dict --> team to highlight and their corresponding colors
    highlight_dict = {'FAIRANT KRAKÓW' : "#fe0000",
                    'NADWIŚLAN KRAKÓW' : "#800001",
                    'TRZEBOL WIELKIE DROGI' : "#d65b02",
                    'BOREK KRAKÓW' : "#9c5d63",
                    'RADZISZOWIANKA II RADZISZÓW' : "#ffd800",
                    'PŁOMIEŃ KOSTRZE' : "#806b00",
                    'TRAMWAJ KRAKÓW' : "#0026ff",
                    'GAJOWIANKA GAJ' : "#029615",
                    'STRZELCY KRAKÓW' : "#005909",
                    'CEDRONKA WOLA RADZISZOWSKA' : "#012742",
                    'PODGÓRZE KRAKÓW' : "#00497e",
                    'ZWIERZYNIECKI KRAKÓW' : "#001280",
                    'DĄBSKI KRAKÓW' : "#b100fe",
                    'ISKRA KRZĘCIN' : "#7f2b0a"
                    }
     
    # instantiate object
    bumpy = Bumpy(
        background_color="#9a9a9a", scatter_color="#a6a6a6",
        label_color="#000000", line_color="#C0C0C0",
        rotate_xticks=None,  # rotate x-ticks by 90 degrees
        ticklabel_size=20, label_size=22,  # ticklable and label font-size
        scatter_points='D',   # other markers
        scatter_primary='o',  # marker to be used for teams
        scatter_size=150,   # size of the marker
        show_right=True,  # show position on the rightside
        plot_labels=True,  # plot the labels
        alignment_yvalue=0.1,  # y label alignment
        alignment_xvalue=0.065  # x label alignment
        )

    # plot bumpy chart
    fig, ax = bumpy.plot(
        x_list=match_day,  # match-day or match-week
        y_list=np.linspace(1, 14, 14).astype(int),  # position value from 1 to 20
        values=data_spring,  # values having positions for each team
        secondary_alpha=0.4,   # alpha value for non-shaded lines/markers
        highlight_dict=highlight_dict,  # team to be highlighted with their colors
        figsize=(18, 8),  # size of the figure
        x_label='Kolejka', y_label='Pozycja w tabeli',  # label name
        ylim=(-0.1, 15),  # y-axis limit
        lw=2.0 # linewidth of the connecting lines
        )

    # title
    TITLE = "Klasyfikacja A Klasa Grupa 3 Kraków sezon 2023/2024 wiosna"
    
    # add title
    fig.text(0.5, 0.99, TITLE, size=30, color="#222222", ha="center")
    
    # add color from highlite_dict to assigned team
    for idx, val in enumerate(df_slice['Drużyna']):
        # Using only the first word of the team name
        team_name = val.split()[0]
        for key, value in highlight_dict.items():
            if val == key:
                if idx == 0:
                    fig.text(0.92, 0.820, team_name, size=20, ha="left", color=value)
                elif idx == 1:
                    fig.text(0.92, 0.765, team_name, fontsize=20, ha="left", color=value)
                elif idx == 2:
                    fig.text(0.92, 0.710, team_name, fontsize=20, ha="left", color=value)
                elif idx == 3:
                    fig.text(0.92, 0.660, team_name, fontsize=20, ha="left", color=value)
                elif idx == 4:
                    fig.text(0.92, 0.610, team_name, fontsize=20, ha="left", color=value)
                elif idx == 5:
                    fig.text(0.92, 0.560, team_name, fontsize=20, ha="left", color=value)
                elif idx == 6:
                    fig.text(0.92, 0.510, team_name, fontsize=20, ha="left", color=value)
                elif idx == 7:
                    fig.text(0.92, 0.458, team_name, fontsize=20, ha="left", color=value)
                elif idx == 8:
                    fig.text(0.92, 0.408, team_name, fontsize=20, ha="left", color=value)
                elif idx == 9:
                    fig.text(0.925, 0.355, team_name, fontsize=20, ha="left", color=value)
                elif idx == 10:
                    fig.text(0.925, 0.305, team_name, fontsize=20, ha="left", color=value)
                elif idx == 11:
                    fig.text(0.925, 0.255, team_name, fontsize=20, ha="left", color=value)
                elif idx == 12:
                    fig.text(0.925, 0.205, team_name, fontsize=20, ha="left", color=value)
                else:
                    fig.text(0.925, 0.150, team_name, fontsize=20, ha="left", color=value)
    
    st.pyplot(fig)
