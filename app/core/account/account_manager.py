import hashlib
import secrets
from datetime import datetime, timedelta
import datetime as dt
from fastapi import FastAPI, Depends, HTTPException, status, Request
from ..config import settings
from app.core.security import hash_password,verify_password
from app.core.database import SessionLocal
from app.models import User as UserModel
from app.models import CaptchaModel
# 密钥应该保密，只在服务器上知道
SECRET_KEY = settings.SECRET_KEY


class AccountManager:
    
    def __init__(self):
        # self.account_id = account_id
        self.db = SessionLocal()
        
    def get_reset_password_token(self,email):
        captcha = self.db.query(CaptchaModel).filter(CaptchaModel.email==email).first()
        if not captcha:
            return None
        return captcha
            
    
    def create_reset_password_token(self,email):
        
        captcha = self.db.query(CaptchaModel).filter(CaptchaModel.email==email).first()
        if captcha:
            # 获取当前 UTC 时间（时区感知的 datetime 对象）
            now = dt.datetime.now(dt.timezone.utc)
            print(now)
            # 确保 captchaItem.timestamp 是时区感知的
            if captcha.timestamp.tzinfo is None:
                # 如果不是时区感知的，将其设置为 UTC
                captcha.timestamp = captcha.timestamp.replace(tzinfo=dt.timezone.utc)
            if (now - captcha.timestamp).total_seconds() <= 300: 
                return None
            else:
                self.db.delete(captcha)
                self.db.commit()
        
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        data = f"{email}${timestamp}"
        token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()
        result = f"{email}${timestamp}&{token}" 
        
        captcha = CaptchaModel(code=result,email=email)
        
        return captcha  
    def clear_token(self,castcha:CaptchaModel):
        self.db.delete(castcha)
        self.db.commit()
        
    
    def verify_reset_password_token(self,token: str) -> str:
        try:
            email, timestamp_token = token.split('$')
            timestamp, user_token = timestamp_token.split('&')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid token format")

        current_timestamp = datetime.utcnow()
        token_gen_time = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        if (current_timestamp - token_gen_time) > timedelta(minutes=1):
            raise HTTPException(status_code=401, detail="Token expired")

        data = f"{email}${timestamp}"
        expected_token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()

        if user_token != expected_token:
            raise HTTPException(status_code=401, detail="Invalid token")

        return email
    
    def reset_password(self,email, new_password):
        db=SessionLocal()
        
        hashed_password = hash_password(new_password)
        user = db.query(UserModel).filter(UserModel.email == email).first()
        
        if not user:
            return 404
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        db.close()
        
        return 200
    