import os
from dotenv import load_dotenv

from fastapi import APIRouter
from sqlmodel import Session

from ..database import get_db
from ..auth.views import get_user

load_dotenv()
router = APIRouter(prefix="/admin", tags=["Admin App"])


def make_admin(db: Session, email: str):
    update_user = get_user(db, email)

    update_user.is_superuser = True

    try:
        db.add(update_user)
        db.commit()
        db.refresh(update_user)
    except Exception as e:
        db.rollback()
        print(f"Unable to update admin user, {e}")
db_session = next(get_db()) # next() function is vital because the get_db() use yield, next() can activate yield to continue passing.

make_admin(db_session, email=os.getenv('admin_email'))
