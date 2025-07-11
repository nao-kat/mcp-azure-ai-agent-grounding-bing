# This script is used to **send requests to an already created agent**. It connects to the existing agent using its ID and allows interactions via the MCP interface.

import time
import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential  # または DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import (
    BingGroundingTool,
    MessageTextContent,
    ListSortOrder
)

# 環境変数の読み込み (.env ファイルから)
load_dotenv()

# 環境変数の取得
PROJECT_ENDPOINT = os.getenv("AZURE_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AGENT_ID")

# Azure AI Project Client の初期化
project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=AzureCliCredential(),  # 必要に応じて DefaultAzureCredential に変更
)

# 既存エージェントに接続
agent = project_client.agents.get_agent(agent_id=AGENT_ID)

# 新しいスレッドを開始
thread = project_client.agents.threads.create()

# ユーザーメッセージを送信
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="<write user prompt here>"  
)

# エージェント実行を開始
run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

# 実行ステータスをポーリング
while run.status in ["queued", "in_progress", "requires_action"]:
    time.sleep(5)
    run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

# 応答メッセージを取得・表示
messages = project_client.agents.messages.list(
    thread_id=thread.id,
    order=ListSortOrder.ASCENDING
)

for msg in messages:
    content = msg.content[-1]
    if isinstance(content, MessageTextContent):
        print(f"{msg.role}: {content.text.value}")
