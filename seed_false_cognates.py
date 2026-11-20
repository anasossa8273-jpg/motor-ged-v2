import json

falsos_cognados = [
    {
        "palabra": "actually",
        "nivel_mcer": "B1-B2",
        "severidad": "MEDIA",
        "confusion_es": "actualmente",
        "correccion_sugerida": "currently / nowadays",
        "explicacion_es": "'Actually' no significa 'actualmente', sino 'en realidad'. Para decir 'actualmente', usa 'currently'.",
        "explicacion_en": "Lexical Transfer (False Friend): 'Actually' means 'in fact'; use 'currently' or 'nowadays' to express present time."
    },
    {
        "palabra": "realize",
        "nivel_mcer": "B1-B2",
        "severidad": "MEDIA",
        "confusion_es": "realizar (hacer)",
        "correccion_sugerida": "carry out / conduct / perform",
        "explicacion_es": "'Realize' significa darse cuenta. Para 'realizar un proyecto o investigación', usa 'carry out' o 'conduct'.",
        "explicacion_en": "Lexical Transfer (False Friend): 'Realize' means to become aware of. For academic tasks, use 'conduct' or 'carry out'."
    },
    {
        "palabra": "assist",
        "nivel_mcer": "B1-B2",
        "severidad": "MEDIA",
        "confusion_es": "asistir (ir a clase/evento)",
        "correccion_sugerida": "attend",
        "explicacion_es": "'Assist' significa ayudar. Para 'asistir a una clase o conferencia', debes usar 'attend'.",
        "explicacion_en": "Lexical Transfer (False Friend): 'Assist' means to help. Use 'attend' when referring to classes or academic events."
    },
    {
        "palabra": "sensible",
        "nivel_mcer": "B1-B2",
        "severidad": "BAJA",
        "confusion_es": "sensible (emotivo)",
        "correccion_sugerida": "sensitive",
        "explicacion_es": "'Sensible' significa sensato/razonable. Para decir que alguien es emotivo o sensible, usa 'sensitive'.",
        "explicacion_en": "Lexical Transfer (False Friend): 'Sensible' denotes practical judgment; use 'sensitive' for emotional responsiveness."
    },
    {
        "palabra": "embarrassed",
        "nivel_mcer": "A1-A2",
        "severidad": "ALTA",
        "confusion_es": "embarazada",
        "correccion_sugerida": "pregnant",
        "explicacion_es": "'Embarrassed' significa sentir vergüenza. Para decir 'embarazada', la palabra correcta es 'pregnant'.",
        "explicacion_en": "Lexical Transfer (False Friend): 'Embarrassed' means ashamed; use 'pregnant' to refer to gestation."
    },
    {
        "palabra": "carpet",
        "nivel_mcer": "A1-A2",
        "severidad": "BAJA",
        "confusion_es": "carpeta",
        "correccion_sugerida": "folder",
        "explicacion_es": "'Carpet' es una alfombra. Para referirte a una carpeta de documentos, usa 'folder'.",
        "explicacion_en": "Lexical Transfer (False Friend): 'Carpet' refers to floor covering; use 'folder' for documents."
    }
]

with open("false_cognates_dict.json", "w", encoding="utf-8") as archivo:
    json.dump(falsos_cognados, archivo, indent=4, ensure_ascii=False)

print("✅ Diccionario de Falsos Cognados actualizado con MCER y Severidad.")