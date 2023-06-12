
import secrets
import functools
from flask import Flask, session, request, redirect, render_template, url_for
import spotipy
from flask_session import Session
from utils.utils import process_data

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = secrets.token_hex(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
Session(app)

SCOPE = 'user-read-private user-read-email user-library-read playlist-read-private playlist-read-collaborative user-top-read'

# Decorator to validate that user has signed in and can enter target route
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "token_info" not in session:
            return redirect(url_for("index"))
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

@app.route('/about')
def about():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=SCOPE,
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    auth_url = auth_manager.get_authorize_url()

    return render_template('about.html', auth_url=auth_url)

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

    return redirect('/menu')


@app.route('/menu')
@login_required
def menu():
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


    return render_template('menu.html', spotify=spotify, playlists_array=playlists_array)


@app.route('/signout')
@login_required
def signout():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/playlist/<playlist_id>', methods=['GET', 'POST'])
@app.route('/playlist/<playlist_id>/', methods=['GET', 'POST'])
@login_required
def playlist(playlist_id):
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    # Token expired, or broken, return to sign in page
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')    
    
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Grabs current user's country
    user_country = spotify.current_user().get('country')

    # Fields supplied for wanted response
    FIELDS = (  'next,'
                'items(added_at,'
                    'track(album(images, release_date, name, external_urls.spotify), artists(external_urls.spotify, name), duration_ms, explicit, external_ids.isrc, external_urls.spotify, id, name, popularity))'
                )
    
    # Response holding playlist name and public/private status
    playlist_details = spotify.playlist(playlist_id=playlist_id, fields=('id, name'), market=user_country, additional_types=['track'])

    track_items_list = [] # Holds all track items from provided playlist id

    # Retrieves tracks from provided playlist id and saves them to 'list'
    playlist_response = spotify.playlist_items(playlist_id=playlist_id, fields=FIELDS, market=user_country, additional_types=['track'])
    track_items_list = playlist_response.get('items') 

    # If there are more pages with tracks, add them to list
    while playlist_response.get('next'):
        playlist_response = spotify.next(playlist_response)
        track_items_list.extend(playlist_response.get('items'))

    # Process list containing all tracks to obtain the final data
    track_items_list = process_data(track_items_list)

    return render_template('playlist.html', spotify=spotify, user_country=user_country, playlist_details=playlist_details, tracks=track_items_list, request=request)

@app.errorhandler(404)
def invalid_route():
    return '404 Page not found'


if __name__ == "__main__":
    app.run(debug=True, port=8000)