import numpy as np
import pandas as pd

# dataset loading
df1 = pd.read_csv('assets/tmdb_5000_movies.csv')
df2 = pd.read_csv('assets/tmdb_5000_credits.csv')

# merging data into one data frame
df2.columns = ['id', 'tittle', 'cast', 'crew']
df1 = df1.merge(df2, on='id')

# # weighted rating
# # formula = [(v/(v+m))*R] + [(m/(v+m))*C]
# # v : number of votes
# # m : minimum number of votes
# # R : average rating of the movie
# # C : mean vote accross the dataset
# C = df1['vote_average'].mean()

# # minimum vote count to figure in chart
# m= df1['vote_count'].quantile(0.9)


# # filtering movies based on m
# f_movies = df1.copy().loc[df1['vote_count']>=m]


# def weighted_rating(movie, m=m, C=C):
#     vote = movie['vote_count']
#     rating = movie['vote_average']
# #     calculation of the score
#     return ((vote/(vote + m))*rating) + ((m/(m + vote))*C)

# # using the method to calculate scores for f_movies
# f_movies['score'] = f_movies.apply(weighted_rating, axis=1)

# f_movies = f_movies.sort_values('score', ascending=False)

# Content based filtering

from sklearn.feature_extraction.text import TfidfVectorizer

# Définition de l'objet de vectorisation
tfidf = TfidfVectorizer(stop_words='english')

df1['overview'] = df1['overview'].fillna('')

# Construction de la matrice
tfidf_movie_matrix = tfidf.fit_transform(df1['overview'])

from sklearn.metrics.pairwise import linear_kernel

# Computing of the cosine similarity
cosine_sim = linear_kernel(tfidf_movie_matrix, tfidf_movie_matrix)

# construction d'un vecteur pour retrouver les index des films en fonction du titre
indices = pd.Series(df1.index, index=df1['title']).drop_duplicates()

# Recommendation par film
def get_recommendations(title, cosine_sim=cosine_sim):
    index = indices[title]
    
#      récupérer les scores de similarité
    sim_scores = list(enumerate(cosine_sim[index]))
    
#     ordonner
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
#     récupérer les 10 premiers
    sim_scores = sim_scores[1:11]
#     return sim_scores
    movies_indices = [i[0] for i in sim_scores]
    
    return df1['title'].iloc[movies_indices]


#### changement de critères ##########

from ast import literal_eval

features = ['cast', 'crew', 'keywords', 'genres']

for feature in features:
    df1[feature] = df1[feature].apply(literal_eval)
    
# Récupérer le nom du directeur depuis la colonne crew
def get_director(list_of_crew):
    for credit in list_of_crew:
        if(credit['job'] == 'Director'):
            return credit['name']
    return np.nan


def get_top_3_list_elements(list_of_elements):
    if(isinstance(list_of_elements, list)):
        names = [i['name'] for i in list_of_elements]
        
        if len(names) > 3:
            names = names[:3]
        return names
    return []

df1['director'] = df1['crew'].apply(get_director)


# Récupération des trois premiers éléments de chaque liste
features = ['cast', 'crew', 'keywords', 'genres']

for feature in features:
    df1[feature] = df1[feature].apply(get_top_3_list_elements)
    
    
def convert_to_lower_and_strip_spaces(data_strings):
    if isinstance(data_strings, list):
        return [str.lower(i.replace(" ", "")) for i in data_strings]
    else:
        if isinstance(data_strings, str):
            return str.lower(data_strings.replace(" ", ""))
        else:
            return ''
        
features = ['cast', 'director', 'keywords', 'genres']

for feature in features:
    df1[feature] = df1[feature].apply(convert_to_lower_and_strip_spaces)
    
    
# Formatage des caractéristiques des films 
def create_soup(row):
    return ' '.join(row['keywords']) + ' ' + ' '.join(row['cast']) + ' ' + row['director'] + ' ' + ' '.join(row['genres'])

df1['soup'] = df1.apply(create_soup, axis=1)

# Vectorisation à partir d'un count vectorizer
from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df1['soup'])

# Vectorisation tfidf
tfidf_movie_matrix2 = tfidf.fit_transform(df1['soup'])

# Calcul de la matrice de similarité avec cosine sim utilisant le count vector
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset index of our main DataFrame and construct reverse mapping as before
df1 = df1.reset_index()
indices = pd.Series(df1.index, index=df1['title'])


# Recommandation à partir de l'historique utilisateur
def get_movie_recom_from_history(movies, ratings, movies_features=tfidf_movie_matrix2):
    user_profile = np.zeros(movies_features.shape[1])
    for i, rating in enumerate(ratings):
        idx = indices[movies[i]]
        user_profile += rating * movies_features[idx].toarray()[0]
        
    user_profile = user_profile/sum(ratings)

    similarities = linear_kernel(user_profile.reshape(1,-1), movies_features)

#   récupérer les scores de similarité
    sim_scores = list(enumerate(similarities[0]))
    
#   ordonner
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
#   récupérer les 10 premiers
    sim_scores = sim_scores[1:11]
#   return sim_scores
    movies_indices = [i[0] for i in sim_scores]
    
#   Exclure les films de l'historique de l'utilisateur
    movies_to_exclude = set(movies)
    recommended_movies = [df1['title'].iloc[i] for i in movies_indices if df1['title'].iloc[i] not in movies_to_exclude]
    
    return recommended_movies[:10]