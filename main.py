import uvicorn
from app.core.database import Base, engine
from app.models import Item as ItemModel
from app.models import User as UserModel


if __name__ == "__main__":
  Base.metadata.create_all(bind=engine)
  config = uvicorn.Config("app.main:app", host="0.0.0.0", port=9711)
  server = uvicorn.Server(config)
  server.run()