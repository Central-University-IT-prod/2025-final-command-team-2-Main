from flask import Blueprint, jsonify, request
import requests
import os
import base64
from io import BytesIO
from app.helpers import check_token

search_bp = Blueprint('search', __name__)

@search_bp.route('/ai', methods=['POST'])
@check_token
def search_film_ai(user):
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    response = requests.post(
        'http://server.vlppz.ru:5000/gen',
        headers={
            'X-API-Password': os.environ.get('CHATGPT_SECRET_KEY', '')
        },
        json={
            "messages": [
                {"role": "system", "content": "Вы ассистент по поиску фильмов. Возвращайте только название фильма, соответствующего запросу пользователя. Без дополнительного текста или объяснений."},
                {"role": "user", "content": f"Найти фильм: {query}"}
            ]
        }
    )
    
    if response.status_code == 200:
        try:
            result = response.json()
            film_name = result.get('response', '').strip()
            return jsonify({'film_name': film_name})
        except Exception as e:
            return jsonify({'error': f'Error parsing response: {str(e)}'}), 500
    else:
        return jsonify({'error': f'Server error: {response.status_code}'}), response.status_code

@search_bp.route("/", methods=['POST'])
@check_token
def search_film(user):
    data = request.get_json()
    query = data.get('query', '')
    page = data.get('page', 1)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    url = f"https://api.themoviedb.org/3/search/multi?query={query}&include_adult=false&language=ru-RU&page={page}"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.environ.get('TMDB_API_TOKEN')}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tmdb_data = response.json()
        
        genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=ru"
        tv_genre_url = "https://api.themoviedb.org/3/genre/tv/list?language=ru"
        
        genre_response = requests.get(genre_url, headers=headers)
        genre_response.raise_for_status()
        genre_data = genre_response.json()
        
        tv_genre_response = requests.get(tv_genre_url, headers=headers)
        tv_genre_response.raise_for_status()
        tv_genre_data = tv_genre_response.json()
        
        genre_map = {genre['id']: genre['name'].capitalize() for genre in genre_data.get('genres', [])}
        tv_genre_map = {genre['id']: genre['name'].capitalize() for genre in tv_genre_data.get('genres', [])}
        
        transformed_results = []
        image_urls = []
        
        for item in tmdb_data.get('results', []):
            if item.get('media_type') in ['movie', 'tv'] and item.get('poster_path'):
                image_urls.append(f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}")
        
        image_data = {}
        if image_urls:
            import concurrent.futures
            
            def fetch_image(url):
                try:
                    img_response = requests.get(url, timeout=3)
                    if img_response.status_code == 200:
                        img_data = BytesIO(img_response.content)
                        encoded_img = base64.b64encode(img_data.getvalue())
                        return url, f"data:image/jpeg;base64,{encoded_img.decode('utf-8')}"
                except Exception:
                    pass
                return url, None
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = {executor.submit(fetch_image, url): url for url in image_urls}
                for future in concurrent.futures.as_completed(future_to_url):
                    url, base64_data = future.result()
                    if base64_data:
                        image_data[url] = base64_data
        
        for item in tmdb_data.get('results', []):
            if item.get('media_type') == 'movie':
                year = None
                if item.get('release_date'):
                    try:
                        year = int(item.get('release_date').split('-')[0])
                    except (ValueError, IndexError):
                        pass
                
                genre_name = None
                if item.get('genre_ids') and len(item.get('genre_ids')) > 0:
                    first_genre_id = item.get('genre_ids')[0]
                    genre_name = genre_map.get(first_genre_id)
                
                image_url = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else None
                image_base64 = image_data.get(image_url) if image_url else None
                
                movie = {
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'originalTitle': item.get('original_title'),
                    'description': item.get('overview'),
                    'image_url': image_url,
                    'image_base64': image_base64,
                    'rating': item.get('vote_average'),
                    'genre': genre_name,
                    'year': year,
                    'user_added': False,
                    'loaded_from_tmdb': True
                }
                transformed_results.append(movie)
            elif item.get('media_type') == 'tv':
                year = None
                if item.get('first_air_date'):
                    try:
                        year = int(item.get('first_air_date').split('-')[0])
                    except (ValueError, IndexError):
                        pass
                
                genre_name = None
                if item.get('genre_ids') and len(item.get('genre_ids')) > 0:
                    first_genre_id = item.get('genre_ids')[0]
                    genre_name = tv_genre_map.get(first_genre_id)
                
                image_url = f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else None
                image_base64 = image_data.get(image_url) if image_url else None
                
                tv_show = {
                    'id': item.get('id'),
                    'title': item.get('name'),
                    'originalTitle': item.get('original_name'),
                    'description': item.get('overview'),
                    'image_url': image_url,
                    'image_base64': image_base64,
                    'rating': item.get('vote_average'),
                    'genre': genre_name,
                    'year': year,
                    'user_added': False,
                    'loaded_from_tmdb': True
                }
                transformed_results.append(tv_show)
        
        return jsonify({
            'page': tmdb_data.get('page', 1),
            'results': transformed_results,
            'total_pages': tmdb_data.get('total_pages', 1),
            'total_results': tmdb_data.get('total_results', 0)
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request error: {str(e)}'}), 500    