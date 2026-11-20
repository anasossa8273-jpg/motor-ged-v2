import json

datos_valencia = [
    # --- ALTA SEVERIDAD: ALTERACIÓN DEL MARCO ARGUMENTAL (B1-B2) ---
    {
        "verbo": "discuss",
        "nivel_mcer": "B1-B2",
        "severidad": "ALTA",
        "preposiciones_incorrectas": ["about"],
        "explicacion_es": "En español decimos 'discutir sobre algo', pero 'discuss' en inglés es transitivo directo y NO admite 'about'.",
        "explicacion_en": "Metalinguistic Feedback (Valency): 'Discuss' is a strict transitive verb taking a direct object without the preposition 'about' (use 'discuss the problem')."
    },
    {
        "verbo": "answer",
        "nivel_mcer": "B1-B2",
        "severidad": "ALTA",
        "preposiciones_incorrectas": ["to"],
        "explicacion_es": "En español decimos 'responder a la pregunta', pero 'answer' toma objeto directo sin 'to' (ej. 'answer the question').",
        "explicacion_en": "Metalinguistic Feedback (Valency): As a verb, 'answer' governs a direct object directly without 'to' (e.g., 'answer the question')."
    },
    {
        "verbo": "explain",
        "nivel_mcer": "B1-B2",
        "severidad": "ALTA",
        "requiere_to_para_receptor": True,
        "explicacion_es": "En español decimos 'le expliqué a él', pero 'explain' exige la preposición 'to' antes de la persona (ej. 'explain to him', no 'explain him').",
        "explicacion_en": "Metalinguistic Feedback (Argument Structure): 'Explain' does not allow dative shift; the recipient must be introduced by 'to' (e.g., 'explain it to him')."
    },

    # --- MEDIA SEVERIDAD: RÉGIMEN PREPOSICIONAL REGIDO (A1-A2 / B1-B2) ---
    {
        "verbo": "depend",
        "nivel_mcer": "B1-B2",
        "severidad": "MEDIA",
        "preposicion_requerida": "on",
        "preposiciones_incorrectas": ["of"],
        "explicacion_es": "En español decimos 'depender de', pero en inglés 'depend' exige la preposición 'on'.",
        "explicacion_en": "Prepositional Valency: 'Depend' governs the preposition 'on' (or 'upon'), never 'of' ('depend on')."
    },
    {
        "verbo": "marry",
        "nivel_mcer": "B1-B2",
        "severidad": "MEDIA",
        "preposiciones_incorrectas": ["with"],
        "explicacion_es": "En español decimos 'casarse con', pero 'marry' no lleva 'with' (usa objeto directo o 'married to').",
        "explicacion_en": "Prepositional Valency: 'Marry' takes a direct object ('marry someone') or uses 'to' in passive/adjectival forms ('married to'), not 'with'."
    },
    {
        "verbo": "arrive",
        "nivel_mcer": "A1-A2",
        "severidad": "MEDIA",
        "preposiciones_incorrectas": ["to"],
        "explicacion_es": "En español decimos 'llegar a', pero en inglés 'arrive' usa 'at' (lugares específicos) o 'in' (ciudades/países), NUNCA 'to'.",
        "explicacion_en": "Prepositional Valency: 'Arrive' collocates with 'at' (specific points) or 'in' (cities/countries), never directional 'to'."
    },
    {
        "verbo": "listen",
        "nivel_mcer": "A1-A2",
        "severidad": "MEDIA",
        "preposicion_requerida": "to",
        "explicacion_es": "En español decimos 'escuchar música', pero 'listen' requiere obligatoriamente 'to' antes del objeto ('listen to music').",
        "explicacion_en": "Prepositional Valency: 'Listen' is an intransitive verb requiring the preposition 'to' before its object ('listen to music')."
    },
    {
        "verbo": "pay",
        "nivel_mcer": "A1-A2",
        "severidad": "MEDIA",
        "preposicion_requerida": "for",
        "explicacion_es": "En español decimos 'pagar la cena', pero en inglés pagar por un bien o servicio exige 'pay for'.",
        "explicacion_en": "Prepositional Valency: Paying in exchange for goods or services requires the prepositional complement 'for' ('pay for dinner')."
    },
    {
        "verbo": "wait",
        "nivel_mcer": "A1-A2",
        "severidad": "MEDIA",
        "preposicion_requerida": "for",
        "explicacion_es": "En español decimos 'esperar el autobús', pero 'wait' exige la preposición 'for' ('wait for the bus').",
        "explicacion_en": "Prepositional Valency: 'Wait' requires the preposition 'for' to introduce the anticipated object or person ('wait for the bus')."
    },
    {
        "verbo": "ask",
        "nivel_mcer": "A1-A2",
        "severidad": "MEDIA",
        "preposicion_requerida": "for",
        "explicacion_es": "En español decimos 'pedir ayuda', pero pedir algo exige 'ask for' ('ask for help').",
        "explicacion_en": "Prepositional Valency: Requesting an object or favor requires 'ask for' ('ask for help')."
    },
    {
        "verbo": "look",
        "nivel_mcer": "A1-A2",
        "severidad": "MEDIA",
        "preposicion_requerida": "for",
        "explicacion_es": "En español decimos 'buscar' o 'mirar', pero en inglés buscar requiere 'look for' y mirar requiere 'look at'.",
        "explicacion_en": "Prepositional Valency: 'Look' requires a prepositional particle to complete its semantic frame ('look for' / 'look at')."
    }
]

with open("valency_dict.json", "w", encoding="utf-8") as archivo:
    json.dump(datos_valencia, archivo, indent=4, ensure_ascii=False)

print("✅ Diccionario de valencias ponderado por MCER y Severidad generado.")