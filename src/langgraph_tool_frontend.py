# langgraph_tool_frontend.py
import streamlit as st
from langgraph_tool_backend import chatbot, get_threads, delete_thread
from langchain_core.messages import HumanMessage, AIMessage
import uuid
from login_manager import LoginManager

# Page configuration
st.set_page_config(
    page_title="AI Agent with Tools",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Login Manager
if "login_manager" not in st.session_state:
    st.session_state.login_manager = LoginManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("""
        <style>
        /* Cyberpunk Background */
        .stApp {
            background-color: #050510;
            background-image: 
                linear-gradient(rgba(0, 243, 255, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 243, 255, 0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: moveGrid 20s linear infinite;
        }

        @keyframes moveGrid {
            0% { background-position: 0 0; }
            100% { background-position: 50px 50px; }
        }

        /* Cyberpunk Card */
        .login-card {
            background: rgba(10, 25, 47, 0.85);
            border: 2px solid #00f3ff;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.4),
                        inset 0 0 20px rgba(0, 243, 255, 0.1);
            padding: 40px;
            text-align: center;
            position: relative;
            backdrop-filter: blur(5px);
            max-width: 450px;
            margin: auto;
            margin-top: 50px;
            overflow: hidden;
        }

        /* Tech Decoration Lines */
        .login-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, #00f3ff, transparent);
            animation: scanline 3s linear infinite;
        }

        @keyframes scanline {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Input Fields */
        .stTextInput > div > div > input {
            background: rgba(5, 5, 16, 0.8) !important;
            border: 1px solid #00f3ff !important;
            color: #00f3ff !important;
            font-family: 'Courier New', monospace !important;
            border-radius: 5px !important;
            padding: 12px 15px !important;
            box-shadow: inset 0 0 10px rgba(0, 243, 255, 0.1);
        }
        
        .stTextInput > div > div > input:focus {
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.3) !important;
            background: rgba(5, 5, 16, 1) !important;
        }

        /* Login Button */
        .stButton > button {
            background: transparent !important;
            border: 2px solid #00f3ff !important;
            color: #00f3ff !important;
            border-radius: 5px !important;
            font-family: 'Arial', sans-serif !important;
            font-weight: bold !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            width: 100%;
        }

        .stButton > button:hover {
            background: #00f3ff !important;
            color: #000 !important;
            box-shadow: 0 0 30px #00f3ff;
        }

        /* Text Styling */
        h1 {
            color: #fff !important;
            text-shadow: 0 0 10px #00f3ff;
            font-family: 'Arial Black', sans-serif;
            letter-spacing: 2px;
            margin-bottom: 5px !important;
        }
        
        caption, p {
            color: #8892b0 !important;
            font-family: 'Courier New', monospace;
        }

        /* Hide Sidebar */
        div[data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1>SYSTEM ACCESS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.8em; margin-bottom: 20px;'>SECURE CONNECTION // REQUIRED</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            # Using icons in placeholder to simulate the design
            username = st.text_input("Username", placeholder="👤 IDENTIFIER", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="🔒 SECURITY KEY", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("INITIALIZE LINK")
            
            if submit:
                if st.session_state.login_manager.login(username, password):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("⛔ ACCESS DENIED: INVALID CREDENTIALS")
        
        st.markdown('</div>', unsafe_allow_html=True)


if not st.session_state.logged_in:
    login_page()
else:
    # Initialize session state
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []

    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        },
        "recursion_limit": 50  # Increased limit as safety net
    }

    # ========================= SIDEBAR =========================
    with st.sidebar:
        st.title("🤖 AI Assistant")
        
        if st.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.markdown("---")
        
        # New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.thread_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💬 Chat History")
        
        # Display thread history
        threads = get_threads()
        if threads:
            for thread in reversed(threads[-15:]):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"🔹 {thread[:12]}...",
                        key=f"thread_{thread}",
                        use_container_width=True,
                        disabled=(thread == st.session_state.thread_id)
                    ):
                        st.session_state.thread_id = thread
                        st.session_state.messages = []
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{thread}"):
                        delete_thread(thread)
                        if thread == st.session_state.thread_id:
                            st.session_state.thread_id = str(uuid.uuid4())
                            st.session_state.messages = []
                        st.rerun()
        else:
            st.info("No chat history")
        
        st.markdown("---")
        st.markdown("### 🛠️ Available Tools")
        tools_list = [
            " Web Search",
            "🧮 Calculator",
            "🌤️ Weather",
            "📈 Stock Price",
            "💱 Currency Convert",
            "📰 News",
            "😂 Jokes",
            "🌌 NASA APOD",
            "🌐 IP Location"
        ]
        for tool in tools_list:
            st.markdown(f"• {tool}")
        
        st.markdown("---")
        st.info("💡 **Try these:**\n- hi / hello\n- calculate 25 + 37\n- weather in london\n- AAPL stock price\n- convert 100 USD to EUR\n- tech news\n- tell me a joke\n- nasa picture\n- search for python")

    # ========================= MAIN =========================
    st.title("✨ AI Assistant with Tools")
    st.caption("Chat with AI - Tools work automatically! Try asking for a joke, weather, stock prices, and more!")

    # Load existing messages from checkpoint
    if not st.session_state.messages:
        try:
            state = chatbot.get_state(config)
            if state and state.values and "messages" in state.values:
                msgs = state.values["messages"]
                # Filter to only user and assistant messages with content
                st.session_state.messages = []
                for m in msgs:
                    if isinstance(m, HumanMessage):
                        st.session_state.messages.append(m)
                    elif isinstance(m, AIMessage) and m.content:
                        st.session_state.messages.append(m)
        except Exception as e:
            print(f"Error loading messages: {e}")
            st.session_state.messages = []

    # Display chat messages
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage) and msg.content:
            with st.chat_message("assistant"):
                st.write(msg.content)

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        # Add user message
        user_msg = HumanMessage(content=user_input)
        st.session_state.messages.append(user_msg)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            tool_status_placeholder = st.empty()
            # Clear any previous tool status
            tool_status_placeholder.empty()
            
            try:
                # Show immediate feedback
                response_placeholder.info("🤔 Thinking...")
                
                # Invoke the chatbot with timeout
                result = chatbot.invoke(
                    {"messages": st.session_state.messages},
                    config=config
                )
                
                # Extract the final response
                if result and "messages" in result:
                    messages = result["messages"]
                    
                    # Show tools used only from the latest AI message
                    tool_calls_made = []
                    # Find the last AIMessage that may contain tool calls
                    for msg in reversed(messages):
                        # STOP scanning if we hit the user's message
                        if isinstance(msg, HumanMessage):
                            break
                            
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            for tool_call in msg.tool_calls:
                                tool_name = tool_call.get('name', 'unknown')
                                tool_calls_made.append(tool_name)
                            # We keep going until we hit the HumanMessage to catch ALL tool calls in the chain
                    
                    # Display tool calls if any were made
                    if tool_calls_made:
                        tool_icons = {
                            'search_tool': '🔍',
                            'calculator_tool': '🧮',
                            'fetch_weather': '🌤️',
                            'get_stock_price': '📈',
                            'convert_currency': '💱',
                            'fetch_news': '📰',
                            'get_joke': '😂',
                            'get_nasa_apod': '🌌',
                            'get_ip_location': '🌐'
                        }
                        
                        tool_display_names = {
                            'search_tool': 'Web Search',
                            'calculator_tool': 'Calculator',
                            'fetch_weather': 'Weather',
                            'get_stock_price': 'Stock Price',
                            'convert_currency': 'Currency Converter',
                            'fetch_news': 'News',
                            'get_joke': 'Joke',
                            'get_nasa_apod': 'NASA APOD',
                            'get_ip_location': 'IP Location'
                        }
                        
                        # Remove duplicates while preserving order
                        unique_tools = list(dict.fromkeys(tool_calls_made))
                        tools_text = ", ".join([
                            f"{tool_icons.get(tool, '🔧')} **{tool_display_names.get(tool, tool)}**"
                            for tool in unique_tools
                        ])
                        tool_status_placeholder.success(f"🔧 **Tools Used:** {tools_text}")
                    
                    # Find the last AI message with content
                    ai_response = None
                    for msg in reversed(messages):
                        if isinstance(msg, AIMessage) and msg.content:
                            ai_response = msg.content
                            break
                    
                    if ai_response:
                        response_placeholder.write(ai_response)
                        st.session_state.messages.append(AIMessage(content=ai_response))
                    else:
                        response_placeholder.warning("⚠️ No response generated. Please try again.")
                else:
                    response_placeholder.error("❌ Failed to get response from agent.")
                        
            except Exception as e:
                error_msg = str(e)
                
                # Check for specific errors
                if "recursion" in error_msg.lower():
                    response_placeholder.error("❌ The agent got stuck in a loop. Starting fresh conversation...")
                    st.info("💡 Try rephrasing your question or start a new chat.")
                    # Reset on recursion error
                    st.session_state.thread_id = str(uuid.uuid4())
                    st.session_state.messages = []
                elif "api" in error_msg.lower() or "key" in error_msg.lower():
                    response_placeholder.error(f"❌ API Error: {error_msg}")
                    st.info("💡 Make sure your GROQ_API_KEY is set correctly in the .env file")
                else:
                    response_placeholder.error(f"❌ Error: {error_msg}")
                    st.info("💡 Try starting a new chat or rephrasing your message")

    # Footer
    st.markdown("---")
    st.caption(f"🔖 Thread ID: {st.session_state.thread_id[:16]}...")
