from fastapi import FastAPI
from app.routers import api_router

app = FastAPI(title="Table Booking API")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
