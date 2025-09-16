import streamlit as st
import pandas as pd
import pickle
import requests
import json
from dotenv import load_dotenv 
import os

load_dotenv()

API_KEY=os.getenv('API_KEY')


with open('movies.pkl','rb') as f:
    load_movie=pickle.load(f)

with open ('similarity.pkl','rb') as f:
    load_similarity_distance=pickle.load(f)


def fetch_poster(movie_id):
    try:
       response=requests.get('https://api.themoviedb.org/3/movie/11954?api_key={API_KEY}&&language=en-US')
       data=response.json()
       print('https://image.tmdb.org/t/p/w500'+data['poster_path'])
    except requests.exceptions.RequestException as e:
        return e

def recommend(movie):
    movie_list=[]
    movie_poster=[]
    movie_index=load_movie[load_movie['title']==movie].index[0]
    distance=sorted(list(enumerate(load_similarity_distance[movie_index])),reverse=True,key=lambda x:x[1])
    for i in distance[1:6]:
        movie_id=i[0]
        movie_list.append(load_movie.iloc[i[0]].title)
        movie_poster.append(fetch_poster(movie_id))
    return movie_poster,movie_list
    
st.title("Movie Recommender System")

movie_list=[]
for i in load_movie['title']:
    movie_list.append(i)

option = st.selectbox(
    "select one movie from below",
    (movie_list),
)

if st.button("Recommand"):
    movie_poster,movieList=recommend(option)
    print('url is:',movie_poster[0])
    for i in movieList:
        st.write(i)
    col1, col2, col3 ,col4,col5= st.columns(5)
    with col1:
        st.write(movieList[0])
        st.write(movie_poster[0])

    with col2:
        st.header(movieList[1])
        st.image(movie_poster[1])

    with col3:
        st.header(movieList[2])
        st.image(movie_poster[2])

    with col4:
        st.header(movieList[3])
        st.image(movie_poster[3])

    with col5:
        st.header(movieList[4])
        st.image(movie_poster[4])        
    


