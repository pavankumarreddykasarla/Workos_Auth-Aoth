# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request, Response, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import RedirectResponse, JSONResponse
# from workos import WorkOSClient

# load_dotenv()
# app = FastAPI()

# FRONTEND_URL = os.getenv("FRONTEND_URL")
# BACKEND_URL = os.getenv("BACKEND_URL")
# COOKIE_PASSWORD = os.getenv("WORKOS_COOKIE_PASSWORD")

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


# @app.get("/auth/login")
# def login():
#     authorization_url = workos.user_management.get_authorization_url(
#         provider="authkit",
#         redirect_uri=f"{BACKEND_URL}/auth/callback",
#     )
#     return RedirectResponse(authorization_url)


# # @app.get("/auth/callback")
# # def callback(code: str):
# #     auth_response = workos.user_management.authenticate_with_code(
# #         code=code,
# #         session={
# #             "seal_session": True,
# #             "cookie_password": COOKIE_PASSWORD,
# #         },
# #     )

# #     response = RedirectResponse(FRONTEND_URL)
# #     response.set_cookie(
# #         key="wos_session",
# #         value=auth_response.sealed_session,
# #         httponly=True,
# #         secure=False,  # True in production with HTTPS
# #         samesite="lax",
# #     )
# #     return response

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
#         secure=False,
#         samesite="lax",
#     )

#     return response

# def get_current_user(request: Request):
#     sealed_session = request.cookies.get("wos_session")

#     if not sealed_session:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     session = workos.user_management.load_sealed_session(
#         sealed_session=sealed_session,
#         cookie_password=COOKIE_PASSWORD,
#     )

#     auth_response = session.authenticate()

#     if not auth_response.authenticated:
#         raise HTTPException(status_code=401, detail="Session expired")

#     return auth_response.user


# @app.get("/api/me")
# def me(user=Depends(get_current_user)):
#     return {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#     }


# @app.get("/api/admin")
# def admin_only(user=Depends(get_current_user)):
#     # Simple authorization example
#     allowed_admins = ["your_email@gmail.com"]

#     if user.email not in allowed_admins:
#         raise HTTPException(status_code=403, detail="Access denied")

#     return {"message": "Welcome admin"}


# @app.post("/auth/logout")
# def logout(request: Request):
#     sealed_session = request.cookies.get("wos_session")

#     if not sealed_session:
#         response = JSONResponse({"message": "Logged out"})
#         response.delete_cookie("wos_session")
#         return response

#     session = workos.user_management.load_sealed_session(
#         sealed_session=sealed_session,
#         cookie_password=COOKIE_PASSWORD,
#     )

#     logout_url = session.get_logout_url()

#     response = RedirectResponse(logout_url)
#     response.delete_cookie("wos_session")
#     return response
import os
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

    response = RedirectResponse(FRONTEND_URL)

    response.set_cookie(
        key="access_token",
        value=auth_response.access_token,
        httponly=True,
        secure=False,      # keep False for localhost
        samesite="lax",
        path="/",
    )

    return response


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "access_token": token
    }


@app.get("/api/me")
def me(auth=Depends(get_current_user)):
    return {
        "message": "User is authenticated",
        "token_preview": auth["access_token"][:25] + "..."
    }


@app.get("/api/admin")
def admin_only(auth=Depends(get_current_user)):
    # Basic authorization example
    # Later you can replace this with WorkOS role/permission checks.
    return {
        "message": "Admin API reached",
        "token_preview": auth["access_token"][:25] + "..."
    }


@app.post("/auth/logout")
def logout():
    response = JSONResponse({"message": "Logged out"})
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return response