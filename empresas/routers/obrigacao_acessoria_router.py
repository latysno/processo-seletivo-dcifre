from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from empresas.models.empresas_obrigacao_model import ObrigacaoAcessoria, Empresa

router = APIRouter(prefix="/obrigacao_acessoria_router", tags=["Obrigação Acessória"])


class ObrigacaoAcessoriaRequest(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int

    class Config:
        orm_mode = True


class ObrigacaoAcessoriaResponse(BaseModel):
    nome: str
    periodicidade: str
    empresa_id: int

    class Config:
        orm_mode = True




@router.get("/", response_model=list[ObrigacaoAcessoriaResponse])
def listar_obrigacoes(db: Session = Depends(get_db)) ->List[ObrigacaoAcessoriaResponse]:
    return db.query(ObrigacaoAcessoria).all()

@router.get("/{id_obrigacao_acessoria}", response_model=ObrigacaoAcessoriaResponse)
def listar_empresa(id_obrigacao_acessoria:int,
                    db: Session = Depends(get_db)
                    )->ObrigacaoAcessoriaResponse:
    obrigacao_cadastradas:ObrigacaoAcessoria = db.query(ObrigacaoAcessoria).get(id_obrigacao_acessoria)
    if obrigacao_cadastradas is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada")
    return obrigacao_cadastradas

@router.post("/", response_model=ObrigacaoAcessoriaResponse, status_code=201)
def criar_obrigacao_acessoria(
        obrigacao_acessoria: ObrigacaoAcessoriaRequest,
        db: Session = Depends(get_db)
) -> ObrigacaoAcessoriaResponse:

    empresa = db.query(Empresa).get(obrigacao_acessoria.empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")


    periodicidade = obrigacao_acessoria.periodicidade.lower()
    valid_periodicidades = ["mensal", "trimestral", "anual"]
    if periodicidade not in valid_periodicidades:
        raise HTTPException(
            status_code=404,
            detail="Periodicidade inválida. Utilize 'mensal', 'trimestral' ou 'anual'."
        )


    obrigacao_acessoria_obj = ObrigacaoAcessoria(
        nome=obrigacao_acessoria.nome,
        periodicidade=periodicidade,
        empresa_id=obrigacao_acessoria.empresa_id
    )

    db.add(obrigacao_acessoria_obj)
    db.commit()
    db.refresh(obrigacao_acessoria_obj)
    return obrigacao_acessoria_obj


@router.put("/{id_obrigacao_acessoria}", response_model=ObrigacaoAcessoriaResponse, status_code=200)
def atualizar_obrigacao_acessoria(
    id_obrigacao_acessoria: int,
    obrigacao_acessoria_request: ObrigacaoAcessoriaRequest,
    db: Session = Depends(get_db)
) -> ObrigacaoAcessoriaResponse:


    obrigacao_acessoria_cadastrada = db.query(ObrigacaoAcessoria).get(id_obrigacao_acessoria)
    if not obrigacao_acessoria_cadastrada:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")


    empresa = db.query(Empresa).get(obrigacao_acessoria_request.empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")


    periodicidade = obrigacao_acessoria_request.periodicidade.lower()
    valid_periodicidades = ["mensal", "trimestral", "anual"]
    if periodicidade not in valid_periodicidades:
        raise HTTPException(
            status_code=400,
            detail="Periodicidade inválida. Utilize 'mensal', 'trimestral' ou 'anual'."
        )


    obrigacao_acessoria_cadastrada.nome = obrigacao_acessoria_request.nome
    obrigacao_acessoria_cadastrada.periodicidade = periodicidade
    obrigacao_acessoria_cadastrada.empresa_id = obrigacao_acessoria_request.empresa_id

    db.commit()
    db.refresh(obrigacao_acessoria_cadastrada)

    return obrigacao_acessoria_cadastrada


@router.delete("/{id_obrigacao_acessoria}", status_code=204)
def excluir_obrigacao_acessoria(
        id_obrigacao_acessoria: int,
        db: Session = Depends(get_db)
) -> None:

    obrigacao_acessoria_cadastrada = db.query(ObrigacaoAcessoria).get(id_obrigacao_acessoria)


    if not obrigacao_acessoria_cadastrada:
        raise HTTPException(
            status_code=404,
            detail="Obrigação acessória não encontrada."
        )


    db.delete(obrigacao_acessoria_cadastrada)
    db.commit()
