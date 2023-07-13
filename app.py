import streamlit as st
import pandas as pd
import pickle
import requests

new_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    pp = data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500" + pp
    return full_path


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = new_df['movie_id'].iloc[i[0]]
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(new_df.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters


st.title('Recommend a Movie')
option = st.selectbox("Select a Movie-", new_df['title'].values)
bt1 = st.button('Recommend')
if bt1:
    names, posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])
    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])
