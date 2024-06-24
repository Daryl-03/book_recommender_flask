
from flask import Flask, jsonify, request
from service.book_recommender_service import get_recom_from_history

app = Flask(__name__)

@app.route("/")
def index():
	return "Hello, World!"

@app.route("/api/book/get_recommendation_from_history", methods=['POST'])
def getBookRecommendations_from_history():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        print(data)
        print(data['bookIdMap'])
        print(data['unreadBookIds'])
        
        # Extract the movie titles and ratings 
        book_ids = list(data['bookIdMap'].keys())
        print(book_ids)
        ratings = list(data['bookIdMap'].values())
        print(ratings)
        
        response = get_recom_from_history(book_ids, ratings, data['unreadBookIds'])
        
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    
        
if __name__ == "__main__":
	app.run(debug=True)
    

    
    
# @app.route("/api/book/get_recommendation", methods=['POST'])
# def getBookRecommendations_from_list():
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()
        
#         # Extract the movie titles and ratings 
#         book_titles = list(data.keys())
#         ratings = list(data.values())
        
#         response = get_recom_from_list(book_titles, ratings)
        
#         return jsonify(response), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# @app.route("/api/get_recommendation", methods=['POST'])
# def getRecommendations():
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()
        
#         # Extract the movie titles and ratings 
#         movie_titles = list(data.keys())
#         ratings = list(data.values())
        
#         response = get_movie_recom_from_history(movie_titles, ratings)
        
#         return jsonify(response), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
	app.run(debug=True)
    
    
    
    