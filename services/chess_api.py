from httpx import AsyncClient
from os import getenv

BASE_URL = getenv("CHESS_API_URL")

async def create_user(tg_id: str) -> dict | None:
    print(f"create_user, {tg_id}")
    async with AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/users/",
            json={
                "tg_id": tg_id
            },
            timeout=5
        )

    print(response.status_code)
    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def create_game(tg_id: str) -> dict | None:
    print(f"create_game, {tg_id}")
    async with AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/games/",
            json={
                "tg_id": tg_id
            },
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def get_user(tg_id: str) -> dict | None:
    print(f"get_user, {tg_id}")
    async with AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/users/{tg_id}",
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def get_user_active_game(tg_id: str) -> dict | None:
    print(f"get_user_active_game, {tg_id}")
    async with AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/users/{tg_id}/active",
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def get_user_games(tg_id: str) -> dict | None:
    print(f"get_user, {tg_id}")
    async with AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/users/{tg_id}/games",
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def game_move(tg_id: str, move: str) -> dict | None:
    print(f"move, {tg_id}")
    async with AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/games/move",
            json={
                "tg_id": tg_id,
                "move": move
            },
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def game_move_bot(tg_id: str) -> dict | None:
    print(f"move_bot, {tg_id}")
    async with AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/games/move_bot",
            json={
                "tg_id": tg_id
            },
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()

async def surrender(tg_id: str) -> dict | None:
    print(f"surrender, {tg_id}")
    async with AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/games/surrender",
            json={
                "tg_id": tg_id
            },
            timeout=5
        )

    if response.status_code not in (200, 201):
        return None

    print(response.json())
    return response.json()