
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
import streamlit as st
from bs4 import BeautifulSoup
import requests
from PIL import Image
from highlight_text import fig_text
from mplsoccer import Bumpy, FontManager, add_image
import itertools
import json

st.set_page_config(layout='wide')

st.title('Class A Krakow Group 3 season 2023/2024')

st.markdown("""
The application shows the current football table MZPN Class A Group 3.

The chart shows each team's current position in the table after a round of matches.
* **Python libraries:** base64, pandas, streamlit, request, BeautifulSoup, highlight_text, mplsoccer
* **Data source:** [https://www.mzpnkrakow.pl/terminarze/2023-2024/seniorzy/a_krakow_3/](https://www.mzpnkrakow.pl/terminarze/2023-2024/seniorzy/a_krakow_3/)
""")

url = 'https://www.mzpnkrakow.pl/terminarze/2023-2024/seniorzy/a_krakow_3/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'id' : 'tabela', 'class' : 'table'})

header = []
rows = []
for i, row in enumerate(table.find_all('tr')):
    if i == 1:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])

rows.remove([])

df = pd.DataFrame([row for row in rows], columns=header)

df_slice = df.iloc[:, 0:8]

df_slice.rename(columns={'Drużyna' : 'Team', 'M' : 'Match', 
                         'Pkt' : 'Points', 'Z' : 'Wins', 
                         'R' : "Draws", 'P' : "Losses", 
                         'Bramki' : 'Goals', 'Poz' : 'Position'}, inplace=True)

st.dataframe(df_slice, hide_index=True, width=600, height=528)


f = open(r"C:/Users/dell/Desktop/Project/KlasaA/ClassA_result_after_3.json")

# returns JSON object as
# a dictionary
data_after_2 = json.load(f)

st.markdown("""The chart shows the position and number of matches played for each team.""")

if st.button('Chart'):
    # match-week
    match_day = [str(num) for num in range(1, 14)]

    # highlight dict --> team to highlight and their corresponding colors
    highlight_dict = {'FAIRANT KRAKÓW' : "#fe0000",
                    'NADWIŚLAN KRAKÓW' : "#800001",
                    'TRZEBOL WIELKIE DROGI' : "#fe6a00",
                    'BOREK KRAKÓW' : "#803400",
                    'RADZISZOWIANKA II RADZISZÓW' : "#ffd800",
                    'PŁOMIEŃ KOSTRZE' : "#806b00",
                    'TRAMWAJ KRAKÓW' : "#0026ff",
                    'GAJOWIANKA GAJ' : "#00fe21",
                    'STRZELCY KRAKÓW' : "#007f0e",
                    'CEDRONKA WOLA RADZISZOWSKA' : "#0094fe",
                    'PODGÓRZE KRAKÓW' : "#00497e",
                    'ZWIERZYNIECKI KRAKÓW' : "#001280",
                    'DĄBSKI KRAKÓW' : "#b100fe",
                    'ISKRA KRZĘCIN' : "#7f2b0a"
                    }

    # highlight_dict = {'TRAMWAJ KRAKÓW' : "#0026ff"}
     
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
        values=data_after_2,  # values having positions for each team
        secondary_alpha=0.4,   # alpha value for non-shaded lines/markers
        highlight_dict=highlight_dict,  # team to be highlighted with their colors
        figsize=(18, 8),  # size of the figure
        x_label='Match no.', y_label='Table position',  # label name
        ylim=(-0.1, 15),  # y-axis limit
        lw=2.0, # linewidth of the connecting lines
        )

    # title and subtitle
    TITLE = "Class A Group 3 season 2023/2024"
    
    # add title
    fig.text(0.5, 0.99, TITLE, size=30, color="#222222", ha="center")
    
    for idx, val in enumerate(df_slice['Team']):
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
    
    