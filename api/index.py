import json
import hmac
import hashlib
from urllib.parse import parse_qsl
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AbboudBots API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = "9000615254:AAE5cRL9Cnt_kLIQVaAlDYRirCsb9S49C7A"

def verify_telegram_init_data(init_data: str, bot_token: str) -> dict | None:
    try:
        parsed_data = dict(parse_qsl(init_data))
        if "hash" not in parsed_data:
            return None
            
        received_hash = parsed_data.pop("hash")
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items()))
        
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if calculated_hash == received_hash:
            if "user" in parsed_data:
                parsed_data["user"] = json.loads(parsed_data["user"])
            return parsed_data
        return None
    except Exception:
        return None

@app.get("/api/trpc/telegram.getUser")
async def get_user(x_telegram_init_data: str = Header(None)):
    if not x_telegram_init_data:
        raise HTTPException(status_code=401, detail={"message": "UNAUTHORIZED", "code": -32001})
        
    auth_result = verify_telegram_init_data(x_telegram_init_data, BOT_TOKEN)
    if not auth_result:
        raise HTTPException(status_code=401, detail={"message": "UNAUTHORIZED", "code": -32001})

    return [{
        "result": {
            "data": {
                "json": {
                    "user": auth_result.get("user", {}),
                    "status": "active"
                }
            }
        }
    }]

@app.get("/api/trpc/telegram.getIggs")
async def get_iggs(x_telegram_init_data: str = Header(None)):
    if not x_telegram_init_data:
        raise HTTPException(status_code=401, detail={"message": "UNAUTHORIZED", "code": -32001})

    auth_result = verify_telegram_init_data(x_telegram_init_data, BOT_TOKEN)
    if not auth_result:
        raise HTTPException(status_code=401, detail={"message": "UNAUTHORIZED", "code": -32001})

    return [{
        "result": {
            "data": {
                "json": {
                    "accounts": [
                        {"igg_id": "100200300", "castle_level": 25, "server": 12},
                        {"igg_id": "400500600", "castle_level": 20, "server": 15}
                    ]
                }
            }
        }
    }]
