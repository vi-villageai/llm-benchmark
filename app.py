from fastapi import FastAPI, Request
from pydantic import BaseModel
import os, logging, argparse, yaml, copy, traceback, time, json, uvicorn
from typing import List, Optional, Union, Any
from datetime import datetime
from src.llm_base import LLMBase


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class InputRequest(BaseModel):
    prompt_id: int = None
    name: str = None
    description: str = None
    system_prompt: str = None
    provider_name: str = None
    generation_params: dict = None

    message: str = None
    history: List[dict] = None
    


if os.getenv("PATH_CONFIG") is not None and os.path.isfile(os.getenv("PATH_CONFIG")):
    # Reading file YAML
    with open(os.getenv("PATH_CONFIG"), "r") as file:
        CONFIG = yaml.safe_load(file)
        PROVIDER_MODELS = CONFIG.get("PROVIDER_MODELS")
        LLM_MANAGER = {}
        for provider_name, provider_setting in PROVIDER_MODELS.items():
            openai_setting = provider_setting.get("openai_setting")
            openai_setting["api_key"] = os.getenv(openai_setting.get("api_key"))
            LLM_MANAGER[provider_name] = LLMBase(
                openai_setting = openai_setting,
                provider_name = provider_name,
            )


app = FastAPI()
ROUTE = "llm-benchmark/api"


@app.get(f"/{ROUTE}")
async def health():
    return {"status": "OK"}


@app.post(f"/{ROUTE}/v1/bot/initSession")
async def init_session(inputs: InputRequest):
    try:
        
    except Exception as e:
        return {
            "status": -1,
            "msg": f"Bad request {traceback.format_exc()}",
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="Host of API", default="127.0.0.1")
    parser.add_argument("--port", type=int, help="Port of API", default=9330)
    parser.add_argument("--workers", type=int, help="Port of API", default=1)
    args = parser.parse_args()

    uvicorn.run("app:app", host=args.host, port=args.port, workers=args.workers)