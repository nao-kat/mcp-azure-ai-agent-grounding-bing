import time
import json
import os
from dotenv import load_dotenv

from azure.ai.agents.models import MessageTextContent, ListSortOrder
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from azure.ai.agents.models import BingGroundingTool

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数から設定を取得
PROJECT_ENDPOINT = os.getenv("AZURE_PROJECT_ENDPOINT")
CONNECTION_ID = os.getenv("AZURE_CONNECTION_ID")

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=AzureCliCredential(),
)

bing = BingGroundingTool(
    connection_id=CONNECTION_ID,
    market="ja-JP",
    set_lang="ja-JP",
    count=10,
    freshness="Day"
)

with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4.1",  # 利用するモデルに変更
        name="MyGroundedAgent",  # 利用するエージェントの名前
        instructions="You are a helpful assistant. Use the tools provided to answer the user's questions. Be sure to cite your sources.",
        tools=bing.definitions + [
            {
                "type": "mcp",
                "server_label": "github",
                "server_url": "https://gitmcp.io/Azure/azure-rest-api-specs"
            }
        ],
        tool_resources=bing.resources
    )
    print(f"Created agent, agent ID: {agent.id}")

    thread = project_client.agents.threads.create()
    print(f"Created thread, thread ID: {thread.id}")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="最新の天気予報や交通情報、注目ニュースを教えてください。信頼できるメディアから3件、URL付きで教えてください。" #適宜変更する
    )
    print(f"Created message, message ID: {message.id}")

    run = project_client.agents.runs.create(thread_id=thread.id, agent_id=agent.id)

    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(5)
        run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)
        print(f"Run status: {run.status}")

    if run.status == "failed":
        print(f"Run error: {run.last_error}")

    run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)

    messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for data_point in messages:
        last_message_content = data_point.content[-1]
        if isinstance(last_message_content, MessageTextContent):
            print(f"{data_point.role}: {last_message_content.text.value}")
