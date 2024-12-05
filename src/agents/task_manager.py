from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from typing import List, Dict
import json


class TaskManager:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.1:8b")
        self.setup_prompts()
        self.setup_chains()

    def setup_prompts(self):
        self.system_prompt = """You are an AI assistant that strictly follows output format requirements.
You must adhere to the following rules:

**Core Principles**

1. ALWAYS verify the required output format before responding
2. NEVER deviate from the specified format
3. Respond with an error if the format requirements are unclear"""

        self.task_generation_template = """
以下のプロジェクト概要に基づいて、必要なタスクを洗い出し、優先順位と工数を設定してください：

{input}

以下の形式でJSONを出力してください：
{{
    "tasks": [
        {{
            "id": "task-1",
            "name": "タスク名",
            "description": "詳細な説明",
            "priority": 1-5,
            "estimated_hours": 数値,
            "dependencies": ["task-id", ...],
            "phase": "準備/実装/テスト/その他"
        }}
    ]
}}
"""

        self.schedule_template = """
以下のタスクリストとプロジェクト制約に基づいて、最適なスケジュールを生成してください：

タスク：
{tasks}

制約条件：
{constraints}

出力形式（JSON）：
{{
    "schedule": [
        {{
            "task_id": "task-1",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "assigned_to": "担当者役割"
        }}
    ],
    "total_duration": "予測される総期間（週単位）",
    "critical_path": ["task-id", ...]
}}
"""

    def setup_chains(self):
        # self.task_chain = LLMChain(llm=self.llm, prompt=self.task_generation_template)
        self.task_chain = ChatPromptTemplate([
            ("system", self.system_prompt),
            ("user", self.task_generation_template)
        ]) | self.llm
        # self.schedule_chain = LLMChain(llm=self.llm, prompt=self.schedule_template)
        self.schedule_chain = ChatPromptTemplate([
            ("system", self.system_prompt),
            ("user", self.schedule_template)
        ]) | self.llm

    def generate_tasks(self, project_description: str) -> Dict:
        """プロジェクト概要からタスクを生成"""
        # response = self.task_chain.run(input=project_description)
        response = self.task_chain.invoke({"input": project_description})
        return json.loads(response.content)

    def create_schedule(self, tasks: List[Dict], constraints: str) -> Dict:
        """タスクリストからスケジュールを生成"""
        tasks_str = json.dumps(tasks, ensure_ascii=False, indent=2)
        # response = self.schedule_chain.run(tasks=tasks_str, constraints=constraints)
        response = self.schedule_chain.invoke({"tasks": tasks_str, "constraints": constraints})
        return json.loads(response.content)

    def calculate_cost_estimate(self, tasks: List[Dict], rates: Dict[str, float]) -> Dict:
        """タスクリストから概算費用を計算"""
        total_cost = 0
        cost_breakdown = {}

        for task in tasks:
            role = task.get("assigned_to", "一般エンジニア")
            hours = task.get("estimated_hours", 0)
            rate = rates.get(role, rates["一般エンジニア"])
            
            task_cost = hours * rate
            total_cost += task_cost
            
            phase = task.get("phase", "その他")
            if phase not in cost_breakdown:
                cost_breakdown[phase] = 0
            cost_breakdown[phase] += task_cost

        return {
            "total_cost": total_cost,
            "breakdown_by_phase": cost_breakdown,
            "currency": "JPY"
        }
