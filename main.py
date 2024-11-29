import pypdf
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
# from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
import gradio as gr
from dotenv import load_dotenv
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_file):
    """ PDF テキスト抽出 """
    pdf_reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


summary_prompt_system = """
あなたは文章を一文で要約する専門家です。
与えられる文章は要件定義に使用するための文章です。
文章の要約にあたっては、最重要な情報のみを残し、それ以外の詳細を省略してください。
結果は例外なく常に一文で出力してください。
一文で要約できない場合でも、簡潔な形式で一文にまとめる努力をしてください。
""".strip()
summary_prompt_user = """以下の文章から何のための要件定義なのかを一文で要約してください。

- 要約は以下の形式で出力してください。
  形式例: [要約結果] 主題を示す簡潔な一文。
  具体例: [要約結果] 営業部門の成績を向上させるためのAI分析ツールを開発する。

文章:
{text}
"""
keywords_prompt_system = """
あなたは文章からキーワードを抽出する専門家です。
キーワードは文章の重要な要素を簡潔に表現する語句であり、冗長でないことが求められます。
出力は常に指定された形式に従い、過不足なく正確に抽出してください。
""".strip()
keywords_prompt_user = """以下の文章から、最重要なキーワードを3つだけ抽出してください。

- キーワードの抽出基準:
  1. 文章の主題を表す単語や短いフレーズを選ぶ。
  2. 固有名詞や重要な概念を優先する。
  3. 冗長な語句や曖昧な表現を避ける。

- 出力形式は以下の通りにしてください（必ずカンマで区切って一行で出力すること）。
  形式例: キーワード1, キーワード2, キーワード3
  具体例: 営業部門, AI分析ツール, 戦略立案

文章:
{text}
"""


def process_text_with_langchain(text):
    """ LangChain で要約とキーワード抽出 """

    logger.info(f"Text: {text}")

    # set up llm
    llm = ChatOllama(
        model=os.environ.get('MODEL', 'gemma2:9b'),
        base_url=os.environ.get('BASE_URL', "http://localhost:11434"),
        # temperature=0.,
    )

    # summary prompt
    summary_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(summary_prompt_system),
        HumanMessage(summary_prompt_user.format(text=text)),
    ])
    # summary_prompt = PromptTemplate.from_template(
    #     "要約以外は出力せず簡潔に答えて下さい．\n以下の文章を一文で要約してください．\n\n{text}"
    # )
    summary_chain = summary_prompt | llm
    summary = summary_chain.invoke({"text": text})
    summary = summary.content

    # extraction keywords prompt
    keywords_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(keywords_prompt_system),
        HumanMessage(keywords_prompt_user.format(text=text)),
    ])
    # keywords_prompt = PromptTemplate.from_template(
    #     "キーワード以外は出力せず簡潔に答えてください．\n以下の文章から主要なキーワードを 3 つ抽出してください．\n\n{text}"
    # )
    keywords_chain = keywords_prompt | llm
    keywords = keywords_chain.invoke({"text": text})
    keywords = keywords.content
    keywords = keywords.split("\n")
    keywords = [k.strip() for k in keywords]

    return summary, keywords


def process_uploaded_file(uploaded_file):
    """ データ解析と JSON 構造化 """
    if uploaded_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        with open(uploaded_file.name, 'r', encoding='utf-8') as f:
            text = f.read()
    elif uploaded_file.name.endswith('.md'):
        with open(uploaded_file.name, 'r', encoding='utf-8') as f:
            text = f.read()
    elif uploaded_file.name.endswith('.rst'):
        with open(uploaded_file.name, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        return json.dumps(
            {'error': '対応していないファイル形式です．対応している形式は pdf, md, rst, txt です．'},
            indent=4,
            ensure_ascii=False,
        )

    summary, keywords = process_text_with_langchain(text)

    result = {
        'background_summary': summary,
        'keywords': keywords,
    } 
    return json.dumps(result, indent=4, ensure_ascii=False)


def main_ui(file):
    """ Gradio UI 構築 """
    result = process_uploaded_file(file)
    return result


interface = gr.Interface(
    fn=main_ui,
    inputs=gr.File(label="ファイルをアップロードしてください． (pdf, md, rst, txt)"),
    outputs=gr.Textbox(label="解析結果 (JSON 形式)")
)

if __name__ == "__main__":
    load_dotenv()

    interface.launch()
