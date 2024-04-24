import hashlib
import secrets
from datetime import datetime, timedelta

# 密钥应该保密，只在服务器上知道
SECRET_KEY = secrets.token_hex(16)

def create_token(username):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    data = f"{username}:{timestamp}"
    token = hashlib.sha256(f"{data}{SECRET_KEY}".encode()).hexdigest()
    return token

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
