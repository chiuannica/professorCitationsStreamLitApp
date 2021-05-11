import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import matplotlib 

# *===========================*
# *===* Intro Information *===*
# *===========================*


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
st.markdown('''<ul>
                <li>The t10 value refers to the number of citations of the professors' 10th highest cited paper</li>
                <li>The h-index measures a scholars's productivity and citation impact. It is defined as the maximum number of <em>h</em> papers that have been cited <em>h</em> times.</li>
                <li>The graphs are filtered by the sidebar fields</li>
            </ul>''', unsafe_allow_html=True)

# *======================*
# *===* LOADING DATA *===*
# *======================*

# load data

def load_data():
    path = "all_professors_04.07.2021_streamlit.csv"
    df = pd.read_csv(path)
    # cut out old records (* means these are current)
    df = df[df.trim == '*']
    # limit the df to some columns
    df = df[["first", "last", "university", "citations", "h-index", "t10", "rank"]]
    # strip spaces from rank and university (prevent mismatching)
    df["university"] = df["university"].str.replace(' ', '')
    df["rank"] = df["rank"].str.strip()
    # fill empty spaces
    df = df.replace('NaN', 0)
    df = df.fillna(0)
    return df

def load_utl_data():
    # load df
    ult_path = "utilities.csv"
    df = pd.read_csv(ult_path)
    df = df[["university"]]
    # remove nulls
    df = df.dropna()
    # strip all spaces
    df["university"] = df["university"].replace(' ', '')
    return df

df_limited = load_data()



# show df (all of it)
st.subheader("Raw Full Data")
st.write(df_limited)

# *=========================*
# *===* SIDEBAR FILTERS *===*
# *=========================*

# --- CITATION SLIDERS --- 
# citation sliders
df_citations = df_limited["citations"]

df_limited["citations"] = pd.to_numeric(df_limited["citations"], downcast="float")

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
df_t10 = df_limited["t10"]

min_t10 = int(df_t10.min())
max_t10 = int(df_citations.max())

st.sidebar.write('**Adjust t10 values**')
max_t10_slider = st.sidebar.slider('Adjust the slider to the maximum t10 value', min_value=min_t10, max_value=max_t10, value=max_t10)
min_t10_slider = st.sidebar.slider('Adjust the slider to the minimum t10 value', min_value=min_t10, max_value=max_t10)

# limit the df based on the sliders
df_limited = df_limited[df_limited.t10 <= max_t10_slider]
df_limited = df_limited[df_limited.t10 >= min_t10_slider]


# --- h-index SLIDERS ---
# h-index  sliders
df_h = df_limited["h-index"]

min_h = int(df_h.min())
max_h = int(df_h.max())

st.sidebar.write('**Adjust h-index values**')
max_h_slider = st.sidebar.slider('Adjust the slider to the maximum h-index value', min_value=min_h, max_value=max_h, value=max_h)
min_h_slider = st.sidebar.slider('Adjust the slider to the minimum h-index value', min_value=min_h, max_value=max_h)

# limit the df based on the sliders
df_limited = df_limited[df_limited["h-index"] <= max_h_slider]
df_limited = df_limited[df_limited["h-index"] >= min_h_slider]

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


# --- UNIVERSITY MULTISELECT --- 
# !!! eventually I want to select multiple universities, but doesn't work :(
st.sidebar.write('**Select Universities**')
# button to click if wants to filter universities
filter_uni_button = st.sidebar.button("Filter Universities")
# if click button
if (filter_uni_button):
    # get list of universities
    uni_options = df_limited["university"].value_counts().to_frame().index
    # select
    uni_select = st.sidebar.selectbox("(Work in Progress). ", options=uni_options);

    # if something is selected, filter 
    if (uni_select):
        df_limited = df_limited.loc[df_limited['university']==(uni_select)]

    # remove filter. if click, reload df
    remove_filter_uni_button = st.sidebar.button("Remove Filter")
    if (remove_filter_uni_button):
        df_limited = load_data()
    

st.subheader("Filtered dataset")
st.write(df_limited)

# *===========================*
# *===* DISPLAYING GRAPHS *===*
# *===========================*

# display bar graph of universities 
st.subheader("Number of records at each university")

# --- COUNT FOR EACH UNIVERSITY --- 
df_uni_counts = df_limited["university"].value_counts().to_frame()

df_uni_counts.rename(columns = {'university' : 'count' }, inplace = True)
df_uni_counts["university"] = df_uni_counts.index

st.write(df_uni_counts["count"])

c = alt.Chart(df_uni_counts).mark_bar().encode(
    x="count:Q",
    y="university:N",
    color="university:N"
).interactive()
st.altair_chart(c, use_container_width=True)


#st.bar_chart(df_uni_counts)

# measures for university size
st.subheader("Measures for sizes of university")
st.write(df_uni_counts.describe())

# display bar graph of professor rank 
st.subheader("Bar graph of the number of professors of each rank")
df_rank_counts = df_limited["rank"].value_counts()
#df_rank_counts = df_rank_counts.loc[["Full", "Associate", "Assistant"]]
st.bar_chart(df_rank_counts)


# --- BUBBLE CHARTS ---
# --- t10 to citations  bubble chart ---
st.subheader("t10 to citations")

df_t10_citations = df_limited[["t10", "citations"]]
c = alt.Chart(df_t10_citations).mark_circle().encode(
    x='t10', 
    y='citations', 
    size='t10', 
    color='t10', 
    tooltip=['t10', 'citations', 't10'])
st.altair_chart(c, use_container_width=True)


# --- t10 to h-index bubble chart ---
st.subheader("t10 to h-index")

df_t10_h = df_limited[["t10", "h-index"]]
c = alt.Chart(df_t10_h).mark_circle().encode(
    x='t10', 
    y='h-index', 
    size='t10', 
    color='t10', 
    tooltip=['t10', 'h-index', 't10'])
st.altair_chart(c, use_container_width=True)

st.subheader("t10 to university")

# --- t10 to universities bubble --- 
df_t10_uni_counts = df_limited[["t10", "university"]]

c = alt.Chart(df_t10_uni_counts).mark_circle().encode(
    x="t10:Q",
    y="university:N",
    size="t10:Q",
    color="t10:Q",
    tooltip=['t10', 'university', 't10']
).interactive()
st.altair_chart(c, use_container_width=True)

st.subheader("citations to university")
df_citation_uni_counts = df_limited[["citations", "university"]]

c = alt.Chart(df_citation_uni_counts).mark_circle().encode(
    x="citations:Q",
    y="university:N",
    size="citations:Q",
    color="citations:Q",
    tooltip=['citations', 'university', 'citations']
).interactive()
st.altair_chart(c, use_container_width=True)

st.subheader("h-index to university")
df_h_uni_counts = df_limited[["h-index", "university"]]

c = alt.Chart(df_h_uni_counts).mark_circle().encode(
    x="h-index:Q",
    y="university:N",
    size="h-index:Q",
    color="h-index:Q",
    tooltip=['h-index', 'university', 'h-index']
).interactive()

st.altair_chart(c, use_container_width=True)




# st.write('''Correlation between faculty size and US News CS ranking:
#    1.0000    0.0103
#    0.0103    1.0000
#
#Correlation between US News CS ranking and university ranking:
#    1.0000    0.6792
#    0.6792    1.0000
#
#Correlation between h-index and t10-index:
#    1.0000    0.8077
#    0.8077    1.0000
#
#Correlation between logs of h-index and t10-index:
#    1.0000    0.9488
#    0.9488    1.0000 ''') 


