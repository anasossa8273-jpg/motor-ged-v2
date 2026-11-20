import json
import os
import subprocess
import sys
import time
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from valency_engine import analizar_valencia_y_orden_oracion

app = FastAPI(
    title="Motor GED de Interferencia L1 (CUCEA / UdeG)",
    description="API de diagnóstico sintáctico-semántico ponderado por severidad y escalable por niveles del MCER (A1-C1).",
    version="2.0.0"
)

def cargar_o_generar_json(nombre_archivo: str, script_generador: str):
    if not os.path.exists(nombre_archivo):
        print(f"⚠️ '{nombre_archivo}' no encontrado. Ejecutando '{script_generador}'...")
        if os.path.exists(script_generador):
            subprocess.run([sys.executable, script_generador], check=True)
        else:
            raise RuntimeError(f"Error crítico: Falta '{nombre_archivo}' y su script '{script_generador}'.")
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

VALENCIAS = cargar_o_generar_json("valency_dict.json", "seed_valency.py")
FALSOS_COGNADOS = cargar_o_generar_json("false_cognates_dict.json", "seed_false_cognates.py")


class SolicitudAnalisis(BaseModel):
    texto: str = Field(..., json_schema_extra={"example": "We discussed about the car red"})
    nivel_mcer: Literal["A1-A2", "B1-B2", "C1"] = Field(
        default="B1-B2",
        description="Nivel del estudiante según el Marco Común Europeo (adapta el idioma y enfoque pedagógico)."
    )


@app.get("/", summary="Página de bienvenida")
async def inicio():
    return {
        "mensaje": "Bienvenido al Motor GED de Interferencia L1 v2.0",
        "documentacion": "Visita http://127.0.0.1:8000/docs para probar la API"
    }


@app.get("/estado", summary="Estado del servidor y diccionarios")
async def verificar_estado():
    return {
        "estado": "activo",
        "version": "2.0.0",
        "valencias_cargadas": len(VALENCIAS),
        "falsos_cognados_cargados": len(FALSOS_COGNADOS)
    }


@app.post("/analizar", summary="Analizar oración con ponderación de severidad y MCER")
async def analizar_oracion(solicitud: SolicitudAnalisis):
    inicio_tiempo = time.time()
    
    if not solicitud.texto.strip():
        raise HTTPException(status_code=400, detail="El texto proporcionado está vacío.")

    resultado = analizar_valencia_y_orden_oracion(
        texto=solicitud.texto,
        diccionario_valencias=VALENCIAS,
        diccionario_falsos_cognados=FALSOS_COGNADOS,
        nivel_mcer=solicitud.nivel_mcer
    )

    fin_tiempo = time.time()
    tiempo_ms = round((fin_tiempo - inicio_tiempo) * 1000, 2)

    return {
        "tiempo_ejecucion_ms": tiempo_ms,
        "nivel_evaluado": solicitud.nivel_mcer,
        "total_errores": len(resultado["errores"]),
        "indice_severidad_global": resultado["puntaje_severidad_total"],
        "errores_detectados": resultado["errores"]
    }