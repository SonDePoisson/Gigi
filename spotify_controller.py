"""
spotify_controller.py
Librairie pour contrôler Spotify Connect depuis l'API Spotify.
"""

import os
from typing import Optional, List, Dict
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# -----------------------------
# CONFIGURATION & VARIABLES
# -----------------------------

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
DEFAULT_DEVICE_NAME = os.getenv("RASPO_DEVICE_NAME")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise EnvironmentError(
        "CLIENT_ID, CLIENT_SECRET et REDIRECT_URI doivent être définis dans les variables d'environnement."
    )

SCOPE = "user-read-playback-state user-modify-playback-state"
DEFAULT_CACHE_PATH = os.path.expanduser("~/.config/spotify_cache/.cache")

# -----------------------------
# FONCTIONS PRIVÉES INTERNES
# -----------------------------


def _init_spotify_client(
    cache_path: str = DEFAULT_CACHE_PATH,
    open_browser: bool = False
) -> spotipy.Spotify:
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=open_browser,
        cache_path=cache_path
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def _get_devices(sp: spotipy.Spotify) -> List[Dict]:
    return sp.devices().get("devices", [])


def _find_device_id(devices: List[Dict], device_name: str) -> Optional[str]:
    for device in devices:
        if device["name"].lower() == device_name.lower():
            return device["id"]
    return None


def _search_track_uri(sp: spotipy.Spotify, song_name: str) -> Optional[str]:
    results = sp.search(q=song_name, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    return tracks[0]['uri'] if tracks else None


# -----------------------------
# API PUBLIQUE
# -----------------------------


def play_song(song_name: str, device_name: Optional[str] = None) -> None:
    """
    Joue un morceau Spotify sur un device donné.

    Args:
        song_name (str): Nom du morceau à lire.
        device_name (Optional[str]): Device cible (défaut : RASPO_DEVICE_NAME).
    """
    sp = _init_spotify_client()
    devices = _get_devices(sp)

    final_device = device_name or DEFAULT_DEVICE_NAME
    if not final_device:
        raise ValueError(
            "Aucun device défini. Spécifiez device_name ou la variable RASPO_DEVICE_NAME."
        )

    device_id = _find_device_id(devices, final_device)
    if not device_id:
        raise ValueError(f"Device '{final_device}' introuvable.")

    uri = _search_track_uri(sp, song_name)
    if not uri:
        raise ValueError(f"Morceau '{song_name}' introuvable sur Spotify.")

    sp.start_playback(device_id=device_id, uris=[uri])


def resume_song(device_name: Optional[str] = None) -> None:
    """
    Reprend la lecture Spotify sur le device spécifié.

    Args:
        device_name (Optional[str]): Device cible (défaut : RASPO_DEVICE_NAME).
    """
    sp = _init_spotify_client()
    devices = _get_devices(sp)

    final_device = device_name or DEFAULT_DEVICE_NAME
    if not final_device:
        raise ValueError(
            "Aucun device défini. Spécifiez device_name ou RASPO_DEVICE_NAME."
        )

    device_id = _find_device_id(devices, final_device)
    if not device_id:
        raise ValueError(f"Device '{final_device}' introuvable.")

    sp.start_playback(
        device_id=device_id
    )  # ATTENTION : pas d'URIs ici => relance la lecture courante


def pause_song(device_name: Optional[str] = None) -> None:
    """
    Met en pause la lecture sur le device spécifié.

    Args:
        device_name (Optional[str]): Device cible (défaut : RASPO_DEVICE_NAME).
    """
    sp = _init_spotify_client()
    devices = _get_devices(sp)

    final_device = device_name or DEFAULT_DEVICE_NAME
    device_id = _find_device_id(devices, final_device)
    if not device_id:
        raise ValueError(f"Device '{final_device}' introuvable pour pause.")

    sp.pause_playback(device_id=device_id)


def next_track(device_name: Optional[str] = None) -> None:
    """Passe au morceau suivant."""
    sp = _init_spotify_client()
    devices = _get_devices(sp)
    device_id = _find_device_id(devices, device_name or DEFAULT_DEVICE_NAME)
    if not device_id:
        raise ValueError(f"Device '{device_name}' introuvable.")
    sp.next_track(device_id=device_id)


def previous_track(device_name: Optional[str] = None) -> None:
    """Reviens au morceau précédent."""
    sp = _init_spotify_client()
    devices = _get_devices(sp)
    device_id = _find_device_id(devices, device_name or DEFAULT_DEVICE_NAME)
    if not device_id:
        raise ValueError(f"Device '{device_name}' introuvable.")
    sp.previous_track(device_id=device_id)


def change_volume(delta: int, device_name: Optional[str] = None) -> None:
    """Augmente ou baisse le volume du device de delta %."""
    sp = _init_spotify_client()
    devices = _get_devices(sp)
    device_id = _find_device_id(devices, device_name or DEFAULT_DEVICE_NAME)
    if not device_id:
        raise ValueError(f"Device '{device_name}' introuvable.")

    # Spotify ne donne pas le volume actuel : on fixe à 50% comme base
    current_volume = 50
    new_volume = max(0, min(100, current_volume + delta))
    sp.volume(new_volume, device_id=device_id)


def shuffle(state: bool = True, device_name: Optional[str] = None) -> None:
    """Active ou désactive le mode shuffle."""
    sp = _init_spotify_client()
    devices = _get_devices(sp)
    device_id = _find_device_id(devices, device_name or DEFAULT_DEVICE_NAME)
    if not device_id:
        raise ValueError(f"Device '{device_name}' introuvable.")
    sp.shuffle(state=state, device_id=device_id)


def repeat(state: str = 'track', device_name: Optional[str] = None) -> None:
    """
    Répète un track/context/off.

    state: 'track' | 'context' | 'off'
    """
    sp = _init_spotify_client()
    devices = _get_devices(sp)
    device_id = _find_device_id(devices, device_name or DEFAULT_DEVICE_NAME)
    if not device_id:
        raise ValueError(f"Device '{device_name}' introuvable.")
    sp.repeat(state=state, device_id=device_id)


def authenticate(cache_path: str = DEFAULT_CACHE_PATH) -> None:
    """
    Authentifie manuellement pour stocker un token OAuth.

    Args:
        cache_path (str): Emplacement du fichier cache.
    """
    sp = _init_spotify_client(cache_path=cache_path, open_browser=False)
    _get_devices(sp)
    print(f"Authentification terminée. Cache stocké à : {cache_path}")


# -----------------------------
# LANCEMENT MANUEL (DEBUG)
# -----------------------------

if __name__ == "__main__":
    authenticate()
