from typing import List
from fastapi import APIRouter, Depends, Path, HTTPException, Request
import requests

from app.core.jwt import get_current_user_authorizer
from app.models.user import User

router = APIRouter()

@router.get("/docker-hub/images",
    response_model=List[str],
    tags=["Docker Hub"]
)
def get_images(
    q: str,
    user: User = Depends(get_current_user_authorizer()),
):
    response = []

    content = _fetch(f'https://hub.docker.com/api/content/v1/products/search?page_size=10&q={q}')
    if(content['summaries']):
        response.extend([summaries['name'] for summaries in content['summaries']])

    content = _fetch(f'https://hub.docker.com/api/content/v1/products/search?page_size=10&source=community&q={q}')
    if(content['summaries']):
        response.extend([summary['name'] for summary in content['summaries']]) 
    
    return response

@router.get("/docker-hub/tags",
    response_model=List[str],
    tags=["Docker Hub"]
)
def get_images(
    q: str,
    user: User = Depends(get_current_user_authorizer()),
):
    if(len(q.split('/')) == 1):
        q = f'library/{q}'

    content = _fetch(f'https://hub.docker.com/v2/repositories/{q}/tags/?page_size=25&ordering=last_updated')
    
    return [result['name'] for result in content['results']]

def _fetch(url):
    result = requests.get(url)
    status_code = result.status_code
    content = result.json()

    if(status_code >= 300):
        raise HTTPException(status_code=status_code, detail=content)

    return content
