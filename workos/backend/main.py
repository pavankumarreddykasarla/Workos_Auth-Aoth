
# import os
# from dotenv import load_dotenv

# from fastapi import FastAPI, Request, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import RedirectResponse, JSONResponse
# from workos import WorkOSClient

# load_dotenv()

# app = FastAPI()

# FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# workos = WorkOSClient(
#     api_key=os.getenv("WORKOS_API_KEY"),
#     client_id=os.getenv("WORKOS_CLIENT_ID"),
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[FRONTEND_URL],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def home():
#     return {"message": "FastAPI WorkOS backend is running"}


# @app.get("/auth/login")
# def login():
#     authorization_url = workos.user_management.get_authorization_url(
#         provider="authkit",
#         redirect_uri=f"{BACKEND_URL}/auth/callback",
#     )

#     return RedirectResponse(authorization_url)


# @app.get("/auth/callback")
# def callback(code: str):
#     auth_response = workos.user_management.authenticate_with_code(
#         code=code,
#     )

#     response = RedirectResponse(FRONTEND_URL)

#     response.set_cookie(
#         key="access_token",
#         value=auth_response.access_token,
#         httponly=True,
#         secure=False,      # keep False for localhost
#         samesite="lax",
#         path="/",
#     )

#     return response


# def get_current_user(request: Request):
#     token = request.cookies.get("access_token")

#     if not token:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     return {
#         "access_token": token
#     }


# @app.get("/api/me")
# def me(auth=Depends(get_current_user)):
#     return {
#         "message": "User is authenticated",
#         "token_preview": auth["access_token"][:25] + "..."
#     }


# @app.get("/api/admin")
# def admin_only(auth=Depends(get_current_user)):
#     # Basic authorization example
#     # Later you can replace this with WorkOS role/permission checks.
#     return {
#         "message": "Admin API reached",
#         "token_preview": auth["access_token"][:25] + "..."
#     }


# @app.post("/auth/logout")
# def logout():
#     response = JSONResponse({"message": "Logged out"})
#     response.delete_cookie(
#         key="access_token",
#         path="/",
#     )
#     return response
import os
import uuid
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from workos import WorkOSClient

load_dotenv()

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

workos = WorkOSClient(
    api_key=os.getenv("WORKOS_API_KEY"),
    client_id=os.getenv("WORKOS_CLIENT_ID"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary local session store for development
# In production, store this in Redis or database
SESSIONS = {}

# Authorization config
ADMIN_EMAILS = {
    "pavanvicky2015@gmail.com"
}


@app.get("/")
def home():
    return {"message": "FastAPI WorkOS backend is running"}


@app.get("/auth/login")
def login():
    authorization_url = workos.user_management.get_authorization_url(
        provider="authkit",
        redirect_uri=f"{BACKEND_URL}/auth/callback",
    )

    return RedirectResponse(authorization_url)


@app.get("/auth/callback")
def callback(code: str):
    auth_response = workos.user_management.authenticate_with_code(
        code=code,
    )

    user = auth_response.user

    user_email = user.email

    role = "admin" if user_email in ADMIN_EMAILS else "user"

    session_id = str(uuid.uuid4())

    SESSIONS[session_id] = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": role,
        "access_token": auth_response.access_token,
    }

    response = RedirectResponse(FRONTEND_URL)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,      # keep False for localhost
        samesite="lax",
        path="/",
    )

    return response


def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = SESSIONS.get(session_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return user

def require_admin(user=Depends(get_current_user)):
    if user["email"] not in ADMIN_EMAILS:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admin role required."
        )

    return user

def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admin role required."
        )

    return user


@app.get("/api/me")
def me(user=Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "role": user["role"],
    }


@app.get("/api/user-dashboard")
def user_dashboard(user=Depends(get_current_user)):
    return {
        "message": "User dashboard access granted",
        "email": user["email"],
        "role": user["role"],
    }

@app.get("/api/admin")
def admin_only(user=Depends(require_admin)):
    return {
        "message": "Admin access granted",
        "email": user["email"],
        "role": "admin"
    }

@app.post("/auth/logout")
def logout(request: Request):
    session_id = request.cookies.get("session_id")

    if session_id and session_id in SESSIONS:
        del SESSIONS[session_id]

    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie(
        key="session_id",
        path="/",
    )

    return response