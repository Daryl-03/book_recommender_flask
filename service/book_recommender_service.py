import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

from ast import literal_eval

from scipy.sparse import hstack


# loading the data
f_df = pd.read_csv('assets/books.csv')


# Définition de l'objet de vectorisation
tfidf = TfidfVectorizer(stop_words='english')
count = CountVectorizer(stop_words='english')

f_df['description'] = f_df['description'].fillna('')
f_df['description'] = f_df['description'].apply(str.lower)

def convert_to_lower_and_strip_spaces(data_strings):
    if isinstance(data_strings, list):
        return [str.lower(i.replace(" ", "")) for i in data_strings]
    else:
        if isinstance(data_strings, str):
            return str.lower(data_strings.replace(" ", ""))
        else:
            return ''

f_df['genres'] = f_df['genres'].apply(literal_eval)

f_df['genres'] = f_df['genres'].apply(convert_to_lower_and_strip_spaces)

f_df['author'] = f_df['author'].apply(convert_to_lower_and_strip_spaces)

# Formatage des caractéristiques des livres 
def create_soup2(row):
    return ' '.join(row['genres']) + ' ' + row['author']

f_df['combined'] = f_df.apply(create_soup2, axis=1)

description_matrix = tfidf.fit_transform(f_df['description'])
genre_author_matrix = count.fit_transform(f_df['combined'])

combined_matrix = hstack((description_matrix, genre_author_matrix))

f_df.reset_index()
indices = pd.Series(f_df.index, index=f_df['title'])
indicesBookId = pd.Series(f_df.index, index=f_df['bookId'])


def get_recom_from_list(books, ratings, books_features=combined_matrix):
    user_profile = np.zeros(books_features.shape[1])
    for i, rating in enumerate(ratings):
        idx = indices[books[i]]
        user_profile += rating * books_features[idx].toarray()[0]
        
    user_profile = user_profile / sum(ratings)

    similarities = cosine_similarity(user_profile.reshape(1, -1), books_features)

    # Get the similarity scores
    sim_scores = list(enumerate(similarities[0]))

    # Sort by similarity score in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 book indices (excluding the user's history)
    book_indices = [i[0] for i in sim_scores if f_df['title'].iloc[i[0]] not in books]

    # Get the recommended books
    recommended_books = [f_df['title'].iloc[i] for i in book_indices]

    return recommended_books[:10]

def get_recom_from_history(books, ratings, books_to_exclude, books_features=combined_matrix):
    user_profile = np.zeros(books_features.shape[1]) 
    
    for i, rating in enumerate(ratings):
        idx = indicesBookId[books[i]]
        user_profile += rating * books_features[idx].toarray()[0]
        
    user_profile = user_profile / sum(ratings)

    similarities = cosine_similarity(user_profile.reshape(1, -1), books_features)

    # Get the similarity scores
    sim_scores = list(enumerate(similarities[0]))

    # Sort by similarity score in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    total_excluded_books = books_to_exclude + books
    # Get the top 10 book indices (excluding the user's history)
    book_indices = [i[0] for i in sim_scores if f_df['bookId'].iloc[i[0]] not in total_excluded_books]

    # Get the recommended books
    recommended_books = [f_df['bookId'].iloc[i] for i in book_indices]

    return recommended_books[:10]