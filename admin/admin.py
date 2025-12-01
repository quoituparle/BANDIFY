from starlette_admin.auth import AuthProvider, AdminConfig, AdminUser
from starlette.responses import RedirectResponse
from sqlmodel import Session, select
from starlette.requests import Request
from starlette.responses import Response


from ..database import engine 
from ..models import User
from ..auth.views import verify_password  

class AdminAuthProvider(AuthProvider):
    async def login(self, username: str, password: str, remember_me: any, request: Request, response: Response) -> Response:
        with Session(engine) as session:
            statement = select(User).where(User.email == username)
            user = session.exec(statement).first()

            if (user 
                and verify_password(password, user.hashed_password) 
                and user.is_superuser 
                and user.is_verified):
                
                request.session["user_id"] = str(user.id)
                request.session["user_email"] = user.email
                return RedirectResponse(url="/admin/user/list", status_code=302)


        return False

    async def is_authenticated(self, request) -> bool:
        return request.session.get("user_id") is not None

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return RedirectResponse(url="/admin")

    def get_admin_user(self, request: Request) -> AdminUser:
        user_email = request.session.get("user_email")
        if user_email:
            return AdminUser(username=user_email)
        return None