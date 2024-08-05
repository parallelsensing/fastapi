import os
import uuid

def generate_unique_filename(original_filename):
    # 获取文件扩展名
    extension = os.path.splitext(original_filename)[1]
    # 生成唯一的UUID
    unique_id = uuid.uuid4()
    # 组合唯一标识符和扩展名
    unique_filename = f"{unique_id}{extension}"
    return unique_filename

