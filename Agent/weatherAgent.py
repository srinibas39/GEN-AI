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
You work on START, THINK, and OUTPUT steps.
You can THINK multiple times if needed.
You may call TOOLS, and then wait for OBSERVE step before continuing.

CRITICAL JSON RULES:
- You MUST return ONLY ONE JSON object per response
- NEVER return multiple JSON objects in one response
- Each response must be a single, valid JSON object that can be parsed
- Do NOT include any text before or after the JSON object
- Do NOT include explanatory text or comments with the JSON
- Do NOT repate the same step again and again.
- If no tool is present for a task, say "Sorry, I don't have permission to perform this task"

Response Flow Rules:
- Always perform only one step at a time and wait for the next step
- Follow the sequence: START → THINK → (TOOL if needed) → OBSERVE (if tool used) → OUTPUT
- You can have multiple THINK steps before OUTPUT
- For every tool call, wait for the OBSERVE step before continuing
- If no tool is present for a task, say "Sorry, I don't have permission to perform this task"
- Do not repeat the same step again and again
- Follow the Example given below strictly.
- Always first 3 steps
- If the user query is not related to the tools available, say "Sorry, I don't have permission to perform this task"

Output JSON Format:
{ "step": "START | THINK | OUTPUT | OBSERVE | TOOL", "content": "string", "tool_name": "string", "input": "string" }

Example:
    User: Hey, can you tell me weather of Patiala?
    ASSISTANT: { "step": "START", "content": "The user is intertested in the current weather details about Patiala" } 
    ASSISTANT: { "step": "THINK", "content": "Let me see if there is any available tool for this query" } 
    ASSISTANT: { "step": "THINK", "content": "I see that there is a tool available getWeatherDetailsByCity which returns current weather data" } 
    ASSISTANT: { "step": "THINK", "content": "I need to call getWeatherDetailsByCity for city patiala to get weather details" }
    ASSISTANT: { "step": "TOOL", "input": "patiala", "tool_name": "getWeatherDetailsByCity" }
    DEVELOPER: { "step": "OBSERVE", "content": "The weather of patiala is cloudy with 27 Cel" }
    ASSISTANT: { "step": "THINK", "content": "Great, I got the weather details of Patiala" }
    ASSISTANT: { "step": "OUTPUT", "content": "The weather in Patiala is 27 C with little cloud. Please make sure to carry an umbrella with you. ☔️" }

Example:
    User: Hey, can you tell me 2 + 2?
    ASSISTANT: { "step": "START", "content": "The user is interested in solving a simple arithmetic: 2 + 2." } 
    ASSISTANT: { "step": "THINK", "content": "Let me see if there is any available tool for this query" } 
    ASSISTANT: { "step": "THINK", "content": "It seems there is no tool available for arithmetic calculations" } 
    ASSISTANT: { "step": "THINK", "content": "No tool is present for this task, so I should say I don't have permission" }
    ASSISTANT: { "step": "OUTPUT", "content": "Sorry, I don't have permission to perform this task" }

Available Tools:
- get_weather(city:str): returns the weather info about the city.
- get_date_time(timezone:str): returns the date and time in the given timezone.
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



def get_date_time(timezone: str):
    url = f"https://timeapi.io/api/time/current/zone?timeZone={timezone}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        date = data.get("date")
        time = data.get("time")
        return f"📅 Date: {date} | 🕒 Time: {time} ({timezone})"
    else:
        return f"❌ Something went wrong: {response.status_code}"


available_tools = {
    "get_weather": get_weather,
    "get_date_time": get_date_time,
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

            elif step == "THINK":
                print("🧠", parsed.get("content"))
                continue

            elif step == "TOOL":
                tool = parsed.get("tool_name")
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
            elif step == "OBSERVE":
                print("👀", parsed.get("content"))
                continue

            elif step == "OUTPUT":
                print("🤖", parsed.get("content"))
                break

            else:
                print("⚠️ Unknown step:", parsed)
                break

if __name__ == "__main__":
    main()
