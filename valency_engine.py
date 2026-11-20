import spacy

nlp = spacy.load("en_core_web_sm")

PESOS_SEVERIDAD = {
    "ALTA": 3,
    "MEDIA": 2,
    "BAJA": 1
}

def _seleccionar_mensaje(nivel_estudiante: str, msg_es: str, msg_en: str) -> str:
    """Adapta el idioma y profundidad de la retroalimentación según el nivel MCER."""
    if nivel_estudiante == "A1-A2":
        return msg_es
    return msg_en

def analizar_valencia_y_orden_oracion(
    texto: str,
    diccionario_valencias: list,
    diccionario_falsos_cognados: list = None,
    nivel_mcer: str = "B1-B2"
) -> dict:
    doc = nlp(texto)
    errores = []

    # 1. ESTRUCTURAS BÁSICAS DE TRANSFERENCIA L1 (Nivel A1-A2 y general)
    # 1a. Omisión de sujeto obligatorio ("Is important" -> "It is important")
    if len(doc) >= 2 and doc[0].lemma_ == "be" and doc[0].pos_ in ["AUX", "VERB"]:
        # Verificar que no sea una pregunta ("Is it...?")
        if not texto.strip().endswith("?"):
            errores.append({
                "tipo_error": "OMISION_SUJETO_EXPLETIVO",
                "severidad": "ALTA",
                "peso": PESOS_SEVERIDAD["ALTA"],
                "nivel_objetivo": "A1-A2",
                "fragmento": f"{doc[0].text} {doc[1].text}",
                "mensaje": _seleccionar_mensaje(
                    nivel_mcer,
                    "Error de estructura básica: En inglés las oraciones declarativas no pueden omitir el sujeto. Usa 'It is...' en lugar de iniciar directo con el verbo.",
                    "Syntactic Structure (Null-Subject Transfer): Unlike Spanish, English is a non-pro-drop language requiring an explicit expletive subject ('It is...')."
                )
            })

    # 1b. Calco de edad con 'have' ("I have 20 years" -> "I am 20 years old")
    for i in range(len(doc) - 2):
        if doc[i].lemma_ == "have" and doc[i + 1].pos_ == "NUM" and doc[i + 2].lemma_ == "year":
            errores.append({
                "tipo_error": "CALCO_LEXICO_EDAD",
                "severidad": "MEDIA",
                "peso": PESOS_SEVERIDAD["MEDIA"],
                "nivel_objetivo": "A1-A2",
                "fragmento": f"{doc[i].text} {doc[i+1].text} {doc[i+2].text}",
                "mensaje": _seleccionar_mensaje(
                    nivel_mcer,
                    "Transferencia L1: En inglés la edad se expresa con el verbo 'to be', no con 'have' (ej. 'I am 20 years old').",
                    "Lexical-Syntactic Transfer: Age in English is predicated with the copula 'to be' rather than 'have' ('I am X years old')."
                )
            })

    # 2. ERRORES DE ORDEN SINTÁCTICO (Adjetivo después de Sustantivo, ej. "car red")
    colores_y_adjetivos_comunes = {"red", "blue", "green", "big", "small", "new", "old", "good", "bad", "black", "white", "expensive", "cheap"}
    for i in range(len(doc) - 1):
        token_actual = doc[i]
        token_siguiente = doc[i + 1]
        es_adjetivo = token_siguiente.pos_ == "ADJ" or token_siguiente.text.lower() in colores_y_adjetivos_comunes

        if token_actual.pos_ in ["NOUN", "PROPN"] and es_adjetivo:
            if i == 0 or doc[i - 1].lemma_ != "be":
                errores.append({
                    "tipo_error": "ORDEN_ADJETIVO_INCORRECTO",
                    "severidad": "MEDIA",
                    "peso": PESOS_SEVERIDAD["MEDIA"],
                    "nivel_objetivo": "A1-A2",
                    "fragmento": f"{token_actual.text} {token_siguiente.text}",
                    "mensaje": _seleccionar_mensaje(
                        nivel_mcer,
                        f"Error de orden sintáctico: En inglés los adjetivos van ANTES del sustantivo. Lo correcto es '{token_siguiente.text} {token_actual.text}'.",
                        f"Word Order Transfer: English requires pre-nominal adjectival modification ('{token_siguiente.text} {token_actual.text}')."
                    )
                })

    # 3. VALENCIAS VERBALES (Marco Argumental y Régimen Preposicional)
    for token in doc:
        if token.pos_ in ["VERB", "AUX"]:
            lema = token.lemma_.lower()
            entrada_verbo = next((item for item in diccionario_valencias if item["verbo"] == lema), None)
            
            if entrada_verbo:
                severidad = entrada_verbo.get("severidad", "MEDIA")
                nivel_item = entrada_verbo.get("nivel_mcer", "B1-B2")
                msg = _seleccionar_mensaje(nivel_mcer, entrada_verbo["explicacion_es"], entrada_verbo["explicacion_en"])

                # Preposiciones Incorrectas por L1
                if "preposiciones_incorrectas" in entrada_verbo:
                    for hijo in token.children:
                        if hijo.dep_ in ["prep", "dative"] and hijo.text.lower() in entrada_verbo["preposiciones_incorrectas"]:
                            errores.append({
                                "tipo_error": "VALENCIA_PREPOSICION_PROHIBIDA",
                                "severidad": severidad,
                                "peso": PESOS_SEVERIDAD[severidad],
                                "nivel_objetivo": nivel_item,
                                "verbo": token.text,
                                "preposicion_incorrecta": hijo.text,
                                "mensaje": msg
                            })

                # Preposiciones Requeridas
                if "preposicion_requerida" in entrada_verbo:
                    tiene_preposicion = any(hijo.text.lower() == entrada_verbo["preposicion_requerida"] for hijo in token.children)
                    if not tiene_preposicion:
                        errores.append({
                            "tipo_error": "VALENCIA_PREPOSICION_FALTANTE",
                            "severidad": severidad,
                            "peso": PESOS_SEVERIDAD[severidad],
                            "nivel_objetivo": nivel_item,
                            "verbo": token.text,
                            "mensaje": msg
                        })

                # Receptores directos sin "to"
                if entrada_verbo.get("requiere_to_para_receptor"):
                    for hijo in token.children:
                        if hijo.dep_ == "dative" or (hijo.dep_ == "obj" and hijo.pos_ in ["PRON", "NOUN"]):
                            tiene_to = any(p.text.lower() == "to" for p in token.children if p.dep_ == "prep")
                            if not tiene_to:
                                errores.append({
                                    "tipo_error": "VALENCIA_RECEPTOR_SIN_TO",
                                    "severidad": severidad,
                                    "peso": PESOS_SEVERIDAD[severidad],
                                    "nivel_objetivo": nivel_item,
                                    "verbo": token.text,
                                    "mensaje": msg
                                })

    # 4. COLOCACIONES ACADÉMICAS (Activado especialmente en niveles B1-B2 y C1)
    if nivel_mcer in ["B1-B2", "C1"]:
        for i in range(len(doc) - 1):
            # Ejemplo: "make research" / "do a mistake"
            if doc[i].lemma_ == "make" and any(c.lemma_ == "research" for c in doc[i].children):
                errores.append({
                    "tipo_error": "COLOCACION_ACADEMICA_C1",
                    "severidad": "BAJA",
                    "peso": PESOS_SEVERIDAD["BAJA"],
                    "nivel_objetivo": "C1",
                    "fragmento": f"{doc[i].text} ... research",
                    "mensaje": _seleccionar_mensaje(
                        nivel_mcer,
                        "Colocación académica: En inglés académico no se usa 'make research', sino 'conduct research' o 'do research'.",
                        "Academic Collocation (Register C1): 'Research' collocates with 'conduct', 'carry out', or 'undertake' rather than 'make'."
                    )
                })

    # 5. DETECCIÓN DE FALSOS COGNADOS
    if diccionario_falsos_cognados:
        for token in doc:
            lema_token = token.lemma_.lower()
            palabra_token = token.text.lower()
            falso_amigo = next((item for item in diccionario_falsos_cognados if item["palabra"] in [palabra_token, lema_token]), None)

            if falso_amigo:
                severidad = falso_amigo.get("severidad", "MEDIA")
                errores.append({
                    "tipo_error": "FALSO_COGNADO_DETECTADO",
                    "severidad": severidad,
                    "peso": PESOS_SEVERIDAD[severidad],
                    "nivel_objetivo": falso_amigo.get("nivel_mcer", "B1-B2"),
                    "palabra_usada": token.text,
                    "posible_confusion": falso_amigo["confusion_es"],
                    "sugerencia": falso_amigo["correccion_sugerida"],
                    "mensaje": _seleccionar_mensaje(nivel_mcer, falso_amigo["explicacion_es"], falso_amigo["explicacion_en"])
                })

    # Ordenar errores de mayor a menor severidad e índice de afectación
    errores.sort(key=lambda x: x["peso"], reverse=True)
    puntaje_severidad_total = sum(e["peso"] for e in errores)

    return {
        "errores": errores,
        "puntaje_severidad_total": puntaje_severidad_total
    }