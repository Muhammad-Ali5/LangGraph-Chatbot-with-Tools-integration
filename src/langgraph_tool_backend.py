from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import os
import requests
import json
import random

load_dotenv()
import time

def safe_api_call(func, *args, **kwargs):
    max_retries = 3
    delay = 1
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                if attempt == max_retries - 1:
                    return "❌ Rate limit exceeded. Please try again later."
                time.sleep(delay)
                delay *= 2
            else:
                raise
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2

# =========================LLM Setup======================
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
)

# =========================Tools Setup======================
# ========================DuckDuckGo Search Tool======================
search_tool = DuckDuckGoSearchRun()

@tool
def calculator_tool(first_num: float, second_num: float, operation: str) -> str:
    """
    A simple calculator tool for basic arithmetic operations.
    Supported operations: add, subtract, multiply, divide.
    """
    try:
        if operation == "add":
            result = first_num + second_num
            return f"{first_num} + {second_num} = {result}"
        elif operation == "subtract":
            result = first_num - second_num
            return f"{first_num} - {second_num} = {result}"
        elif operation == "multiply":
            result = first_num * second_num
            return f"{first_num} × {second_num} = {result}"
        elif operation == "divide":
            if second_num == 0:
                return "❌ Error: Division by zero is not allowed."
            result = first_num / second_num
            return f"{first_num} ÷ {second_num} = {result}"
        else:
            return f"❌ Error: Unsupported operation '{operation}'. Use: add, subtract, multiply, or divide."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ========================Stock Price Tool======================
@tool
def get_stock_price(symbol: str) -> str:
    """
    Fetch the current stock price for a given symbol using Alpha Vantage API.
    symbol (str): The stock symbol (e.g., 'AAPL', 'GOOGL', 'MSFT')
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return "⚠️ ALPHA_VANTAGE_API_KEY not configured. Using mock data."
    
    try:
        url = "https://www.alphavantage.co/query"
        params = {'function': 'GLOBAL_QUOTE', 'symbol': symbol.upper(), 'apikey': api_key}
        response = requests.get(url, params=params, timeout=8)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"].get("05. price"):
            price = float(data["Global Quote"]["05. price"])
            change = data["Global Quote"].get("09. change", "N/A")
            return f"📈 {symbol.upper()}: ${price:.2f} (Change: {change})"
        else:
            # Fallback to mock data
            mock_prices = {"AAPL": 195.50, "GOOGL": 142.80, "TSLA": 238.45, "MSFT": 380.25, "AMZN": 180.50}
            price = mock_prices.get(symbol.upper(), 150.00)
            return f"📈 {symbol.upper()}: ${price:.2f} (mock data)"
    except Exception as e:
        return f"❌ Error fetching stock price: {str(e)}"

# ========================Weather Tool======================
@tool
def fetch_weather(city: str) -> str:
    """
    Fetch the current weather for a given city using the WeatherAPI.
    city (str): The name of the city (e.g., 'London', 'New York')
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "⚠️ WEATHER_API_KEY not configured. Using mock data."
    
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        r = requests.get(url, timeout=8)
        data = json.loads(r.text)
        
        if "error" in data:
            # Fallback to mock data
            mock_weather = {
                "london": "🌤️ London: 12°C, Cloudy, Humidity: 75%",
                "new york": "☀️ New York: 18°C, Sunny, Humidity: 60%",
                "tokyo": "⛅ Tokyo: 22°C, Partly Cloudy, Humidity: 65%"
            }
            return mock_weather.get(city.lower(), f"🌤️ {city.title()}: 20°C, Clear, Humidity: 70%")
        
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        return f"🌤️ {city.title()}: {temp}°C, {condition}, Humidity: {humidity}%"
    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"

