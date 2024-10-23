import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class DjangoHttpClient:
    djangoHttpxInstance = httpx.AsyncClient(
        base_url=os.getenv("DJANGO_URL"),
        timeout=25000
    )

    @classmethod
    async def post(cls, endpoint: str, data: dict):
        try:
            response = await cls.djangoHttpxInstance.post(endpoint, json=data)

            if response.status_code == 200:
                return True
            else:
                print(f"Failed to send to Django: {response.status_code}")
                return False

        except httpx.RequestError as exc:
            print(f"An error occurred while sending to Django: {str(exc)}")
            return False