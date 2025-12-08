##
## EPITECH PROJECT, 2025
## AREA
## File description:
## test
##

import unittest
from fastapi.testclient import TestClient
from backend.main import app, GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
import httpx

client = TestClient(app)

class TestGoogleLog(unittest.TestCase):
    def test_google_login(self):
        response = client.get("/auth/google/login")

        self.assertEqual(response.status_code, 307)
        location = response.headers["location"]

        self.assertIn(GOOGLE_AUTH_URL, location)
        self.assertIn(f"client_id={GOOGLE_CLIENT_ID}", location)
        self.assertIn(f"client_id={GOOGLE_REDIRECT_URI}", location)

class MockGoogle:

    async def post(self, *args, **kwargs):
        return httpx.Response(
            status_code=200,
            json={"access_token": "fake-access-token"}
        )


    async def get(self, *args, **kwargs):
        return httpx.Response(
            status_code=200,
            json={
                "id": "12345",
                "email": "test@area.com",
                "name": "Charles Leclerc"
            }
        )

    async def _aenter_(self):
        return self

    async def _aexit_(self, exc_type, exc, traceback):
        pass


class TestGoogleCallback(unittest.TestCase):
    def test_google_callback(self):
        response = client.get("/auth/google/callback?code=fake-code")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(["message"], "Google login success!")
        self.assertEqual(data["google_user"]["email"], "test@area.com")
        self.assertEqual(["tokens"]["access_token"], "fake-access-token")