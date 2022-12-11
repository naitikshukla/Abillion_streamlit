import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import altair as alt

# Read in the review data from a CSV file
review_data = pd.read_csv('assessment_dataset.csv',encoding='latin')

# Create a range filter for the likesCount and commentsCount columns
likes_count_range = st.sidebar.slider("likesCount range:", 0, 121, (50,100))
comments_count_range = st.sidebar.slider( "commentsCount range:", 0, 38 , (5,30))

pivot = review_data.pivot_table(index=['brandCategory','reviewBrand'], values=['likesCount', 'commentsCount'], aggfunc='mean')

# Filter the dataframe based on the selected values
filtered_data = pivot[
    (pivot["likesCount"] >= likes_count_range[0]) &
    (pivot["likesCount"] <= likes_count_range[1]) &
    (pivot["commentsCount"] >= comments_count_range[0]) &
    (pivot["commentsCount"] <= comments_count_range[1])
]

# Display scatter plot
filtered_data= filtered_data.reset_index()
filtered_data['sumLC'] = filtered_data['likesCount']+filtered_data['commentsCount']
c = alt.Chart(filtered_data).mark_circle().encode(
    x='likesCount', y='commentsCount', color='brandCategory',size='sumLC', tooltip=['likesCount', 'commentsCount','reviewBrand','brandCategory'])
st.altair_chart(c, use_container_width=True)

# Display the filtered data
st.write(filtered_data)

# Calculate and display the sum of the likesCount and commentsCount columns
st.write("Total likes + comments:", filtered_data["likesCount"].sum() + filtered_data["commentsCount"].sum())
