import httpx

from app.core.config import settings


class UnclothyService:
    API_KEY = settings.API_KEY
    WEBHOOK_URL = f"{settings.SERVER_ADDRESS}:{settings.SERVER_PORT}/unclothy/webhook"
    BASE_URL = "https://unclothy.com/api/v2"

    @classmethod
    async def create_task(cls, image: str, webhook_url: str = None):
        payload = {
          "base64": image,
          "webhook_url": webhook_url if webhook_url else cls.WEBHOOK_URL,
          "settings": {
            "generationMode": "naked",
            "gender": "female",
            "age": "automatic",
            "bodyType": "skinny",
            "breastsSize": "medium",
            "assSize": "medium",
            "pussy": "shaved",
          }
        }

        headers = {
            "x-api-key": cls.API_KEY,
            "Content-Type": "application/json"
        }

        with httpx.AsyncClient as client:
            response = await client.post(
                url=f"{cls.BASE_URL}/create",
                headers=headers,
                json=payload,
            )

            if response.status_code == 200:
                return response.json()


    @classmethod
    async def get_task(cls, task_id: str):
        headers = {
            "x-api-key": cls.API_KEY,
            "Content-Type": "application/json"
        }

        with httpx.AsyncClient as client:
            response = await client.get(url=f"{cls.BASE_URL}/task/{task_id}")

            if response.status_code == 200:
                return response.json()

    @classmethod
    async def get_credits(cls):
        headers = {
            "x-api-key": cls.API_KEY,
            "Content-Type": "application/json"
        }

        with httpx.AsyncClient as client:
            response = await client.get(url=f"{cls.BASE_URL}/user/credits")

            if response.status_code == 200:
                return response.json()
