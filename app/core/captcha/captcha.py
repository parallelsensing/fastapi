from app.core.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from app.models import CaptchaModel,User 
import random
import time

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Captcha:
    def __init__(self,):
        self.db = SessionLocal()
    def __del__(self):
        self.db.close()
    def get_captcha(self,email:str,)->CaptchaModel:
        
        captchaItem = self.db.query(CaptchaModel).filter(CaptchaModel.email == email).first()
        if not captchaItem:
            return None
        return captchaItem
    def generate_captcha(self,email)->CaptchaModel:
        # 检查是否已经存在验证码
        captchaItem = self.get_captcha(email)
        if captchaItem:
            return captchaItem
        # 生成验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        timestamp = int(time.time())
        captcha = CaptchaModel(code=code, email=email)
        self.db.add(captcha)
        self.db.commit()
        self.db.refresh(captcha)
        return captcha
    
    def clear_captcha(self,caseptcha:CaptchaModel):
        self.db.delete(caseptcha)
        self.db.commit()
        self.db.close()
        
    def check_captcha(self, email:str, code:str):
        caseptcha = self.get_captcha(email)
        if caseptcha and caseptcha.code == code:
            self.clear_captcha(caseptcha)
            return True
        return False
    