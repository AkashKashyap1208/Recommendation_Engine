# --------- to run this project use : streamlit run app.py -----------------

import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=05a6a2c960093940c05bc81222339d4a&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # here our data frame name is 'movies' instead of 'new_df'
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # print(i[0])
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching the poster from API by using movie id
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)
    print(recommended_movies)
    return recommended_movies, recommended_movies_posters


# print(movies)

st.title("Movie Recommender System")


# for making select box
selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values)

print(recommend(selected_movie_name))

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])


# if st.button('Recommend'):
#     recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
#
#     num_movies = len(recommended_movie_names)
#     num_columns = 5  # Set the number of columns you want to display
#
#     columns = st.columns(num_columns)
#
#     for index in range(num_movies):
#         with columns[index % num_columns]:
#             st.text(recommended_movie_names[index])
#             st.image(recommended_movie_posters[index])
