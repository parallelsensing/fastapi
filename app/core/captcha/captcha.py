from app.core.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from app.models import CaptchaModel,User 
import random
import time

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
            if int(time.time())-captchaItem.timestamp<=300:
                return None
            else:
                self.db.delete(captchaItem)
                self.db.commit()
            # return captchaItem
        # 生成验证码
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # timestamp = int(time.time())
        captcha = CaptchaModel(code=code, email=email)
        self.db.add(captcha)
        self.db.commit()
        self.db.refresh(captcha)
        return captcha
    
    def clear_captcha(self,caseptcha:CaptchaModel):
        self.db.delete(caseptcha)
        self.db.commit()
        self.db.close()
        
    def check_captcha(self, email: str, code: str) -> bool:
        captcha = self.get_captcha(email)
        if captcha and captcha.code == code:
            # 检查有效期
            current_time = int(time.time())
            if current_time - captcha.timestamp <= 300:  # 5分钟有效期
                self.clear_captcha(captcha)
                return True
        return False
    