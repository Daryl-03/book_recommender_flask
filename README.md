# Book Recommender Flask

A Flask-based book recommendation system that provides stateless, content-based book suggestions.

## Overview

This application implements a content-based book recommendation engine using TF-IDF vectorization and cosine similarity. It operates as a stateless API service that generates personalized book recommendations based on user-provided ratings and exclusion lists.

## Implemented Features

### Core Recommendation Engine
- **Content-Based Filtering**: Uses TF-IDF on book descriptions and CountVectorizer on genres/authors 
- **Hybrid Feature Matrix**: Combines text and categorical features using scipy sparse matrices
- **User Profile Generation**: Creates weighted user profiles from rated books

### API Endpoints
- **Health Check**: `GET /` returns basic status
- **Book Recommendations**: `POST /api/book/get_recommendation_from_history` generates recommendations

### Data Processing
- **Kaggle Dataset**: Uses `assets/books.csv` with ~10,000 books 
- **Text Preprocessing**: Normalizes descriptions, genres, and authors
- **Feature Indexing**: O(1) book ID to matrix index lookups

## API Usage

### Request Format
```json
{
  "bookIdMap": {
    "book1": 4,
    "book2": 3
  },
  "unreadBookIds": ["book3", "book4"]
}
```

### Response Format
```json
["book5", "book6", "book7", "book8", "book9", "book10", "book11", "book12", "book13", "book14"]
```

## Architecture

### Stateless Design
- No user authentication or persistent sessions
- Client sends complete user state in each request
- Recommendations generated on-the-fly from input parameters 

### Recommendation Pipeline
1. Parse `bookIdMap` into book IDs and ratings
2. Build weighted user profile vector
3. Calculate cosine similarity with all books
4. Filter out rated books and `unreadBookIds`
5. Return top 10 recommendations 

## Setup

1. Install dependencies:
   ```bash
   pip install flask pandas scikit-learn numpy scipy
   ```

2. Run the application:
   ```bash
   python app.py
   ```

## Technology Stack

- **Flask 2.3.3**: Web framework
- **pandas 2.1.0**: Data manipulation
- **scikit-learn 1.3.0**: TF-IDF vectorization and cosine similarity
- **NumPy 1.26.0**: Numerical operations
- **scipy 1.11.2**: Sparse matrix operations
