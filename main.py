from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import URLBase, URLInfo
import validators
import secrets
from models import Url, Base
from database import SessionLocal, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return "Hi, Welcome to shorty that shortens URLs"

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url", response_model=URLInfo)
def create_url(url: URLBase, db:Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message= f"The URL you entered, '{url.target_url}' is not valid")
    
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key ="".join(secrets.choice(chars) for _ in range(8))
    db_url = Url(
        target_url=url.target_url,
        key=key,
        secret_key=secret_key,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url