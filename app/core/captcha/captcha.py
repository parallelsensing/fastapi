from app.core.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from app.models import CaptchaModel,User 
import random
import time
import datetime

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
            # 获取当前 UTC 时间（时区感知的 datetime 对象）
            now = datetime.datetime.now(datetime.timezone.utc)
            print(now)
            # 确保 captchaItem.timestamp 是时区感知的
            if captchaItem.timestamp.tzinfo is None:
                # 如果不是时区感知的，将其设置为 UTC
                captchaItem.timestamp = captchaItem.timestamp.replace(tzinfo=datetime.timezone.utc)
            if (now - captchaItem.timestamp).total_seconds() <= 60: 
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
            # 获取当前 UTC 时间（时区感知的 datetime 对象）
            now = datetime.datetime.now(datetime.timezone.utc)
            if captcha.timestamp.tzinfo is None:
                # 如果不是时区感知的，将其设置为 UTC
                captcha.timestamp = captcha.timestamp.replace(tzinfo=datetime.timezone.utc)
            if (now - captcha.timestamp).total_seconds() <= 60:
                self.clear_captcha(captcha)
                return True
        return False
    