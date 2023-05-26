'''
    flask spotipy Flask-Session
'''
import os
import functools
from flask import Flask, session, request, redirect, render_template, url_for
import spotipy
from flask_session import Session

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

    # If there are more pages with playlists, add them to array.
    while playlist_data.get('next'):
        playlist_data = spotify.next(playlist_data)
        playlists_array.extend(playlist_data.get('items'))


    return render_template('dashboard.html', spotify=spotify, playlists_array=playlists_array)


@app.route('/signout')
@login_required
def signout():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/playlist/<playlist_id>')
@login_required
def playlist(country='US', playlist_id=0):
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    # Token expired, or broken, return to sign in page
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')    
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return 'playlist'

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
    FIELDS = '' #empty to extract actual args

    test_id = '6E1grnrnbXTGP9fDJQMzNb' # dynamic value full code
    
    result = spotify.playlist_items(playlist_id=test_id, fields=FIELDS, limit=10, offset=0, market='US', additional_types=['track'])
    return result

    # return spotify.audio_features(test_id)

if __name__ == "__main__":
    app.run(debug=True, port=8000)