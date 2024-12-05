# 要件定義支援システム

LLMを活用して要件定義プロセスを自動化・効率化するシステム。

## 機能

- 課題の自動分析と整理
- プロジェクト計画の立案
- タスクの自動生成と管理
- スケジュール最適化
- 提案書の自動生成とレビュー

## 技術スタック

- Python 3.10+
- ollama
- langchain
- gradio
- その他依存関係は`requirements.txt`を参照

## セットアップ

1. 環境構築
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

3. ollamaのセットアップ
```bash
ollama pull llama3.1:8b
```

## 使用方法

1. システムの起動
```bash
python src/main.py
```

2. ブラウザで以下のURLにアクセス
```
http://127.0.0.1:7860
```

3. 各タブで必要な情報を入力し、機能を利用

## プロジェクト構造

```
requirements_system/
├── requirements.txt
├── config/
│   └── config.yaml
├── src/
│   ├── main.py
│   ├── agents/
│   │   ├── task_manager.py
│   │   └── document_generator.py
│   ├── models/
│   │   ├── issue.py
│   │   ├── project.py
│   │   └── task.py
│   └── utils/
│       ├── llm_utils.py
│       └── data_utils.py
└── data/
    └── templates/
        ├── project_template.md
        └── proposal_template.md
```

## 注意事項

- ollama のセットアップが必要です
- llama3.1:8b モデルを使用します
- メモリ要件：最低 8 GB 推奨