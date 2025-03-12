"""
test_spotify_controller.py
Script de test pour valider le fonctionnement de spotify_controller.py
"""

import spotify_controller
from time import sleep


def test_play_song():
    print("\n--- TEST : play_song() ---")
    song_name = "Stromae Santé"
    device_name = None  # ou "Olympe", si tu veux forcer
    try:
        spotify_controller.play_song(song_name, device_name)
        print(f"[OK] Lecture de '{song_name}' lancée avec succès")
    except Exception as e:
        print(f"[ERREUR] Impossible de lancer la lecture : {e}")


def test_pause_song():
    print("\n--- TEST : pause_song() ---")
    device_name = None  # ou "Olympe"
    try:
        spotify_controller.pause_song(device_name)
        print(f"[OK] Lecture mise en pause sur le device")
    except Exception as e:
        print(f"[ERREUR] Impossible de mettre en pause : {e}")


def test_authenticate():
    print("\n--- TEST : authenticate() ---")
    try:
        spotify_controller.authenticate()
        print(f"[OK] Authentification réussie et cache mis à jour")
    except Exception as e:
        print(f"[ERREUR] Authentification impossible : {e}")


if __name__ == "__main__":
    print("######## TEST SPOTIFY CONTROLLER ########")

    # Active une fois si tu veux régénérer un token
    # test_authenticate()

    # Lancer la lecture d'un morceau
    test_play_song()

    # Attendre quelques secondes, puis pause
    print("Attente de 5 secondes avant de mettre en pause...")
    sleep(5)

    # Pause du morceau
    test_pause_song()

    print("######## FIN TEST ########")
