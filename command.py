"""
command.py
Assistant vocal principal : Gigi
Analyse des commandes utilisateur et contrôle Spotify.
"""

from nlp_parser import NLPParser
import spotify_controller as sp_ctrl

# -----------------------------
# EXÉCUTION DES COMMANDES
# -----------------------------


def execute_command(parsed_cmd: dict):
    """
    Exécute la commande en fonction de l'action et de l'objet détectés.

    Args:
        parsed_cmd (dict): {'action': str, 'object': str}
    """
    action = parsed_cmd.get("action")
    objet = parsed_cmd.get("object")

    if not action:
        print("Gigi : Je n'ai pas compris la commande.")
        return

    # Gestion des salutations
    if action == "salutation":
        print("Gigi : Salut ! Comment puis-je t'aider ?")
        return

    # Lecture de musique (jouer une chanson spécifique)
    if action in ["mets", "joue", "jouer", "lance", "balance"]:
        if not objet:
            print("Gigi : Quelle chanson veux-tu écouter ?")
            return
        print(f"Gigi : Je lance '{objet}' sur Spotify !")
        try:
            sp_ctrl.play_song(song_name=objet)
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Pause de la lecture
    if action == "pause":
        print("Gigi : Lecture mise en pause.")
        try:
            sp_ctrl.pause_song()
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Reprendre la lecture en cours
    if action in ["reprends", "reprend"]:
        print("Gigi : Reprise de la lecture.")
        try:
            sp_ctrl.resume_song(
            )  # Nouvelle fonction dans spotify_controller.py
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Arrêter la lecture
    if action == "stop":
        print("Gigi : Arrêt de la lecture.")
        try:
            sp_ctrl.pause_song(
            )  # En attendant d'avoir un stop() dédié, on utilise pause
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

        # Volume
    if action in ["monte", "augmente"]:
        print("Gigi : J'augmente le volume.")
        try:
            sp_ctrl.change_volume(delta=+10)
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    if action in ["baisse", "diminue"]:
        print("Gigi : Je baisse le volume.")
        try:
            sp_ctrl.change_volume(delta=-10)
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Suivant / Précédent
    if action == "suivant":
        print("Gigi : Morceau suivant.")
        try:
            sp_ctrl.next_track()
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    if action == "précédent":
        print("Gigi : Morceau précédent.")
        try:
            sp_ctrl.previous_track()
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Shuffle
    if action == "shuffle_on":
        print("Gigi : Activation du mode aléatoire.")
        try:
            sp_ctrl.shuffle(state=True)
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    if action == "shuffle_off":
        print("Gigi : Désactivation du mode aléatoire.")
        try:
            sp_ctrl.shuffle(state=False)
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Repeat
    if action == "repeat_track":
        print("Gigi : Répétition du morceau activée.")
        try:
            sp_ctrl.repeat(state="track")
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    if action == "repeat_context":
        print("Gigi : Répétition de la playlist activée.")
        try:
            sp_ctrl.repeat(state="context")
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    if action == "repeat_off":
        print("Gigi : Répétition désactivée.")
        try:
            sp_ctrl.repeat(state="off")
        except Exception as e:
            print(f"Gigi : Erreur Spotify - {e}")
        return

    # Réponses conversationnelles
    if action == "blague":
        print(
            "Gigi : Pourquoi les canards ont-ils autant de plumes ? Pour couvrir leur derrière !"
        )
        return

    if action == "heure":
        from datetime import datetime
        heure = datetime.now().strftime("%H:%M")
        print(f"Gigi : Il est {heure}.")
        return

    if action == "humeur":
        print("Gigi : Je vais super bien ! Et toi ?")
        return

    # Action non reconnue
    print(f"Gigi : Action '{action}' non reconnue.")


# -----------------------------
# PROGRAMME PRINCIPAL
# -----------------------------


def main():
    """
    Assistant vocal Gigi : boucle principale.
    """
    print("Assistant Gigi activé ! Tape 'exit' pour quitter.")

    nlp = NLPParser()

    try:
        while True:
            user_input = input("\nDis quelque chose : ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Gigi : À la prochaine !")
                break

            parsed_cmd = nlp.parse_command(user_input)
            execute_command(parsed_cmd)

    except KeyboardInterrupt:
        print("\nInterruption clavier détectée. Fermeture de Gigi.")


# -----------------------------
# LANCEMENT DIRECT
# -----------------------------

if __name__ == "__main__":
    main()
