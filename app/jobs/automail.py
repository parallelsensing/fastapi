from app.db.session import SessionLocal
from app import crud



async def remind():
  db = SessionLocal()

  # remind reviewer who invited review
 
  db.close()