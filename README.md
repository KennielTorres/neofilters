
# neofilters

A [Spotify](https://www.spotify.com/)-based application that allows you to view your music playlists and filter their tracks with advanced options. 


## Features

- Search by track name or artists
- View, and search by, the track's ISRC
- Filter by Explicit and/or Clean
- Filter by Release Date
- Filter by Added Date
- View Spotify's track Popularity rating



## Demo

You can view the live demo at [neofilters](https://neofilters.onrender.com)
## Tech Stack

**Frontend:** HTML, CSS, JavaScript, jQuery

**Backend:** Python, Flask, [spotipy library](https://spotipy.readthedocs.io/), [Spotify Web API](https://developer.spotify.com/)

**Hosting:** [Render](https://www.render.com)

## Environment Variables

Before running this project locally, you will need to register an app on the [Spotify Developer Dashboard](https://developer.spotify.com/). Then, from the app just created, add the following environment variables in your terminal on the root directory of the project after installing the dependencies:

`SPOTIPY_CLIENT_ID`

`SPOTIPY_CLIENT_SECRET`

`SPOTIPY_REDIRECT_URI`

- Mac OS/Linux: 
```bash
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-spotify-redirect-uri'
```
- Windows: 
```bash
set SPOTIPY_CLIENT_ID='your-spotify-client-id'
set SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
set SPOTIPY_REDIRECT_URI='your-spotify-redirect-uri'
```

[See Spotipy Reference](https://spotipy.readthedocs.io/en/2.22.1/#authorization-code-flow)


Note* 

The server's port has been reconfigured from Flask's default port (5000) to (8000) on the 'app.py' file. Use as is, or change, as you deem fit.
## Run Locally
Developed and tested with Python 3.11.4

Clone the project

```bash
  git clone https://github.com/KennielTorres/neofilters.git
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 app.py
```

Stop the server
```bash
  Press ctrl+c
```

## FAQ

#### Does neofilters access my Spotify account data during sign in?

No, you are redirected to Spotify's official app authorization page. We temporarily obtain the 'access' and 'refresh' tokens provided by Spotify's authorization response. These are stored in your server session. They contain no information that is personally identifiable 

#### Does neofilters store any of my Spotify data?

None of your data requested from Spotify's Web API is stored by neofilters.
## Author

- [@KennielTorres](https://www.github.com/KennielTorres)

