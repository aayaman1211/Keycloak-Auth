import os
import requests
from jose import jwt  # from python-jose
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
REALM = os.getenv("REALM", "demo-realm")

app = FastAPI()

# Allow frontend on localhost:3000 to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_scheme = HTTPBearer()


def validate_token(token: str):
    """
    Validate token via Keycloak's userinfo endpoint,
    then decode it (without verifying signature) just to read roles.
    """

    # 1) Ask Keycloak if this token is valid
    userinfo_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"
    resp = requests.get(userinfo_url, headers={"Authorization": f"Bearer {token}"})

    if resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token (userinfo status {resp.status_code})",
        )

    # 2) Decode token only to inspect payload
    try:
        payload = jwt.decode(
            token,
            key="",  # no key because we are disabling signature verification
            options={"verify_signature": False, "verify_aud": False},
            algorithms=["RS256", "HS256"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not decode token: {e}",
        )

    return payload


def require_role(role: str):
    def wrapper(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        token = credentials.credentials
        payload = validate_token(token)
        roles = payload.get("realm_access", {}).get("roles", [])

        if role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required role: {role}",
            )
        return payload

    return wrapper


@app.get("/user-info")
def user_info(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    payload = validate_token(credentials.credentials)
    return {
        "username": payload.get("preferred_username"),
        "roles": payload.get("realm_access", {}).get("roles", []),
    }


@app.get("/admin-only")
def admin_only(payload=Depends(require_role("admin"))):
    return {
        "message": "Hello admin!",
        "username": payload.get("preferred_username"),
        "roles": payload.get("realm_access", {}).get("roles", []),
    }