#importaciones
from fastapi import FastAPI, status, HTTPException,Depends
import asyncio
from typing import Optional
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#******************
#Instancia del servidor
#******************

app= FastAPI(
    title="Mi Primer API",
    description="Ivan Isay Guerra L",
    version="1.0"
)


#******************
#TB ficticia
#******************

usuarios=[
    {"id":1,"nombre":"Diego","edad":21},
    {"id":2,"nombre":"Coral","edad":21},
    {"id":3,"nombre":"Saul","edad":21},
]

#******************
#Modelo Pydantic de validacion
#******************

class crear_usuario(BaseModel):
    id: int= Field(...,gt=0,description= "identificador de usuario")
    nombre:str= Field(...,min_length= 3, max_length= 50, example="Juanito Doe")
    edad:int = Field(..., ge=1, le=125,description="Edad validad entre 1 y 125" )   


#******************
#Seguridad con HTTP BASIC
#******************

security= HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuarioAut= secrets.compare_digest(credenciales.username,"ivanisay")
    contraAuth= secrets.compare_digest(credenciales.password,"123456")
    
    if not(usuarioAut and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail=" Credenciales no autorizadas"
        )
        
    return credenciales.username  


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
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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
async def eliminar_usuario(id: int,usuarioAuth:str=Depends(verificar_peticion)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:

            usuarios.pop(index)

            return {
                "message": f"Usuario eliminado por {usuarioAuth}"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
    
#******************    
# otros Endpoints
#******************
@app.get("/",tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"}

@app.get("/holaMundo",tags=['Asincronia'])
async def Hola():
    await asyncio.sleep(5) #peticion,consultaBD,Archivo
    return {
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }
            
@app.get("/v1/ParametroOb/{id}",tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje":"usuario encontrado",
            "usuario":id,
            "status":"200" }
    
@app.get("/v1/ParametroOp/",tags=['Parametro Opcional'])
async def consultatodos(id:Optional[int]=None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"mensaje":"usuario encontrado","usuario":usuarioK}
        return{"mensaje":"usuario no encontrado","status":"200"}   
    else:
        return {"mensaje":"No se proporciono id","status":"200"} 
    