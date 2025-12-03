from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """获取给定城市的天气（示例工具，返回固定文案）"""
    return f"{city} 今日多云，最高 25℃，最低 18℃。"

model = init_chat_model("google_genai:gemini-2.5-flash")

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是Gemini，当询问天气的时候必要时调用工具回答用户问题。",
)

input_messages = []

while True:
    user_input = input("请输入问题: ")
    if user_input.lower() in ("exit", "quit", "q"):
        break
    input_messages.append({"role": "user", "content": user_input})
    result = agent.invoke({
        "messages": input_messages
    })
    input_messages.append({"role": "assistant", "content": result["messages"][-1].content})
    print(result["messages"][-1].content)

