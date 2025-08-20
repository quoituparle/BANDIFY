from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from ..database import get_db, create_db_and_tables
from .. import models
from ..auth.views import get_current_user
from models import User


load_dotenv()
FastAPI()

class modelSetting(BaseModel):
    model: str
    test: str
    inputText: str | None
    score: float | None

router = APIRouter(prefix="/main", tags=["Main App"])

@router.get('/me')
async def read_users(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "full_name": current_user.full_name, "id": current_user.id}

