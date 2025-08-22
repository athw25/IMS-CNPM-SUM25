import uvicorn
from fastapi import FastAPI
from recruitment_controller import router as recruitment_router

app = FastAPI()
app.include_router(recruitment_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
