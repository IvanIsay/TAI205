
#1. importaciones
from fastapi import FastAPI,status, HTTPException
from typing import Optional
import asyncio


#******************
#2.Inicializacion APP
#******************

app= FastAPI(
    title=' MI Primer API',
    description="Ivan Isay Guerra L",
    version='1.0.0'
    )

#******************
# BD ficticia
#******************

usuarios=[
    {"id":"1","nombre":"Ivan","edad":38},
    {"id":"2","nombre":"Diana","edad":20},
    {"id":"3","nombre":"Julian","edad":20},
]



     
#******************
#  Usuario CRUD
#******************

@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def leer_usuarios( ):
    return{
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
    }
    
@app.post("/v1/usuarios/",tags=['CRUD HTTP'] ,status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }
    

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"],status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario_actualizado: dict):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            # Reemplazamos completamente el usuario
            usuarios[index] = usuario_actualizado

            return {
                "message": "Usuario actualizado completamente",
                "data": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
@app.patch("/v1/usuarios/{id}", tags=["CRUD HTTP"],status_code=status.HTTP_200_OK)
async def actualizar_parcial(id: int, datos: dict):

    for usr in usuarios:
        if usr["id"] == id:

            # Actualización parcial
            usr.update(datos)

            return {
                "message": "Usuario actualizado parcialmente",
                "data": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"],status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            usuarios.pop(index)

            return {
                "message": "Usuario eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
    
#******************
# Otros Endpoints
#******************
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3) #simulacion peticion,consultaBD..
    return {
            "Calificacion":"7.5",
            "estatus":"200"
            }  
    
@app.get("/v1/parametroO/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado":"usuario encontrado",
        "Estatus":"200",
        }
    
    
    
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            ) 
    usuarios.append(usuario)
    return{
        "mensaje": "usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
    }