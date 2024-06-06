import hashlib
import secrets
from datetime import datetime, timedelta

# 密钥应该保密，只在服务器上知道
SECRET_KEY = secrets.token_hex(16)

def create_token(username):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data = f"{username}:{timestamp}"
    token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()
    return f"{username}:{token}"  # 包含用户名和 token

def verify_token(username, token):
    # 提取时间戳
    current_timestamp = datetime.utcnow()
    token_gen_time = datetime.strptime(token[-14:], "%Y%m%d%H%M%S")
    if (current_timestamp - token_gen_time) > timedelta(hours=1):
        return False  # Token 已过期

    # 重新计算哈希值
    data = f"{username}:{token[-14:]}"
    expected_token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()
    return token == expected_token

def get_current_user(token: str):
    try:
        username, user_token = token.split('%')  # 尝试解析用户名和 token
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    # 重新构建用于验证的 token
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data = f"{username}:{timestamp}"
    expected_token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()

    if user_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return username