# ========================News Tool======================
@tool
def fetch_news(topic: str) -> str:
    """
    Fetch latest news headlines on a given topic.
    topic (str): The news topic (e.g., 'technology', 'sports').
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return "⚠️ NEWS_API_KEY not configured. Using mock data."
    
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&pageSize=5&sortBy=publishedAt"
        r = requests.get(url, timeout=8)
        data = json.loads(r.text)
        
        if "articles" in data and data["articles"]:
            headlines = [f"• {article['title']}" for article in data["articles"][:5]]
            return f"📰 Latest {topic.title()} News:\n" + "\n".join(headlines)
        else:
            # Mock data fallback
            mock_news = {
                "technology": ["• AI Models Reach New Capabilities", "• Tech Giants Invest in Quantum Computing"],
                "business": ["• Stock Markets Show Growth", "• Major Companies Report Earnings"],
                "sports": ["• Championship Teams Advance", "• Record Breaking Performances"]
            }
            headlines = mock_news.get(topic.lower(), ["• Latest news updates"])
            return f"📰 Latest {topic.title()} News:\n" + "\n".join(headlines)
    except Exception as e:
        return f"❌ Error fetching news: {str(e)}"

# ========================Currency Converter Tool======================
@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another.
    amount (float): The amount to convert.
    from_currency (str): Source currency (e.g., 'USD').
    to_currency (str): Target currency (e.g., 'EUR').
    """
    api_key = os.getenv("EXCHANGE_API_KEY")
    if not api_key:
        return "⚠️ EXCHANGE_API_KEY not configured. Using mock rates."
    
    try:
        url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
        r = requests.get(url, timeout=8)
        data = json.loads(r.text)
        
        if "rates" in data:
            from_curr = from_currency.upper()
            to_curr = to_currency.upper()
            rate = data["rates"][to_curr] / data["rates"][from_curr]
            result = amount * rate
            return f"💱 {amount} {from_curr} = {result:.2f} {to_curr}"
        else:
            # Mock rates fallback
            mock_rates = {("USD", "EUR"): 0.92, ("USD", "GBP"): 0.79, ("EUR", "USD"): 1.09}
            rate = mock_rates.get((from_currency.upper(), to_currency.upper()), 1.0)
            result = amount * rate
            return f"💱 {amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()} (mock rate)"
    except Exception as e:
        return f"❌ Error converting currency: {str(e)}"

# ========================Joke Tool======================
@tool
def get_joke(category: str = "Any") -> str:
    """
    Fetch a random joke from a category.
    category (str): Joke category (e.g., 'Programming', 'Pun', 'Misc', 'Any'). Default: 'Any'.
    """
    try:
        url = f"https://v2.jokeapi.dev/joke/{category}?type=single"
        r = requests.get(url, timeout=8)
        data = json.loads(r.text)
        
        if "joke" in data and data["joke"]:
            return f"😂 {data['joke']}"
        elif "setup" in data and "delivery" in data:
            return f"😂 {data['setup']}\n\n{data['delivery']}"
        else:
            # Fallback jokes
            fallback_jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What did the ocean say to the beach? Nothing, it just waved!",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ]
            return f"😂 {random.choice(fallback_jokes)}"
    except Exception as e:
        return f"😂 Why don't programmers like nature? It has too many bugs!"

# ========================NASA APOD Tool======================
@tool
def get_nasa_apod() -> str:
    """
    Fetch NASA's Astronomy Picture of the Day (APOD).
    """
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        return "⚠️ NASA_API_KEY not configured. Please add it to your .env file to use this feature.\n\nGet your free API key at: https://api.nasa.gov"
    
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        r = requests.get(url, timeout=8)
        data = json.loads(r.text)
        
        if "error" not in data:
            title = data.get("title", "Astronomy Picture")
            explanation = data.get("explanation", "")[:250]
            image_url = data.get("url", "")
            return f"🌌 **{title}**\n\n{explanation}...\n\n🖼️ Image: {image_url}"
        else:
            return "🌌 **Pillars of Creation**\n\nThe iconic Pillars of Creation are elephant-like stellar nurseries in the Eagle Nebula, showcasing the beauty of star formation."
    except Exception as e:
        return f"❌ Error fetching NASA APOD: {str(e)}"

