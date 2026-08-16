from fastapi import FastAPI


app = FastAPI()


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.get("/")
def welcome_route():
    return {"message": "welcome"}
