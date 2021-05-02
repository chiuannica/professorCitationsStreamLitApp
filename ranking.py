import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# *===========================*
# *===* RESULTS OF SCRIPT *===*
# *===========================*

# --- LOAD THE DATA ---
path_2017 = "scholar_ranking_data_USN2017.csv"
path_2018 = "scholar_ranking_data_USN2018.csv"

def load_rank(path):
    df = pd.read_csv(path)
    df = df.fillna(0)
    df = df.replace(' ', '')
    df = df.replace(' NaN', 0)
    df.set_index("Rank")
    return df

# load 2017, 2018 ranking data
df_2017 = load_rank(path_2017);
df_2018 = load_rank(path_2018)

# *===========================*
# *======* RAW DATASET *======*
# *===========================*

# --- RAW DATA --- 
# show the full raw ranking data for 2017 and 2018
st.header("Scholar scores and ranking")
st.write("Scores based on Google Scholar citations measures were generated")
st.write("These measures are M10, G10, P10, C40, C60, C80")
st.subheader("2017 USN Ranking and 2020 professor data")
st.write(df_2017)
st.subheader("2018 USN Ranking and 2020 professor data")
st.write(df_2018)

# restrict to a few important columns
df_2017_trimmed = df_2017[["Rank", "University", "Size", "USN", "Scholar"]]


df_2018_trimmed = df_2018[["Rank", "University", "Size", "USN", "Scholar"]]


# --- MERGE 2017 and 2018 ---
df_2017_2018 = pd.merge(df_2017_trimmed, df_2018_trimmed, on='University', how='inner')

# rename columns
df_2017_2018.rename(columns = {'Size_x' : '2017 Size', 'Size_y' : '2018 Size',
                               'Scholar_x' : '2017 Scholar', 'Scholar_y' : '2018 Scholar', 
                               'USN_x' : '2017 USN', 'USN_y' : '2018 USN', 
                               'Rank_x' : '2017 Rank', 'Rank_y' : '2018 Rank' }, inplace = True)

# *================================*
# *===* COMPARING 2017 to 2018 *===*
# *================================*
st.header("2017 vs 2018")
st.subheader("Size")
df_2017_2018_size = df_2017_2018[['University', '2017 Size', '2018 Size']]
st.write(df_2017_2018_size)


st.subheader("Rank")
df_2017_2018_rank = df_2017_2018[['University', '2017 Rank', '2018 Rank']]
st.write(df_2017_2018_rank)

st.subheader("Scholar score")
df_2017_2018_scholar = df_2017_2018[['University', '2017 Scholar', '2018 Scholar']]
st.write(df_2017_2018_scholar)

st.subheader("USN score")
df_2017_2018_usn = df_2017_2018[['University', '2017 USN', '2018 USN']]
st.write(df_2017_2018_usn)