import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from empresas.models.empresas_obrigacao_model import Empresa

router = APIRouter(prefix="/empresas_router", tags=["Empresas"])

class EmpresasCadastradasRequest(BaseModel):
    nome:str
    cnpj:str
    endereco:str
    email:str
    telefone:str

    class Config:
        orm_mode = True

class EmpresasCadastradasResponse(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: str
    telefone: str

    class Config:
        orm_mode = True


@router.get("/", response_model=list[EmpresasCadastradasResponse])
def listar_empresas(db: Session = Depends(get_db)) ->List[EmpresasCadastradasResponse]:
    return db.query(Empresa).all()

@router.get("/{id_empresa}", response_model=EmpresasCadastradasResponse)
def listar_empresa(id_empresa: int, db: Session = Depends(get_db)) -> EmpresasCadastradasResponse:

    empresa_cadastrada = db.query(Empresa).get(id_empresa)

    if not empresa_cadastrada:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa com ID {id_empresa} não encontrada."
        )

    return empresa_cadastrada


@router.post("/", response_model=EmpresasCadastradasResponse, status_code=201)
def criar_empresa(
        empresa: EmpresasCadastradasRequest,
        db: Session = Depends(get_db)
    ) -> EmpresasCadastradasResponse:

    if not re.fullmatch(r"\d{14}", empresa.cnpj):
        raise HTTPException(
            status_code=400,
            detail="CNPJ inválido. Deve conter exatamente 14 dígitos numéricos."
        )

    if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", empresa.email):
        raise HTTPException(
            status_code=400,
            detail="E-mail inválido. Deve conter um '@' e um domínio válido (ex: .com, .net)."
        )

    if not re.fullmatch(r"\d{11}", empresa.telefone):
        raise HTTPException(
            status_code=400,
            detail="Telefone inválido. Deve conter 11 dígitos numéricos incluindo o DDD."
        )

    empresa_obj = Empresa(
        nome=empresa.nome,
        cnpj=empresa.cnpj,
        endereco=empresa.endereco,
        email=empresa.email,
        telefone=empresa.telefone
    )

    db.add(empresa_obj)
    db.commit()
    db.refresh(empresa_obj)

    return empresa_obj


@router.put("/{id_empresa}", response_model=EmpresasCadastradasResponse, status_code=200)
def att_empresa(
    id_empresa: int,
    empresa_cadastradas_request: EmpresasCadastradasRequest,
    db: Session = Depends(get_db)
) -> EmpresasCadastradasResponse:

    empresa_cadastradas: Empresa = db.query(Empresa).get(id_empresa)
    if not empresa_cadastradas:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa com ID {id_empresa} não encontrada."
        )

    if not re.fullmatch(r"\d{14}", empresa_cadastradas_request.cnpj):
        raise HTTPException(
            status_code=400,
            detail="CNPJ inválido. Deve conter exatamente 14 dígitos numéricos."
        )

    if not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w+$", empresa_cadastradas_request.email):
        raise HTTPException(
            status_code=400,
            detail="E-mail inválido. Deve conter um '@' e um domínio válido (ex: .com, .net)."
        )

    if not re.fullmatch(r"\d{11}", empresa_cadastradas_request.telefone):
        raise HTTPException(
            status_code=400,
            detail="Telefone inválido. Deve conter 11 dígitos numéricos incluindo o DDD."
        )

    empresa_cadastradas.nome = empresa_cadastradas_request.nome
    empresa_cadastradas.cnpj = empresa_cadastradas_request.cnpj
    empresa_cadastradas.endereco = empresa_cadastradas_request.endereco
    empresa_cadastradas.email = empresa_cadastradas_request.email
    empresa_cadastradas.telefone = empresa_cadastradas_request.telefone

    db.commit()
    db.refresh(empresa_cadastradas)

    return empresa_cadastradas

@router.delete("/{id_empresa}", status_code=204)
def excluir_empresa(id_empresa: int, db: Session = Depends(get_db)) -> None:

    empresa_cadastrada = db.query(Empresa).filter(Empresa.id == id_empresa).first()

    if not empresa_cadastrada:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa com ID {id_empresa} não encontrada."
        )

    try:
        # Exclui a empresa se ela não tiver vinculo com alguma obrigação acessória
        db.delete(empresa_cadastrada)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao excluir empresa. Verifique dependências no banco. Detalhe: {str(e)}"
        )




