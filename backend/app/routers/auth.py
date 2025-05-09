from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import verify_password, create_access_token
from app.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.dni == form_data.username).first()
    if not user or not verify_password(form_data.password, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": user.dni})
    return {"access_token": access_token, "token_type": "bearer"}

