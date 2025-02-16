import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from empresas.routers import empresas_router, obrigacao_acessoria_router
from shared.database import engine, Base

from empresas.models.empresas_obrigacao_model import Empresa, ObrigacaoAcessoria


#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def teste():
    return JSONResponse(content={"message": "localhost:8001/docs"})

app.include_router(empresas_router.router)
app.include_router(obrigacao_acessoria_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
