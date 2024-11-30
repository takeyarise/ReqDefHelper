from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import gradio as gr
import json

logger = logging.getLogger(__name__)


class ProjectIdea:
    def __init__(self):
        self.project_data = {
            "project_name": "",
            "purpose": "",
            "main_features": [],
            "target_users": "",
        }


    def interact_with_user(self, input_text, step):
        llm = ChatOllama(
            model=os.environ.get("MODEL", "gemma2:9b"),
            base_url=os.environ.get("BASE_URL", "http://localhost:11434"),
            # temperature=0.,
        )

        # build prompt
        if step == 0:
            prompt = "プロジェクトの名前を簡潔に教えてください．例えば、'AI分析ツール'など．"
        elif step == 1:
            prompt = (
                f"プロジェクト名が「{self.project_data['project_name']}」であることを前提に，"
                "このプロジェクトの目的を一文で教えてください．"
            )
        elif step == 2:
            prompt = (
                f"プロジェクト名が「{self.project_data['project_name']}」，"
                f"目的が「{self.project_data['purpose']}」であることを前提に，"
                "このプロジェクトで必要な主な機能を箇条書きで 3 つ教えてください．"
            )
        elif step == 3:
            prompt = (
                f"プロジェクト名が「{self.project_data['project_name']}」，"
                f"目的が「{self.project_data['purpose']}」，"
                f"主な機能が「{self.project_data['main_features']}」であることを前提に，"
                "このプロジェクトのターゲットとなるユーザーを教えてください．"
            )
        else:
            return "プロジェクトアイデアが完成しました．以下が概要です．", self.project_data

        prompt = PromptTemplate.from_template(prompt)
        conversation = prompt | llm
        response = conversation.invoke({})

        # データを収集
        if step == 0:
            self.project_data['project_name'] = response.content.strip()
        elif step == 1:
            self.project_data['purpose'] = response.content.strip()
        elif step == 2:
            self.project_data['main_features'] = [item.strip() for item in response.content.split(',')]
        elif step == 3:
            self.project_data['purpose'] = response.content.strip()

        return response.content, self.project_data

    def main_ui(self, user_input, step):
        response, updated_project_data = self.interact_with_user(user_input, step)
        if step >= 4:
            return json.dump(updated_project_data, indent=4, ensure_ascii=False), step
        return response, step + 1


if __name__ == '__main__':
    pi = ProjectIdea()
    interface = gr.Interface(
        fn=pi.main_ui,
        inputs[
            gr.Textbox(label="ユーザーの入力をどうぞ", lines=2),
            gr.Number(label="現在のステップ (0: プロジェクト名, 1: 目的...)", default=0),
        ],
        outputs=[
            gr.Textbox(label="AIからの応答", lines=3),
            gr.Number(label="次のステップ", default=0)
        ],
    )

    interface.launch()