# ========================IP Location Tool======================
@tool
def get_ip_location(ip: str) -> str:
    """
    Fetch location info for a given IP address.
    ip (str): The IP address (e.g., '8.8.8.8').
    """
    try:
        url = f"https://ipapi.co/{ip}/json/"
        r = requests.get(url, timeout=8)
        data = json.loads(r.text)
        
        if "error" not in data:
            city = data.get("city", "Unknown")
            country = data.get("country_name", "Unknown")
            region = data.get("region", "")
            lat = data.get("latitude", "N/A")
            lon = data.get("longitude", "N/A")
            
            location = f"{city}, {region}, {country}" if region else f"{city}, {country}"
            return f"🌐 IP: {ip}\n📍 Location: {location}\n🗺️ Coordinates: {lat}, {lon}"
        else:
            return f"❌ Error: {data.get('reason', 'Unknown error')}"
    except Exception as e:
        return f"❌ Error fetching IP location: {str(e)}"

tools = [search_tool, calculator_tool, get_stock_price, fetch_weather, fetch_news, convert_currency, get_joke, get_nasa_apod, get_ip_location]
llm_with_tools = llm.bind_tools(tools=tools)

# =========================State===========================
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# =========================Graph Node Definition======================
def chat_node(state: ChatState) -> dict:
    """LLM node that handles conversation or requests a tool call."""
    try:
        last_message = state["messages"][-1].content.lower()
        # Handle casual conversation
        if "how are you" in last_message or "hey" in last_message:
            return {"messages": [AIMessage(content="Hey there! I'm ready to help. What's on your mind?")]}
        # Handle single joke request
        elif "tell me a joke" in last_message or "another joke" in last_message:
            return {"messages": [AIMessage(content="", tool_calls=[{"name": "get_joke", "args": {"category": "Any"}, "id": "joke_call"}])]}
        # Handle multiple joke requests (e.g., "tell me 4 jokes")
        elif "joke" in last_message and any(num in last_message for num in ["1", "2", "3", "4", "5"]):
            try:
                num_jokes = int(next(num for num in ["1", "2", "3", "4", "5"] if num in last_message))
                tool_calls = [
                    {"name": "get_joke", "args": {"category": random.choice(["Any", "Programming", "Pun", "Misc"])}, "id": f"joke_call_{i}"}
                    for i in range(num_jokes)
                ]
                return {"messages": [AIMessage(content="", tool_calls=tool_calls)]}
            except:
                return {"messages": [AIMessage(content="", tool_calls=[{"name": "get_joke", "args": {"category": "Any"}, "id": "joke_call"}])]}
        else:
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}
    except Exception as e:
        print(f"Error in chat_node: {str(e)}")
        return {"messages": [SystemMessage(content="Sorry, I hit an error. Please try again.")]}

def custom_tools_node(state: ChatState) -> dict:
    """Custom tools node to handle tool call results cleanly."""
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        tool_results = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            # Find and execute the tool
            for tool in tools:
                if tool.name == tool_name:
                    result = tool.invoke(tool_args)
                    # Convert result to string if it's a dict
                    if isinstance(result, dict):
                        if "joke" in result:
                            result = result["joke"]
                        elif "error" in result:
                            result = f"Error: {result['error']}"
                        else:
                            result = json.dumps(result)
                    tool_results.append(AIMessage(content=result, tool_call_id=tool_id))
        return {"messages": tool_results}
    return {"messages": []}

# =========================Database Setup======================
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# =========================Graph Definition======================
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools_node", custom_tools_node)

graph.add_edge(START, "chat_node")

def route_tools(state: ChatState):
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools_node"
    return "__end__"

graph.add_conditional_edges(
    "chat_node",
    route_tools,
    {
        "tools_node": "tools_node",
        "__end__": END,
    }
)

graph.add_edge("tools_node", "chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

# =========================Database Operations======================
def retrieve_all_threads():
    """Retrieve all unique thread IDs from checkpoints."""
    all_threads = set()
    try:
        for checkpoint in checkpointer.list(None):
            all_threads.add(checkpoint["config"]["configurable"]["thread_id"])
    except Exception as e:
        print(f"Error retrieving threads: {e}")
    return list(all_threads)

def get_threads():
    """Get all thread IDs (frontend compatibility function)."""
    return retrieve_all_threads()

def delete_thread(thread_id: str) -> bool:
    """Delete a specific thread from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
        cursor.execute("DELETE FROM checkpoint_writes WHERE thread_id = ?", (thread_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting thread {thread_id}: {e}")
        return False