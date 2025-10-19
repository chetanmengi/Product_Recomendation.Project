
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.recommender import Recommender\nfrom app.genai.generator import generate_description

router = APIRouter()

class Query(BaseModel):
    query: str
    k: int = 5

# instantiate recommender (loads dataset once)
reco = Recommender()

@router.post('/query')
def query(q: Query):
    results = reco.recommend(q.query, k=q.k)
    return {"query": q.query, "results": results}

@router.get('/analytics/summary')
def analytics_summary():
    return reco.analytics_summary()


@router.post('/generate')
def generate(payload: Query):
    # generate descriptions for top-k recommendations (uses template generator)
    items = reco.query({'query': payload.query, 'k': payload.k})
    results = []
    for it in items:
        desc = generate_description(it.get('title',''), it.get('brand',''), it.get('material',''), it.get('color',''), it.get('category',''))
        results.append({**it, 'generated_description': desc})
    return {'results': results}
