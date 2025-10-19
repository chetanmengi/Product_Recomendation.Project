
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.recommend import router as recommend_router
import os

app = FastAPI(title='Product Reco App')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router, prefix='/api')

# mount static folder to serve built React app if placed in backend/static
static_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend_build')
if os.path.exists(static_dir):
    app.mount('/', StaticFiles(directory=static_dir, html=True), name='static')

@app.get('/health')
def health():
    return {'status': 'ok'}
