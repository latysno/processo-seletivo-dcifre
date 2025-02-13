import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from empresas.routers import empresas_router

app = FastAPI()

@app.get("/")
def teste():
    return JSONResponse(content={"message": "teste"})

app.include_router(empresas_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
