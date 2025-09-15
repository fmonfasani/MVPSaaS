import os, json
from typing import TypedDict, List
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from huggingface_hub import InferenceClient

class AgentState(TypedDict):
    messages: List[dict]
    task: str
    result: str
    error: str

groq = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="mixtral-8x7b-32768")
hf = InferenceClient(token=os.getenv("HUGGINGFACE_API_TOKEN"))

def research(state: AgentState) -> AgentState:
    try:
        prompt = f"Generate a JSON spec for a landing page for: {state['task']}. " \
                 f"Fields: title, subtitle, sections[title,body], cta[text,url]."
        res = groq.invoke(prompt)
        state['messages'].append({'role':'research','content':res.content})
        return state
    except Exception as e:
        state['error'] = str(e); return state

def writer(state: AgentState) -> AgentState:
    try:
        base = state['messages'][-1]['content']
        # fallback HF si hace falta (texto corto)
        if not base or "{" not in base:
            base = hf.text_generation("Landing JSON for: "+state['task'], max_new_tokens=256)
        # Validar que sea JSON
        try:
            parsed = json.loads(base)
        except Exception:
            # intento de reparar
            base = base[base.find("{"): base.rfind("}")+1]
            parsed = json.loads(base)
        state['result'] = json.dumps(parsed)
        return state
    except Exception as e:
        state['error'] = str(e); return state

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("research", research)
    g.add_node("writer", writer)
    g.set_entry_point("research")
    g.add_edge("research","writer")
    g.add_edge("writer", END)
    return g.compile()

if __name__ == "__main__":
    import sys
    task = sys.argv[1] if len(sys.argv)>1 else ""
    flow = build_graph()
    state = AgentState(messages=[], task=task, result="", error="")
    out = flow.invoke(state)
    print(json.dumps({
        "success": not bool(out['error']),
        "result": out.get("result",""),
        "error": out.get("error",""),
        "messages": out.get("messages",[])
    }))
