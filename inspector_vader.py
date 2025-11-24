from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import math


# --------------------------
# Inicializar VADER
# --------------------------

analyzer = SentimentIntensityAnalyzer()
lexicon = analyzer.lexicon
from vaderSentiment.vaderSentiment import NEGATE, BOOSTER_DICT

# --------------------------
# Funciones auxiliares
# --------------------------

def is_negated(token):
    return token.lower() in NEGATE

def scalar_inc_dec(token, valence):
    """Calcula el efecto de intensificadores/atenuadores"""
    t = token.lower()
    if t in BOOSTER_DICT:
        scalar = BOOSTER_DICT[t]
        if valence < 0:
            scalar *= -1
        return scalar
    return 0.0

def normalize(score, alpha=15):
    """Normalización final del compound (función logística de VADER)"""
    return score / math.sqrt((score * score) + alpha)

# --------------------------
# Procesamiento principal
# --------------------------

def vader_step_by_step(text):
    print("\n=== TEXT ===")
    print(text)
    print()

    # Tokenización parecida a VADER
    tokens = re.findall(r"\w+|[!?.]", text.lower())

    print("=== TOKENS ===")
    print(tokens)
    print()

    sentiments = []
    print("=== INITIAL VALENCES ===")
    for i, token in enumerate(tokens):
        valence = lexicon.get(token, 0.0)
        if valence != 0:
            print(f"{i:2d}  {token:15s} → {valence}")
        sentiments.append(valence)
    print()

    print("=== ADJUSTMENTS (INTENSIFIERS / NEGATIONS) ===")
    for i, token in enumerate(tokens):
        valence = sentiments[i]
        if valence != 0:

            # Intensificadores en las 3 palabras previas
            for j in range(max(0, i - 3), i):
                scalar = scalar_inc_dec(tokens[j], valence)
                if scalar != 0:
                    sentiments[i] += scalar
                    print(f"  Booster '{tokens[j]}' affects '{token}': {scalar:+.3f}")

            # Negación 1 palabra antes
            if i > 0 and is_negated(tokens[i - 1]):
                sentiments[i] *= -0.74
                print(f"  Negation '{tokens[i-1]}' affects '{token}' (× -0.74)")

            # Negación 2 palabras antes
            if i > 1 and is_negated(tokens[i - 2]):
                sentiments[i] *= -0.74
                print(f"  Negation '{tokens[i-2]}' affects '{token}' (× -0.74)")

    print()
    print("=== FINAL ADJUSTED VALENCES ===")
    for token, val in zip(tokens, sentiments):
        if val != 0:
            print(f"{token:15s} → {val:+.3f}")
    print()

    # --------------------------
    # Compound
    # --------------------------
    total = sum(sentiments)
    compound = normalize(total)

    print("=== RAW SUM OF VALENCES ===")
    print(total)

    print("\n=== NORMALIZED COMPOUND (LOGISTIC) ===")
    print(compound)

    print("\n=== OFFICIAL VADER SCORES ===")
    print(analyzer.polarity_scores(text))


# --------------------------
# Example
# --------------------------

from translate import Translator
traductor = Translator(to_lang="en")
#frase = 'El uso excesivo de pantallas lleva a los niños a necesitarlas aún más'
frase = "¡Desastre financiero en Tokio! La bolsa se desploma en un terriblemente desastroso martes, fatal pero no catastrófico."
frase_eng = traductor.translate(frase)
vader_step_by_step(frase_eng)

