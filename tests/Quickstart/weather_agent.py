from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from dataclasses import dataclass


SYSTEM_PROMPT = """
你是Gemini，当询问天气的时候必要时调用工具回答用户问题，而且天气相关问题时很爱玩双关语。

你可以使用两个工具：

- get_weather_for_location：用来获取某个具体地点的天气
- get_user_location：用来获取用户的位置

如果用户向你询问天气，一定要先确认地点。如果你能从问题中判断出他们指的是“我所在的地方”，就使用 get_user_location 工具来获取他们的位置。

"""

@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气。"""
    return f"在{city} 总是晴天！"

@dataclass
class Context:
    """自定义运行时的上下文结构"""
    user_id: str

# 先不玩 context 这一套
# 先不玩 context 这一套
# 先不玩 context 这一套
@tool
def get_user_location() -> str:
    """根据当前用户获取所在城市。"""
    return "昆明"  # 先不玩 context 这一套


@dataclass
class ResponseFormat:
    """用于 Agent 的响应结构数据"""
    # 搞笑（双关）风格的回复
    punny_response: str | None = None
    # 如果有的话，关于天气的有趣信息
    weather_conditions: str | None = None


model = init_chat_model("google_genai:gemini-2.5-flash")

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,\
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# `thread_id` 是当前这段对话的唯一标识符。
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "外面的天气怎么样？"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])