from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.sensor import router as sensor_router
from routes.disease import router as disease_router

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Route registration
app.include_router(sensor_router)
app.include_router(disease_router)

@app.get("/")
def root():
    return {"status": "Backend running"}
