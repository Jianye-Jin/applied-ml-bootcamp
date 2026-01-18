from fastapi import FastAPI

app = FastAPI(title="applied-ml-bootcamp")

@app.get("/health")
def health():
    return {"ok": True}
