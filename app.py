'''
    flask spotipy Flask-Session
'''
import os
import functools
from flask import Flask, session, request, redirect, render_template, url_for
import spotipy
from flask_session import Session
from utils.utils import process_data

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

SCOPE = 'user-read-private user-read-email user-library-read playlist-read-private playlist-read-collaborative user-top-read'

# Decorator to validate that user has signed in and can enter target route
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "token_info" not in session:
            return redirect(url_for("index", next=request.url))
        return func(*args, **kwargs)
    return secure_function

@app.route('/')
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    auth_url = auth_manager.get_authorize_url()
    return render_template('index.html', auth_url=auth_url)

@app.route('/callback')
def callback():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    
    #  Authorization code from Spotify's callback after signing in and accepting app. Returns string
    auth_code = auth_manager.get_authorization_code(request.args.get("code"))

    # Unable to get authorization code
    if not auth_manager.get_authorization_code(request.args.get("code")):
        return redirect('/')
    
    # Token acquired from authorization code above
    # For code string only, add arg: as_dict=False
    access_token = auth_manager.get_access_token(auth_code)

    # Validates access token, renews it if expired or broken, and saves it to cache
    cache_handler.save_token_to_cache(auth_manager.validate_token(access_token))

    return redirect('/dashboard')

@app.route('/dashboard')
@login_required
def dashboard():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    # Token expired, or broken, return to sign in page
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')    
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    playlists_array = [] # Holds all playlists' data

    playlist_data = spotify.current_user_playlists()
    # Add playlists to array
    playlists_array = playlist_data.get('items')

    # If there are more pages with playlists, add them to list.
    while playlist_data.get('next'):
        playlist_data = spotify.next(playlist_data)
        playlists_array.extend(playlist_data.get('items'))


    return render_template('dashboard.html', spotify=spotify, playlists_array=playlists_array)


@app.route('/signout')
@login_required
def signout():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/playlist/')
@login_required
def playlist():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    # Token expired, or broken, return to sign in page
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')    
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Grabs current user's country
    user_country = spotify.current_user().get('country')

    # Grabs playlist id from url
    playlist_id = request.args.get('id')

    # Fields supplied for wanted response
    FIELDS = (  'next,'
                'items(added_at, added_by.id,'
                    'track(album(images, release_date), artists(external_urls.spotify, name), duration_ms, explicit, external_ids.isrc, external_urls.spotify, id, is_local, name, popularity))'
                )
    
    # Response holding playlist name and public/private status
    playlist_details = spotify.playlist(playlist_id=playlist_id, fields=('name, public'), market=user_country, additional_types=['track'])

    track_items_list = [] # Holds all track items from provided playlist id

    # Retrieves tracks from provided playlist id and saves them to 'list'
    playlist_response = spotify.playlist_items(playlist_id=playlist_id, fields=FIELDS, market=user_country, additional_types=['track'])
    track_items_list = playlist_response.get('items') 

    # If there are more pages with tracks, add them to list
    while playlist_response.get('next'):
        playlist_response = spotify.next(playlist_response)
        track_items_list.extend(playlist_response.get('items'))

    # Process list containing all tracks to obtain the final data
    process_data(spotify, track_items_list)

    # Sort list of tracks by track name
    track_items_list.sort(key=lambda x:x.get('track').get('name'))

    """
        track name = track_items_array[#item_index] || item .get('track').get('name')
        track url = .get('track').get('external_urls').get('spotify')
        track artwork = .get('track').get('album').get('images')[0].get('url')
        track artist/s = .get('track').get('artists')[#artist_index].get('name')
        artist/s url = .get('track').get('artists')[0].get('external_urls').get('spotify')
        duration in ms = .get('track').get('duration_ms')
        explicit = .get('track').get('explicit') 
        release date = .get('track').get('album').get('release_date')
        isrc = .get('track').get('external_ids').get('isrc')
        added to playlist (date:time) = .get('added_at')
        person who added track to playlist = .get('added_by').get('id')
    """
    return render_template('playlist.html', spotify=spotify, playlist_details=playlist_details, tracks=track_items_list)

@app.errorhandler(404)
def invalid_route():
    return '404 Page not found'

@app.route('/testing')
@login_required
def testing():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    # Token expired, or broken, return to sign in page
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')    
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    empty = '' #empty to extract actual args
    FIELDS = (  'next,'
                'items(added_at, added_by.id,'
                    'track(album(album_type, images, release_date), artists(external_urls.spotify, name), duration_ms, explicit, external_ids.isrc, external_urls.spotify, id, is_local, name, popularity))'
                )
    
    test_id = '37i9dQZF1EUMDoJuT8yJsl' # dynamic value full code
    test_arr = []
    # result = spotify.playlist_items(playlist_id=test_id, limit=2, fields=FIELDS, market='US', additional_types=['track'])
    result = spotify.playlist_items(playlist_id=test_id, fields=FIELDS, market='US', additional_types=['track'])

    item = result.get('items')[1]

    return render_template('testing.html', item=item)


if __name__ == "__main__":
    app.run(debug=True, port=8000)