from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (rutas_rol, rutas_auth, rutas_sede, rutas_salon,
                     rutas_usuario, rutas_alerta, rutas_dispositivo,
                     rutas_sensor, rutas_umbral, rutas_lectura)
app = FastAPI(
    title="API de Calidad del Aire en Espacios Cerrados",
    description="Backend modular con FastAPI y PostgreSQL puro",
    version="1.0.0"
)

# Permite que el frontend (Svelte) llame a la API desde otro puerto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rutas_rol.router)
app.include_router(rutas_auth.router)
app.include_router(rutas_sede.router)
app.include_router(rutas_salon.router)
app.include_router(rutas_usuario.router)
app.include_router(rutas_alerta.router)
app.include_router(rutas_dispositivo.router)
app.include_router(rutas_sensor.router)
app.include_router(rutas_umbral.router)
app.include_router(rutas_lectura.router)




@app.get("/")
def estado_api():
    return {"mensaje": "La API se encuentra en línea y funcional"}