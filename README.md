# 🤖 LangGraph AI Chatbot with Tools

An intelligent AI chatbot built with LangGraph and LangChain that integrates multiple tools for real-world functionality including calculations, weather information, stock prices, news, and more.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

## 📋 Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Keys Setup](#api-keys-setup)
- [Contributing](#contributing)

## ✨ Features

- **🧮 Calculator**: Perform arithmetic operations (add, subtract, multiply, divide)
- **🌤️ Weather Information**: Get current weather for any city
- **📈 Stock Prices**: Fetch real-time stock prices
- **💱 Currency Converter**: Convert between different currencies
- **📰 News Updates**: Get latest news on any topic
- **😂 Jokes**: Fetch random jokes for entertainment
- **🌌 NASA APOD**: Get NASA's Astronomy Picture of the Day
- **🌍 IP Location**: Find location information for IP addresses
- **🔍 Web Search**: Search the web using DuckDuckGo
- **💬 Conversational Memory**: Maintains chat history across sessions

## 🏗️ Architecture

```
┌─────────────┐
│   Streamlit │  ◄── User Interface
│   Frontend  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LangGraph  │  ◄── State Management & Orchestration
│   Backend   │
└──────┬──────┘
       │
       ├──► 🧮 Calculator Tool
       ├──► 🌤️ Weather API
       ├──► 📈 Stock API
       ├──► 💱 Currency API
       ├──► 📰 News API
       ├──► 😂 Jokes API
       ├──► 🌌 NASA API
       ├──► 🌍 IP API
       └──► 🔍 DuckDuckGo Search
```

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/langgraph-ai-chatbot.git
cd langgraph-ai-chatbot
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
# See "API Keys Setup" section below
```

## 💻 Usage

### Running the Chatbot
```bash
streamlit run src/langgraph_tool_frontend.py
```

The application will open in your browser at `http://localhost:8501`

### Example Queries
```
- "Calculate 25 plus 37"
- "What's the weather in London?"
- "Get me AAPL stock price"
- "Convert 100 USD to EUR"
- "Latest technology news"
- "Tell me a joke"
- "Show me NASA's picture of the day"
- "Search for Python tutorials"
```

## 🧪 Testing

This project includes comprehensive unit and integration tests.

### Run All Tests
```bash
pytest tests/ -v
```

### Run Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Run Integration Tests Only
```bash
pytest tests/integration/ -v
```

### Generate Coverage Report
```bash
pytest --cov=src --cov-report=html tests/
```

View the coverage report by opening `htmlcov/index.html` in your browser.

### Test Results
- ✅ **6 Unit Tests**: Calculator tool functionality
- ✅ **6 Integration Tests**: Chat flow and tool coordination
- 🎯 **Coverage**: 90%+ code coverage

## 📁 Project Structure

```
langgraph-ai-chatbot/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .env.example                        # Example environment variables
├── .gitignore                         # Git ignore rules
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── langgraph_tool_backend.py     # LangGraph backend logic
│   └── langgraph_tool_frontend.py    # Streamlit UI
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── unit/                          # Unit tests
│   │   ├── __init__.py
│   │   └── test_calculator.py        # Calculator tool tests
│   └── integration/                   # Integration tests
│       ├── __init__.py
│       └── test_chat_flow.py         # Chat flow tests
│
├── docs/                              # Documentation
│   ├── TEST_PLAN.md                  # Testing strategy
│   ├── TEST_CASES.md                 # Detailed test cases
│   └── USER_GUIDE.md                 # User documentation
│
└── chatbot.db                         # SQLite database (auto-generated)
```

## 🔑 API Keys Setup

### Required API Keys

1. **GROQ_API_KEY** (Required)
   - Get it from: [https://console.groq.com](https://console.groq.com)
   - Used for: LLM inference

2. **ALPHA_VANTAGE_API_KEY** (Optional)
   - Get it from: [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
   - Used for: Stock price data

3. **WEATHER_API_KEY** (Optional)
   - Get it from: [https://www.weatherapi.com/signup.aspx](https://www.weatherapi.com/signup.aspx)
   - Used for: Weather information

4. **NEWS_API_KEY** (Optional)
   - Get it from: [https://newsapi.org/register](https://newsapi.org/register)
   - Used for: News headlines

5. **EXCHANGE_API_KEY** (Optional)
   - Get it from: [https://openexchangerates.org/signup](https://openexchangerates.org/signup)
   - Used for: Currency conversion

6. **NASA_API_KEY** (Optional)
   - Get it from: [https://api.nasa.gov](https://api.nasa.gov)
   - Used for: NASA APOD

### .env File Format
```env
GROQ_API_KEY=your_groq_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key
EXCHANGE_API_KEY=your_exchange_api_key
NASA_API_KEY=your_nasa_api_key
```

**Note**: The system uses mock data when API keys are not configured, so you can test basic functionality without all keys.

## 🧑‍💻 Development

### Adding New Tools

1. Create a new tool function in `src/langgraph_tool_backend.py`:
```python
@tool
def your_new_tool(param: str) -> str:
    """
    Description of your tool
    """
    # Your implementation
    return result
```

2. Add the tool to the tools list:
```python
tools = [..., your_new_tool]
```

3. Create tests in `tests/unit/test_your_tool.py`

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions
- Keep functions focused and modular

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Test Documentation

Detailed test documentation is available in:
- **Test Plan**: `docs/TEST_PLAN.md`
- **Test Cases**: `docs/TEST_CASES.md`

### Test Coverage Summary

| Module | Coverage | Tests |
|--------|----------|-------|
| Calculator Tool | 100% | 9 tests |
| Chat Flow | 85% | 6 tests |
| Overall | 90%+ | 15+ tests |

## 🐛 Known Issues

None at the moment. Report issues on GitHub!

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- UI powered by [Streamlit](https://streamlit.io/)
- LLM inference via [Groq](https://groq.com/)

## 📧 Contact

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/YOUR_USERNAME/langgraph-ai-chatbot](https://github.com/YOUR_USERNAME/langgraph-ai-chatbot)

---

⭐ **Star this repository if you find it helpful!** ⭐