#importaciones
from fastapi import FastAPI
from app.routers import usuarios,varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

#Instancia del servidor
app= FastAPI(
    title="Mi Primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
