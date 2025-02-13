from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/empresas_router")

class EmpresasCadastradasRequest(BaseModel):
    nome:str
    cnpj:str
    endereco:str
    email:str
    telefone:str

class EmpresasCadastradasResponse(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str


@router.get("/", response_model=list[EmpresasCadastradasResponse])
async def listar_empresas():
    return[
        EmpresasCadastradasResponse(
            nome='teste',
            cnpj='13213123',
            endereco='asdasdasd',
            email='abc@email.com',
            telefone='899163899'
        )
    ]

@router.post("/", response_model=EmpresasCadastradasResponse, status_code=201)
def criar_empresa(empresa: EmpresasCadastradasRequest):
    return EmpresasCadastradasResponse(
    nome=empresa.nome,
    cnpj = empresa.cnpf,
    endereco = empresa.endereco,
    email = empresa.email,
    telefone = empresa.telefone
    )

