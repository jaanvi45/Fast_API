from fastapi import FastAPI 
from fastapi import APIRouter,Depends,status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database,models
from ..hashing import Hash
from ..token import create_access_token


router = APIRouter(
    tags = ["Authentication"]
)


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    
    
    access_token = create_access_token(data={"sub": user.email})
    return access_token(access_token=access_token, token_type="bearer")

@router.post("/reset-password")
def reset_password(email: str, new_password: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    hashed_password = Hash.bcrypt(new_password)
    user.password = hashed_password
    db.commit()

    return {"message": "Password has been reset successfully"}
