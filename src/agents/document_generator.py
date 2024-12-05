from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any
import json
import markdown
from datetime import datetime


class DocumentGenerator:
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

        self.proposal_template = """
以下の情報を基に、提案書を作成してください：

プロジェクト情報：
{project_info}

タスク情報：
{tasks}

スケジュール：
{schedule}

費用：
{costs}

以下の形式でMarkdown形式の提案書を作成してください：

# プロジェクト提案書

## 1. エグゼクティブサマリー
[プロジェクトの概要と主要なポイントを簡潔に記述]

## 2. 課題と目的
[現状の課題と本プロジェクトの目的を詳細に記述]

## 3. 提案内容
[具体的な提案内容を記述]

## 4. 実施体制とスケジュール
[プロジェクト体制とマイルストーン付きのスケジュールを記述]

## 5. 費用
[費用の詳細な内訳と支払い条件を記述]

## 6. 期待される効果
[プロジェクト完了後に得られる効果を記述]

## 7. リスクと対策
[想定されるリスクとその対策を記述]
"""

        self.review_template = """
以下の提案書をレビューし、改善点を指摘してください：

{document}

以下の観点で評価し、具体的な改善提案をしてください：
1. 内容の整合性
2. 論理の流れ
3. 表現の適切さ
4. 必要な情報の過不足
5. ビジネス価値の明確さ

出力形式（JSON）：
{{
    "overall_evaluation": "全体評価（1-5）",
    "review_points": [
        {{
            "category": "カテゴリ",
            "issue": "問題点",
            "suggestion": "改善案",
            "priority": 1-5
        }}
    ],
    "summary": "総評"
}}
"""

    def setup_chains(self):
        # self.proposal_chain = LLMChain(llm=self.llm, prompt=self.proposal_template)
        self.proposal_chain = ChatPromptTemplate([
            ("system", self.system_prompt),
            ("user", self.proposal_template)
        ]) | self.llm
        # self.review_chain = LLMChain(llm=self.llm, prompt=self.review_template)
        self.review_chain = ChatPromptTemplate([
            ("system", self.system_prompt),
            ("user", self.review_template)
        ]) | self.llm

    def generate_proposal(self, project_info: Dict, tasks: Dict, schedule: Dict, costs: Dict) -> str:
        """提案書の生成"""
        response = self.proposal_chain.invoke({
            "project_info": json.dumps(project_info, ensure_ascii=False),
            "tasks": json.dumps(tasks, ensure_ascii=False),
            "schedule": json.dumps(schedule, ensure_ascii=False),
            "costs": json.dumps(costs, ensure_ascii=False)
        })
        return response.content

    def review_document(self, document: str) -> Dict:
        """提案書のレビュー実施"""
        response = self.review_chain.invoke({"document": document})
        return json.loads(response.content)

    def apply_feedback(self, document: str, feedback: Dict) -> str:
        """フィードバックを基に提案書を修正"""
        revision_template = """
以下の文書を、フィードバックに基づいて修正してください：

原文書：
{document}

フィードバック：
{feedback}

修正後の文書を出力してください。
"""

        # revision_chain = LLMChain(llm=self.llm, prompt=revision_template)
        revision_chain = ChatPromptTemplate([
            ("system", self.system_prompt),
            ("user", revision_template)
        ]) | self.llm
        
        sorted_feedback = sorted(
            feedback["review_points"],
            key=lambda x: x["priority"],
            reverse=True
        )
        
        current_doc = document
        for feedback_point in sorted_feedback:
            current_doc = revision_chain.invoke({
                "document": current_doc,
                "feedback": json.dumps(feedback_point, ensure_ascii=False)
            })
            current_doc = current_doc.content

        return current_doc

    def export_to_html(self, markdown_content: str) -> str:
        """MarkdownをHTMLに変換"""
        return markdown.markdown(markdown_content)