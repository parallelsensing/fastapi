import hashlib
import os


def hash_password(password: str) -> str:
    # 生成盐
    salt = os.urandom(16)  # 生成16字节的盐
    # 使用 md5 哈希密码和盐
    hashed_password = hashlib.md5(salt + password.encode('utf-8')).hexdigest()
    # 将盐和哈希值组合在一起存储（盐的十六进制表示）
    return salt.hex() + ":" + hashed_password

def verify_password(stored_password: str, provided_password: str) -> bool:
    salt, hashed_password = stored_password.split(":")
    salt = bytes.fromhex(salt)  # 将盐转换回字节
    # 使用相同的算法和盐哈希提供的密码
    hashed_provided_password = hashlib.md5(salt + provided_password.encode('utf-8')).hexdigest()
    # 比较哈希值
    return hashed_password == hashed_provided_password
