from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_estado_servidor():
    res = client.get("/estado")
    assert res.status_code == 200
    assert res.json()["estado"] == "activo"

def test_orden_adjetivo_y_retroalimentacion_a1():
    res = client.post("/analizar", json={"texto": "I bought a car red", "nivel_mcer": "A1-A2"})
    data = res.json()
    assert data["total_errores"] == 1
    assert data["errores_detectados"][0]["tipo_error"] == "ORDEN_ADJETIVO_INCORRECTO"
    assert "ANTES del sustantivo" in data["errores_detectados"][0]["mensaje"]

def test_valencia_severidad_alta_y_ordenamiento():
    # Oración con error de severidad MEDIA ("car red") y severidad ALTA ("discussed about")
    res = client.post("/analizar", json={"texto": "We discussed about the car red", "nivel_mcer": "B1-B2"})
    data = res.json()
    assert data["total_errores"] == 2
    assert data["indice_severidad_global"] == 5  # 3 (ALTA) + 2 (MEDIA)
    # Verifica que el error de ALTA severidad aparezca primero
    assert data["errores_detectados"][0]["severidad"] == "ALTA"
    assert "Metalinguistic Feedback" in data["errores_detectados"][0]["mensaje"]

def test_transferencia_basica_a1_sujeto_omitido():
    res = client.post("/analizar", json={"texto": "Is important to study", "nivel_mcer": "A1-A2"})
    data = res.json()
    assert data["total_errores"] == 1
    assert data["errores_detectados"][0]["tipo_error"] == "OMISION_SUJETO_EXPLETIVO"

def test_colocacion_academica_c1():
    res = client.post("/analizar", json={"texto": "We need to make research on this topic", "nivel_mcer": "C1"})
    data = res.json()
    assert any(e["tipo_error"] == "COLOCACION_ACADEMICA_C1" for e in data["errores_detectados"])

def test_oracion_sin_errores():
    res = client.post("/analizar", json={"texto": "We discussed the red car yesterday", "nivel_mcer": "B1-B2"})
    assert res.json()["total_errores"] == 0
    assert res.json()["indice_severidad_global"] == 0