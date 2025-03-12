"""
nlp_parser.py
Librairie NLP pour analyser les commandes textuelles de l'assistant vocal Gigi.
"""

import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

# -----------------------------
# CONFIGURATION & VARIABLES
# -----------------------------

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class NLPParser:
    """
    Classe de traitement NLP pour les commandes textuelles de l'assistant Gigi.
    """

    def __init__(self):
        # Liste des verbes d'action de base
        self.intent_verbs = [
            "mets",
            "met",
            "joue",
            "jouer",
            "lance",
            "balance",
            "pause",
            "stop",
            "reprends",
            "reprend",
            # Nouveaux verbes ajoutés ici directement !
            "augmente",
            "monte",
            "baisse",
            "diminue",
            "suivant",
            "précédent",
            "active",
            "désactive",
            "répète"
        ]

        # Synonymes de commandes textuelles → actions
        self.synonymes_intent = {
            # Commandes de navigation
            "musique suivante": "suivant",
            "piste suivante": "suivant",
            "piste précédente": "précédent",
            "titre précédent": "précédent",

            # Modes
            "active le mode aléatoire": "shuffle_on",
            "désactive le mode aléatoire": "shuffle_off",
            "répète la chanson": "repeat_track",
            "répète l'album": "repeat_context",
            "arrête la répétition": "repeat_off",

            # Conversation
            "raconte moi une blague": "blague",
            "quelle heure est il": "heure",
            "comment ça va": "humeur"
        }

        # Liste des salutations
        self.salutations = ["salut", "bonjour", "coucou", "yo", "hello"]

        # Stopwords personnalisés
        french_stopwords = set(stopwords.words('french'))
        self.custom_stopwords = french_stopwords.union(
            {
                "spotify", "musique", "chanson", "s'il", "te", "plait", "la",
                "le", "les", "un", "une", "sur", "dans", "de", "to", "peux",
                "tu"
            }
        )

        self.tokenizer = TreebankWordTokenizer()

    def parse_command(self, phrase: str) -> dict:
        """
        Analyse une phrase textuelle et retourne l'action et l'objet détectés.

        Args:
            phrase (str): La commande utilisateur en texte brut.

        Returns:
            dict: {'action': str, 'object': str}
        """
        phrase = phrase.lower().strip()

        # Vérification salutation
        if phrase in self.salutations:
            return {"action": "salutation", "object": ""}

        # Vérification des synonymes d'intentions
        for key in self.synonymes_intent:
            if key in phrase:
                action = self.synonymes_intent[key]
                return {"action": action, "object": ""}

        # Tokenisation simple
        tokens = self.tokenizer.tokenize(phrase)

        # Recherche de l'action
        action = next((t for t in tokens if t in self.intent_verbs), None)

        if not action:
            return {"action": None, "object": None}

        # Suppression des stopwords et du verbe
        filtered_tokens = [
            token for token in tokens
            if token not in self.custom_stopwords and token != action
        ]

        objet = " ".join(filtered_tokens).strip()

        return {"action": action, "object": objet}
