from pytubefix import exceptions as pytube_exceptions
import pydl
import urllib


def test_wifi_connection():
    """
    Test the Wi-Fi connection by attempting to access a website.

    Returns:
        bool: True if the Wi-Fi connection is successful, False otherwise.
    """
    try:
        urllib.request.urlopen("http://music.youtube.com")
    except:
        raise WifiError


def file_exists():
    pass


def config_error():
    pydl.console.print(
        "[bold red]Invalid config file![/bold red] Please generate a new config file!"
    )
    pydl.generate_config()


def auth_error():
    pydl.console.print(
        "[bold red]Invalid auth file![/bold red] Please generate a new auth file!"
    )
    pydl.auth()


def playlist_error():
    pydl.console.print(
        "[bold red]Invalid playlist/authentification![/bold red] Please check the playlist URL!"
    )


def unavailable_song_error():
    pydl.console.print("[bold red]The song is unavailable![/bold red] Skipping...")


class WifiError(Exception):
    """Raised when the Wi-Fi connection is not successful."""

    def __init__(self, message="Wi-Fi connection failed."):
        self.message = message
        super().__init__(self.message)
