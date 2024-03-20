import uvicorn

if __name__ == "__main__":
  config = uvicorn.Config("app.main:app", host="0.0.0.0", port=9711)
  server = uvicorn.Server(config)
  server.run()