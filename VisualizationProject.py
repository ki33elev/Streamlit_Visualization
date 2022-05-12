import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from celluloid import Camera
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network


top_players = ['Djokovic N.', 'Federer R.', 'Medvedev D.', 'Zverev A.', 'Nadal R.',
               'Tsitsipas S.', 'Rublev A.', 'Berrettini M.', 'Murray A.', 'Ruud C.']


def print_header():
    st.title("ATP Tour analytics")
    st.markdown(
        "<h1 style='text-align: center;'><img width=300px src='data:image/jpeg;base64,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'>",
        unsafe_allow_html=True)
    st.markdown("""
        This page provides analytics and visualization for ATP (Association of Tennis Professionals)
        matches for years 2012-2021.
        Raw data was taken from https://data.world/tylerudite/atp-match-data.
    """)


@st.cache(suppress_st_warning=True)
def load_and_process_data():
    data = pd.read_csv('atp_data.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data['Winner'] = data['Winner'].apply(lambda s: s.rstrip())
    data['Loser'] = data['Loser'].apply(lambda s: s.rstrip())
    data['Year'] = data['Date'].apply(lambda date: date.year)
    return data


def plot_matches_distribution_histogram(data):
    years = [data['Date'][i].year for i in range(data['Date'].shape[0])]
    fig, ax = plt.subplots(figsize=(10, 6))
    bar = ax.bar(pd.Series(years).value_counts().index, pd.Series(years).value_counts().values,
                 align='center')
    ax.bar_label(bar, label_type='edge', padding=2)
    ax.set_xlabel('Year')
    ax.set_ylabel('Total number of ATP matches played')
    ax.set_ylim(top=2900)
    st.pyplot(fig)


def plot_surface_chart(data):
    counts = data.groupby('Tournament')['Surface'].max().value_counts().values
    surface = data.groupby('Tournament')['Surface'].max().value_counts().index
    ### FROM: https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/#32.-Pie-Chart
    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}% ({:d})".format(pct, absolute)
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(counts, autopct=lambda pct: func(pct, counts),
                                      textprops=dict(color="w"), colors=['blue', 'sandybrown', 'green'])
    ax.legend(wedges, surface, title="Surface Type", loc="best")
    ### END FROM
    st.pyplot(fig)


def plot_player_dynamics(data):
    st.write('Choose one of the top players to see how his preformance changes:')
    player = st.selectbox("Player", top_players)
    stat_win = data[data['Winner'] == player].groupby('Year')['Winner'].count()
    stat_los = data[data['Loser'] == player].groupby('Year')['Loser'].count()
    for year in range(2012, 2022):
        if year not in stat_win:
            stat_win[year] = 0
        if year not in stat_los:
            stat_los[year] = 0
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=stat_win, ax=ax)
    sns.lineplot(data=stat_los, ax=ax)
    ax.set(xlabel='Year', ylabel='Total number of wins/loses')
    plt.legend(labels=['Wins', 'Loses'])
    st.pyplot(fig)


def plot_cups_won_dynamics(data):
    st.write("""This animation shows the cumulative number amount of ATP tournaments
    won by top players in 2012-2021.""")
    fig, ax = plt.subplots(figsize=(8, 5))
    camera = Camera(fig)
    cups_won = dict()
    for player in top_players:
        cups_won[player] = 0

    for year in range(2012, 2022):
        for player in top_players:
            if player in data[data['Round'] == 'The Final'] \
                    .groupby('Year')['Winner'].value_counts()[year].index:
                cups_won[player] += data[data['Round'] == 'The Final'] \
                    .groupby('Year')['Winner'].value_counts()[year][player]
        cups_won = dict(sorted(cups_won.items(), key=lambda x: x[1], reverse=False))

        y_pos = np.arange(len(cups_won))
        bar = ax.barh(y_pos, cups_won.values(), align='center')
        ax.bar_label(bar, label_type='edge', padding=5)
        ax.set_yticks(y_pos, labels=cups_won.keys())
        ax.invert_yaxis()
        ax.set_title(f'Year: {year}')
        ax.set_xlabel('Numeber of tournaments won')
        ax.set_ylabel('Player')
        camera.snap()

    animation = camera.animate(interval=600, repeat=False)
    components.html(animation.to_jshtml(), height=700, width=1000)


def plot_player_graph(data):
    st.write('Choose one of the top players, year and surface to see the graph of opponents he played')
    player = st.selectbox("Player", sorted(top_players))
    year = st.slider("Year", min_value=2012, max_value=2021, step=1)
    surface = st.selectbox("Surface", ['Hard', 'Clay', 'Grass'])
    df = data[(data['Year'] == year) & (data['Surface'] == surface)][['Winner', 'Loser']]
    graph = nx.Graph([(win, loss) for (win, loss) in df.values])
    if player in graph:
        subgraph = graph.subgraph([player] + list(graph.neighbors(player)))
        net = Network(directed=False, notebook=False)
        net.from_nx(subgraph)
        net.show("visualization.html")
    else:
        st.error(f'{player} did not play any matches on {surface} in {year}. Please change one of the settings')


data = load_and_process_data()

print_header()

st.subheader('Total number of ATP matches played through time')
plot_matches_distribution_histogram(data)

st.subheader('Number of ATP tournaments played on each surface')
plot_surface_chart(data)

st.subheader('Top players wins/losses dynamics')
plot_player_dynamics(data)

st.subheader('Tournament wins')
plot_cups_won_dynamics(data)

st.subheader('Players graph')
plot_player_graph(data)
