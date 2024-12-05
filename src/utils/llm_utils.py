from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
import json

def create_llm(model_name: str = "llama3.1:8b") -> Ollama:
    """LLMインスタンスの作成"""
    return Ollama(model=model_name)

def format_json_output(data: Dict[str, Any]) -> str:
    """JSON出力の整形"""
    return json.dumps(data, ensure_ascii=False, indent=2)

def load_prompt_template(template_path: str) -> PromptTemplate:
    """プロンプトテンプレートの読み込み"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    return PromptTemplate.from_template(template)

def sanitize_llm_output(output: str) -> str:
    """LLM出力の整形とクリーニング"""
    output = output.strip()
    try:
        # JSON形式の場合は整形
        data = json.loads(output)
        return format_json_output(data)
    except json.JSONDecodeError:
        # プレーンテキストの場合はそのまま返す
        return output