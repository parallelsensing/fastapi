import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request
from .config import settings

# 密钥应该保密，只在服务器上知道
SECRET_KEY = settings.SECRET_KEY


def create_token(username: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data = f"{username}:{timestamp}"
    token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()
    return f"{username}:{timestamp}%{token}"  # 包含用户名、时间戳和 token

def verify_token(token: str) -> str:
    try:
        username, timestamp_token = token.split(':')
        timestamp, user_token = timestamp_token.split('%')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    current_timestamp = datetime.utcnow()
    token_gen_time = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
    if (current_timestamp - token_gen_time) > timedelta(hours=1):
        raise HTTPException(status_code=401, detail="Token expired")

    data = f"{username}:{timestamp}"
    expected_token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()

    if user_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    return username

def get_current_user(request: Request) -> str:
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(status_code=401, detail="非法操作")

    token = token.replace("Bearer ", "")  # 移除 "Bearer " 前缀
    return verify_token(token)