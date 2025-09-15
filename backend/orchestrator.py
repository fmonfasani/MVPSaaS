# orchestrator.py
import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: List[dict]
    task: str
    result: str
    error: str

# ---- LLMs: opción A: modelo local via HF InferenceClient local (en el mismo Space)
from huggingface_hub import InferenceClient
import os
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", None)
# modelo liviano (ej: distilgpt2). Cambiá por otro que prefieras.
LOCAL_MODEL_ID = os.getenv("LOCAL_MODEL_ID", "distilgpt2")
client = InferenceClient(model=LOCAL_MODEL_ID, token=HF_TOKEN)

def research(state: AgentState) -> AgentState:
    try:
        prompt = f"""Genera un JSON compacto para una landing del rubro: "{state['task']}".
Campos: title, subtitle, sections[{{title,body}}], cta{{text,url}}. SOLO JSON."""
        txt = client.text_generation(prompt, max_new_tokens=320)
        state["messages"].append({"role":"research","content":txt})
        return state
    except Exception as e:
        state["error"] = str(e); return state

def writer(state: AgentState) -> AgentState:
    try:
        raw = state["messages"][-1]["content"]
        # recorte ingenuo a JSON
        start, end = raw.find("{"), raw.rfind("}")
        parsed = json.loads(raw[start:end+1]) if start!=-1 and end!=-1 else {"title":"Draft","subtitle":"","sections":[],"cta":{"text":"Contactar","url":"/"}}
        state["result"] = json.dumps(parsed, ensure_ascii=False)
        return state
    except Exception as e:
        state["error"] = str(e); return state

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("research", research)
    g.add_node("writer", writer)
    g.set_entry_point("research")
    g.add_edge("research","writer")
    g.add_edge("writer", END)
    return g.compile()

def run_agent(task: str) -> dict:
    flow = build_graph()
    out = flow.invoke(AgentState(messages=[], task=task, result="", error=""))
    return {
        "success": not bool(out["error"]),
        "result": out.get("result",""),
        "error": out.get("error",""),
        "messages": out.get("messages",[])
    }
