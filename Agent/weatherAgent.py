import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN, and OUTPUT steps.
You can PLAN multiple times if needed.
You may call TOOLS, and then wait for OBSERVE step before continuing.

Rules:
- Always return valid JSON in the format:
  { "step": "START" | "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE", "content": "string", "tool": "string", "input": "string" }

Available Tools:
- get_weather(city:str): returns the weather info about the city.
"""

# History
message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# Tool implementation
def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}"
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
}

def main():
    while True:
        user_query = input("👉 ")
        if user_query.lower() in ["exit", "quit"]:
            break

        message_history.append({"role": "user", "content": user_query})

        while True:
            response = client.responses.create(
                model="gpt-5",
                input=message_history
            )

            output_text = response.output_text.strip()

            try:
                parsed = json.loads(output_text)
            except json.JSONDecodeError:
                print("⚠️ Model did not return valid JSON:", output_text)
                break

            step = parsed.get("step")

            # Save model response in history
            message_history.append({"role": "assistant", "content": output_text})

            if step == "START":
                print("🔥", parsed.get("content"))
                continue

            elif step == "PLAN":
                print("🧠", parsed.get("content"))
                continue

            elif step == "TOOL":
                tool = parsed.get("tool")
                tool_input = parsed.get("input")
                if tool in available_tools:
                    tool_res = available_tools[tool](tool_input)
                    print(f"🔧 {tool}({tool_input}) → {tool_res}")
                    # Feed OBSERVE step back to model
                    observe_msg = {
                        "role": "developer",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": tool,
                            "input": tool_input,
                            "output": tool_res
                        })
                    }
                    message_history.append(observe_msg)
                    continue
                else:
                    print("⚠️ Unknown tool:", tool)
                    break

            elif step == "OUTPUT":
                print("🤖", parsed.get("content"))
                break

            else:
                print("⚠️ Unknown step:", parsed)
                break

if __name__ == "__main__":
    main()
