"""
test_nlp_unit.py
Tests unitaires pour l'analyse de commandes textuelles avec corrections
"""

import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

# -------------------
# Chargement des données NLTK (stopwords)
# -------------------
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# -------------------
# Config NLP
# -------------------

# Liste des verbes d'action reconnus
INTENT_VERBS = [
    "mets", "met", "joue", "jouer", "lance", "balance", "pause", "stop",
    "reprends", "reprend"
]

# Dictionnaire de synonymes vers intentions connues
SYNONYMES_INTENT = {"fais une pause": "pause", "peux-tu jouer": "joue"}

# Stopwords en français + personnalisés
FRENCH_STOPWORDS = set(stopwords.words('french'))
CUSTOM_STOPWORDS = FRENCH_STOPWORDS.union(
    {
        "spotify", "musique", "chanson", "s'il", "te", "plait", "la", "le",
        "les", "un", "une", "sur", "dans", "de", "to", "peux", "tu"
    }
)

# Tokenizer simple
tokenizer = TreebankWordTokenizer()


# -------------------
# Fonction d'analyse de commande
# -------------------
def parse_command(phrase: str) -> dict:
    """
    Analyse une phrase et retourne l'action et l'objet extraits.
    
    Args:
        phrase (str): La commande textuelle utilisateur.
    
    Returns:
        dict: Dictionnaire contenant 'action' (str) et 'object' (str)
    """
    phrase = phrase.lower().strip()

    # Vérifie si la phrase correspond à une intention complète
    for key in SYNONYMES_INTENT:
        if key in phrase:
            action = SYNONYMES_INTENT[key]
            objet = ""  # Pas d'objet dans ce cas précis
            return {"action": action, "object": objet}

    # Tokenisation
    tokens = tokenizer.tokenize(phrase)

    # Cherche l'action (verbe)
    action = None
    for token in tokens:
        if token in INTENT_VERBS:
            action = token
            break

    if not action:
        return {"action": None, "object": None}

    # Filtrer les stopwords + le verbe d'action détecté
    filtered_tokens = [
        token for token in tokens
        if token not in CUSTOM_STOPWORDS and token != action
    ]

    objet = " ".join(filtered_tokens).strip()

    return {"action": action, "object": objet}


# -------------------
# Fonction de tests unitaires
# -------------------
def run_tests():
    """
    Exécute une série de tests sur différentes phrases pour valider le parsing.
    """
    # Dictionnaire de tests : {phrase: (action attendue, objet attendu)}
    test_phrases = {
        "Mets Stromae Santé sur Spotify": ("mets", "stromae santé"),
        "Joue Fade to Black de Metallica": ("joue", "fade black metallica"),
        "Pause la musique": ("pause", ""),
        "Stop la chanson": ("stop", ""),
        "Reprends la lecture": ("reprends", "lecture"),
        "Lance Booba DKR sur Spotify": ("lance", "booba dkr"),
        "Balance une musique chill sur Spotify": ("balance", "chill"),
        "Peux-tu jouer Paroles Paroles s'il te plaît ?":
            ("joue", "paroles paroles"),
        "Fais une pause": ("pause", ""),
        "Salut, comment ça va ?": (None, None)
    }

    print("\n===== TESTS UNITAIRES NLP COMMANDES =====\n")

    success_count = 0
    fail_count = 0

    for phrase, expected in test_phrases.items():
        result = parse_command(phrase)
        action = result["action"]
        objet = result["object"]

        expected_action, expected_objet = expected

        test_pass = (action == expected_action) and (objet == expected_objet)

        status = "OK" if test_pass else "FAIL"

        print(f"[{status}] Phrase : '{phrase}'")
        print(
            f"  Action attendue : '{expected_action}' | Action détectée : '{action}'"
        )
        print(
            f"  Objet attendu   : '{expected_objet}' | Objet détecté   : '{objet}'\n"
        )

        if test_pass:
            success_count += 1
        else:
            fail_count += 1

    print("===== BILAN FINAL =====")
    print(f"Succès : {success_count} / {success_count + fail_count} tests")
    print("=========================\n")


# -------------------
# Exécution directe du script
# -------------------
if __name__ == "__main__":
    run_tests()
