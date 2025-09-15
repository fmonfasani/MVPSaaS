# app.py
import os, json
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from orchestrator import run_agent

APP = FastAPI()
APP.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

@APP.get("/health")
def health(): return {"ok": True}

async def verify_supabase_user(token: str):
    # valida el JWT preguntándole a Supabase
    headers = {"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=10) as cx:
        r = await cx.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Auth failed")
    return r.json()

@APP.post("/agent-process")
async def agent_process(req: Request):
    body = await req.json()
    auth = req.headers.get("authorization","")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth.split(" ",1)[1]

    user = await verify_supabase_user(token)
    task = body.get("message","").strip()
    conv_id = body.get("conversationId")

    if not task or not conv_id:
        raise HTTPException(status_code=400, detail="Bad input")

    result = run_agent(task)

    # guardar respuesta en Supabase
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    payload = {
        "conversation_id": conv_id,
        "role": "assistant",
        "content": result.get("result","")
    }
    async with httpx.AsyncClient(timeout=10) as cx:
        r = await cx.post(f"{SUPABASE_URL}/rest/v1/messages", headers=headers, data=json.dumps(payload))
    # ignoramos fallo de log si solo querés responder
    return result
