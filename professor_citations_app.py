import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

st.title("Computer Science Department Professors' Citations")
st.subheader("Purpose of Data")
st.write("This is the display of data I spent months collecting as a research assistant.")
st.write("The purpose of this data is to predict peer review scores based on computer science departments' citation values.")
st.write('''The ranking of universities is a significant factor in students’ decisions to attend a
        university, government organizations deciding where to allocate funding, and universities in
        deciding how to grow their programs. Rankings have been based on multiple factors, including
        location, student to faculty ratio, and student happiness.''')
st.write('''This dataset includes the professors at computer science programs, 
            the number of citations they have, and scraped citation measures 
            from their Google Scholar page.''')
st.subheader("Things to know to interpret data")
st.write('''The t10 value refers to the number of citations of the professors' 10th highest cited paper.''')
st.markdown("**The graphs are filtered by the sidebar fields.**")


# load data
path = "Crawled_Faculty_data_3.25.2021.xlsx"
df = pd.read_excel(path)

# cut out old records (* means these are current)
df = df[df.trim == '*']
df_limited = df

# limit the df to some columns
df_limited = df_limited[["first", "last", "university", "citations", "t10", "rank"]]

# show df
st.subheader("Data")
st.write(df_limited)

# --- Univ

# --- CITATION SLIDERS --- 
# citation sliders
df_citations = df["citations"]
min_citations = int(df_citations.min())
max_citations = int(df_citations.max())

st.sidebar.write('**Adjust citation values**')
max_citation_slider = st.sidebar.slider('Adjust the slider to the maximum citation value', min_value=min_citations, max_value=max_citations, value=max_citations )
min_citation_slider = st.sidebar.slider('Adjust the slider to the minimum citation value', min_value=min_citations, max_value=max_citations)

# limit the df based on the sliders
df_limited = df_limited[df_limited.citations <= max_citation_slider]
df_limited = df_limited[df_limited.citations >= min_citation_slider]

# --- t10 SLIDERS ---
# t10 sliders
df_t10 = df["t10"]

min_t10 = int(df_t10.min())
max_t10 = int(df_citations.max())

st.sidebar.write('**Adjust t10 values**')
max_t10_slider = st.sidebar.slider('Adjust the slider to the maximum t10 value', min_value=min_t10, max_value=max_t10, value=max_t10)
min_t10_slider = st.sidebar.slider('Adjust the slider to the minimum t10 value', min_value=min_t10, max_value=max_t10)

# limit the df based on the sliders
df_limited = df_limited[df_limited.t10 <= max_t10_slider]
df_limited = df_limited[df_limited.t10 >= min_t10_slider]


# --- RANK MULTISELECT ---
# select rank
st.sidebar.write('**Professor Rank**')

rank_radio = st.sidebar.radio(
    "Select the professor to filter",
    ("All", "Full", "Associate", "Assistant"))

if (rank_radio == "Full"):
    df_limited = df_limited[ (df_limited['rank'] == "Full") ]
elif (rank_radio == "Associate"):
    df_limited = df_limited[ (df_limited['rank'] == "Associate") ]
elif (rank_radio == "Assistant"):
    df_limited = df_limited[ (df_limited['rank'] == "Assistant") ]




# --- DISPLAYING GRAPHS ---
# display bar graph of universities 
st.subheader("Bar graph of the number of records at each university")
df_uni_counts = df_limited["university"].value_counts()
st.bar_chart(df_uni_counts)

# display bar graph of professor rank 
st.subheader("Bar graph of the number of professors of each rank")
df_rank_counts = df_limited["rank"].value_counts()
#df_rank_counts = df_rank_counts.loc[["Full", "Associate", "Assistant"]]
st.bar_chart(df_rank_counts)


# --- BUBBLE CHARTS ---
import altair as alt
st.subheader("t10 to citations")

df_t10_citations = df_limited[["t10", "citations"]]
c = alt.Chart(df_t10_citations).mark_circle().encode(x='t10', y='citations', size='t10', tooltip=['t10', 'citations', 't10'])
st.altair_chart(c, use_container_width=True)


st.subheader("t10 to university")
df_t10_uni_counts = df_limited[["t10", "university"]]

c = alt.Chart(df_t10_uni_counts).mark_circle().encode(x='t10', y='university', size='t10', color='t10', tooltip=['t10', 'university', 't10'])
st.altair_chart(c, use_container_width=True)

st.subheader("citations to university")
df_citation_uni_counts = df_limited[["citations", "university"]]

c = alt.Chart(df_citation_uni_counts).mark_circle().encode(x='citations', y='university', size='citations', color='citations', tooltip=['citations', 'university', 'citations'])
st.altair_chart(c, use_container_width=True)
