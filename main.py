import argparse
import configparser
import spotipy
import spotipy.util as util

def like_playlist(username, playlist_id, client_id, client_secret):
    token = util.prompt_for_user_token(username, scope='playlist-modify-public', client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost/')
    if token:
        sp = spotipy.Spotify(auth=token)

        playlist = sp.playlist(playlist_id)
        playlist_uri = playlist['uri']

        sp.current_user_saved_tracks_add(None, playlist_uri)
        print(f"Liked playlist {playlist_id} for user {username}")
    else:
        print(f"Failed to get token for user {username}")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    users = config.sections()
    playlists = {}
    for user in users:
        playlists[user] = config[user]['playlists'].split(',')

    parser = argparse.ArgumentParser(description='Like a Spotify playlist')
    parser.add_argument('username', type=str, help='Spotify username')
    parser.add_argument('playlist_link', type=str, help='Spotify playlist link')
    args = parser.parse_args()

    playlist_id = args.playlist_link.split('/')[-1].split('?')[0]

    for user in users:
        if user == args.username:
            client_id = config[user]['client_id']
            client_secret = config[user]['client_secret']

            like_playlist(user, playlist_id, client_id, client_secret)