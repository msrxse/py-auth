from fastapi import FastAPI

app = FastAPI(title="py-auth")


@app.get("/health")
async def health():
    return {"status": "ok"}