"""
test_nlp_unit.py
Tests unitaires pour l'analyse de commandes textuelles avec corrections
"""

import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords

# -------------------
# Chargement des données NLTK (stopwords)
# -------------------
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# -------------------
# Config NLP
# -------------------

# Liste des verbes d'action reconnus
INTENT_VERBS = [
    "mets", "met", "joue", "jouer", "lance", "balance", "pause", "stop",
    "reprends", "reprend"
]

# Dictionnaire de synonymes vers intentions connues
SYNONYMES_INTENT = {"fais une pause": "pause", "peux-tu jouer": "joue"}

# Stopwords en français + personnalisés
FRENCH_STOPWORDS = set(stopwords.words('french'))
CUSTOM_STOPWORDS = FRENCH_STOPWORDS.union(
    {
        "spotify", "musique", "chanson", "s'il", "te", "plait", "la", "le",
        "les", "un", "une", "sur", "dans", "de", "to", "peux", "tu"
    }
)

# Tokenizer simple
tokenizer = TreebankWordTokenizer()


# -------------------
# Fonction d'analyse de commande
# -------------------
def parse_command(phrase: str) -> dict:
    """
    Analyse une phrase et retourne l'action et l'objet extraits.
    
    Args:
        phrase (str): La commande textuelle utilisateur.
    
    Returns:
        dict: Dictionnaire contenant 'action' (str) et 'object' (str)
    """
    phrase = phrase.lower().strip()

    # Vérifie si la phrase correspond à une intention complète
    for key in SYNONYMES_INTENT:
        if key in phrase:
            action = SYNONYMES_INTENT[key]
            objet = ""  # Pas d'objet dans ce cas précis
            return {"action": action, "object": objet}

    # Tokenisation
    tokens = tokenizer.tokenize(phrase)

    # Cherche l'action (verbe)
    action = None
    for token in tokens:
        if token in INTENT_VERBS:
            action = token
            break

    if not action:
        return {"action": None, "object": None}

    # Filtrer les stopwords + le verbe d'action détecté
    filtered_tokens = [
        token for token in tokens
        if token not in CUSTOM_STOPWORDS and token != action
    ]

    objet = " ".join(filtered_tokens).strip()

    return {"action": action, "object": objet}


# -------------------
# Fonction de tests unitaires
# -------------------
def run_tests():
    """
    Exécute une série de tests sur différentes phrases pour valider le parsing.
    """
    # Dictionnaire de tests : {phrase: (action attendue, objet attendu)}
    test_phrases = {
        "Mets Stromae Santé sur Spotify": ("mets", "stromae santé"),
        "Joue Fade to Black de Metallica": ("joue", "fade black metallica"),
        "Pause la musique": ("pause", ""),
        "Stop la chanson": ("stop", ""),
        "Reprends la lecture": ("reprends", "lecture"),
        "Lance Booba DKR sur Spotify": ("lance", "booba dkr"),
        "Balance une musique chill sur Spotify": ("balance", "chill"),
        "Peux-tu jouer Paroles Paroles s'il te plaît ?":
            ("joue", "paroles paroles"),
        "Fais une pause": ("pause", ""),
        "Salut, comment ça va ?": (None, None)
    }

    print("\n===== TESTS UNITAIRES NLP COMMANDES =====\n")

    success_count = 0
    fail_count = 0

    for phrase, expected in test_phrases.items():
        result = parse_command(phrase)
        action = result["action"]
        objet = result["object"]

        expected_action, expected_objet = expected

        test_pass = (action == expected_action) and (objet == expected_objet)

        status = "OK" if test_pass else "FAIL"

        print(f"[{status}] Phrase : '{phrase}'")
        print(
            f"  Action attendue : '{expected_action}' | Action détectée : '{action}'"
        )
        print(
            f"  Objet attendu   : '{expected_objet}' | Objet détecté   : '{objet}'\n"
        )

        if test_pass:
            success_count += 1
        else:
            fail_count += 1

    print("===== BILAN FINAL =====")
    print(f"Succès : {success_count} / {success_count + fail_count} tests")
    print("=========================\n")


# -------------------
# Exécution directe du script
# -------------------
if __name__ == "__main__":
    run_tests()
