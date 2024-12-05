from typing import Dict, List, Any
import json
from datetime import datetime
from pathlib import Path

def save_project_data(project_data: Dict[str, Any], output_dir: str) -> str:
    """プロジェクトデータの保存"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"project_{timestamp}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)
    
    return str(output_path)

def load_project_data(file_path: str) -> Dict[str, Any]:
    """プロジェクトデータの読み込み"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_project_history(project_dir: str) -> List[Dict[str, Any]]:
    """プロジェクトの履歴取得"""
    path = Path(project_dir)
    project_files = sorted(path.glob("project_*.json"), reverse=True)
    
    history = []
    for file in project_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            history.append({
                "file_name": file.name,
                "created_at": data.get("created_at"),
                "title": data.get("title", "Untitled"),
                "data": data
            })
    
    return history