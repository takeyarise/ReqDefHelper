# main.pyの内容
import gradio as gr
from agents.task_manager import TaskManager
from agents.document_generator import DocumentGenerator
from typing import Dict, Any
import json
from datetime import datetime

class RequirementsSystem:
    def __init__(self):
        self.task_manager = TaskManager()
        self.document_generator = DocumentGenerator()
        self.project_data = {}

    def analyze_project(self, description: str, goals: str) -> Dict[str, Any]:
        """プロジェクトの分析と初期化"""
        self.project_data = {
            "description": description,
            "goals": goals,
            "created_at": datetime.now().isoformat()
        }
        return self.project_data

    def generate_tasks(self, project_description: str) -> str:
        """タスクの生成"""
        tasks = self.task_manager.generate_tasks(project_description)
        self.project_data["tasks"] = tasks
        return json.dumps(tasks, ensure_ascii=False, indent=2)

    def create_schedule(self, tasks_json: str, constraints: str) -> str:
        """スケジュールの生成"""
        # tasks = json.loads(tasks_json)
        tasks = tasks_json
        schedule = self.task_manager.create_schedule(tasks, constraints)
        self.project_data["schedule"] = schedule
        return json.dumps(schedule, ensure_ascii=False, indent=2)

    def generate_proposal(self) -> str:
        """提案書の生成"""
        if not all(key in self.project_data for key in ["description", "tasks", "schedule"]):
            missing_keys = [key for key in ["description", "tasks", "schedule"] if key not in self.project_data]
            return """Error: 必要な情報が不足しています。プロジェクト情報、タスク、スケジュールを先に生成してください。
            不足している情報: {}
            """.format(missing_keys)
        
        rates = {
            "一般エンジニア": 10000,
            "シニアエンジニア": 15000,
            "プロジェクトマネージャー": 20000
        }
        costs = self.task_manager.calculate_cost_estimate(
            self.project_data["tasks"]["tasks"],
            rates
        )
        self.project_data["costs"] = costs

        proposal = self.document_generator.generate_proposal(
            self.project_data,
            self.project_data["tasks"],
            self.project_data["schedule"],
            costs
        )
        self.project_data["proposal"] = proposal
        return proposal

    def review_proposal(self, proposal: str) -> str:
        """提案書のレビュー"""
        review_result = self.document_generator.review_document(proposal)
        self.project_data["review"] = review_result
        return json.dumps(review_result, ensure_ascii=False, indent=2)

    def apply_feedback(self, proposal: str, feedback_json: str) -> str:
        """フィードバックの適用"""
        # feedback = json.loads(feedback_json)
        feedback = feedback_json
        revised_proposal = self.document_generator.apply_feedback(proposal, feedback)
        self.project_data["revised_proposal"] = revised_proposal
        return revised_proposal

def create_ui():
    """Gradioインターフェースの作成"""
    system = RequirementsSystem()

    with gr.Blocks() as app:
        gr.Markdown("# 要件定義支援システム")
        
        with gr.Tab("プロジェクト情報"):
            project_description = gr.Textbox(label="プロジェクトの説明", lines=5)
            project_goals = gr.Textbox(label="プロジェクトの目標", lines=3)
            analyze_btn = gr.Button("プロジェクトを分析")
            project_output = gr.JSON(label="分析結果")
            
            analyze_btn.click(
                system.analyze_project,
                inputs=[project_description, project_goals],
                outputs=[project_output]
            )

        with gr.Tab("タスク管理"):
            task_desc = gr.Textbox(label="タスク生成用の詳細情報", lines=5)
            generate_tasks_btn = gr.Button("タスクを生成")
            tasks_output = gr.JSON(label="生成されたタスク")
            
            constraints = gr.Textbox(label="スケジュール制約条件", lines=3)
            create_schedule_btn = gr.Button("スケジュールを生成")
            schedule_output = gr.JSON(label="生成されたスケジュール")
            
            generate_tasks_btn.click(
                system.generate_tasks,
                inputs=[task_desc],
                outputs=[tasks_output]
            )
            
            create_schedule_btn.click(
                system.create_schedule,
                inputs=[tasks_output, constraints],
                outputs=[schedule_output]
            )

        with gr.Tab("提案書作成"):
            generate_proposal_btn = gr.Button("提案書を生成")
            proposal_output = gr.Textbox(label="生成された提案書", lines=20)
            
            review_btn = gr.Button("提案書をレビュー")
            review_output = gr.JSON(label="レビュー結果")
            
            apply_feedback_btn = gr.Button("フィードバックを適用")
            revised_proposal = gr.Textbox(label="修正後の提案書", lines=20)
            
            generate_proposal_btn.click(
                system.generate_proposal,
                inputs=[],
                outputs=[proposal_output]
            )
            
            review_btn.click(
                system.review_proposal,
                inputs=[proposal_output],
                outputs=[review_output]
            )
            
            apply_feedback_btn.click(
                system.apply_feedback,
                inputs=[proposal_output, review_output],
                outputs=[revised_proposal]
            )

    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(share=False)