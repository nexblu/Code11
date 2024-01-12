from fastapi import APIRouter
from models.user import Register
from config.db import db
from fastapi.responses import JSONResponse
import requests


router = APIRouter()


@router.get("/email_validator/{email}")
async def email_validator(email: str):
    url = "https://community-neutrino-email-validate.p.rapidapi.com/email-validate"

    payload = {"email": email}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "24ed65ae48msha241654d8bc9256p17cb04jsn525ebae94435",
        "X-RapidAPI-Host": "community-neutrino-email-validate.p.rapidapi.com",
    }

    response = (requests.post(url, data=payload, headers=headers)).json()
    if response["valid"]:
        return JSONResponse(
            content=[
                {
                    "code11": {
                        "result": {
                            "email": email,
                            "provider": response["provider"],
                            "valid": response["valid"],
                        },
                        "status": "email valid",
                        "status_code": 200,
                    }
                }
            ],
            status_code=200,
        )
    return JSONResponse(
        content=[
            {
                "code11": {
                    "result": {
                        "email": email,
                        "provider": response["provider"],
                        "valid": response["valid"],
                    },
                    "status": "email not valid",
                    "status_code": 404,
                }
            }
        ],
        status_code=404,
    )


@router.get("/login/{username}/{password}")
async def login(username: str, password: str):
    if data := await db.get("username", username, password):
        return JSONResponse(
            content=[
                {
                    "code11": {
                        "result": {
                            "username": username,
                            "email": data["email"],
                            "password": password,
                        },
                        "status": "berhasil login",
                        "status_code": 200,
                    }
                }
            ],
            status_code=200,
        )
    return JSONResponse(
        content=[
            {
                "code11": {
                    "status": "failed login",
                    "status_code": 404,
                }
            }
        ],
        status_code=404,
    )


@router.post("/register")
async def register(user: Register):
    if not (
        data := await db.get("email", user.username, user.password, email=user.email)
    ):
        await db.insert(user.username, user.password, user.email)
        return JSONResponse(
            content=[
                {
                    "code11": {
                        "result": {
                            "username": user.username,
                            "email": user.email,
                            "password": user.password,
                        },
                        "status": "berhasil register",
                        "status_code": 200,
                    }
                }
            ],
            status_code=200,
        )
    return JSONResponse(
        content=[
            {
                "code11": {
                    "status": "failed register",
                    "status_code": 400,
                }
            }
        ],
        status_code=400,
    )
