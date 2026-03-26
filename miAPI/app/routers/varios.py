#******************    
# otros Endpoints
#******************

import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(tags=['Inicio'])

@routerV.get("/")
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"}

@routerV.get("/holaMundo")
async def Hola():
    await asyncio.sleep(5) #peticion,consultaBD,Archivo
    return {
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }
            
@routerV.get("/v1/ParametroOb/{id}")
async def consultauno(id:int):
    return {"mensaje":"usuario encontrado",
            "usuario":id,
            "status":"200" }
    
@routerV.get("/v1/ParametroOp/")
async def consultatodos(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"mensaje":"usuario encontrado","usuario":usuarioK}
        return{"mensaje":"usuario no encontrado","status":"200"}   
    else:
        return {"mensaje":"No se proporciono id","status":"200"} 
    