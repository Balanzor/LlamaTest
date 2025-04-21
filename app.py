
import streamlit as st
from groq import Groq
import time
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="🤖 Llama Scout Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for a more attractive design
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .app-header {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-left: 5px solid #4b6fff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat container */
    .chat-container {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #333333;
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background-color: #e1f0ff;
        border-left: 4px solid #2e86de;
        margin-left: 2rem;
        margin-right: 0.5rem;
    }
    
    .assistant-message {
        background-color: #f0f0f0;
        border-left: 4px solid #6c757d;
        margin-right: 2rem;
        margin-left: 0.5rem;
    }
    
    /* Input area styling */
    .input-area {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4b6fff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #3a5ae8;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.7rem;
        color: #888;
        text-align: right;
        margin-top: 0.3rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        font-size: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #eaeaea;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
client = Groq(
    api_key="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",
)

# System prompt to improve model responses
SYSTEM_PROMPT = """You are Llama Scout, an advanced AI assistant powered by Llama 3.3 70B.
Your responses should be:
1. Accurate and factual
2. Helpful and informative
3. Clear and well-structured
4. Concise but comprehensive

When you don't know something, admit it rather than making up information.
Format your responses with appropriate markdown for readability.
"""

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

# Header with custom styling
st.markdown('<div class="app-header">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://img.icons8.com/fluency/96/bot.png", width=80)
with col2:
    st.title("Llama Scout AI Assistant")
    st.markdown("Your intelligent companion powered by Llama 3.3 70B")
st.markdown('</div>', unsafe_allow_html=True)

# Create a two-column layout
col1, col2 = st.columns([3, 1])

with col2:  # Sidebar content moved to right column
    st.markdown("### ⚙️ Settings")
    
    temperature = st.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.7, 
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    
    max_tokens = st.slider(
        "Max Tokens", 
        min_value=100, 
        max_value=4000, 
        value=1000, 
        step=100,
        help="Maximum length of the model's response"
    )
    
    st.markdown("### 🔍 Model Information")
    st.markdown("""
    - **Model**: llama-3.3-70b-versatile
    - **Provider**: Groq
    - **Capabilities**: 
        - Natural conversations
        - Knowledge through 2023
        - Code assistance
        - Creative writing
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.session_state.chat_started = False
        st.rerun()

with col1:  # Main chat area
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Welcome message if chat hasn't started
    if not st.session_state.chat_started:
        st.markdown("""
        <div class="chat-message assistant-message">
            <strong>🤖 Llama Scout:</strong> 
            <p>Hello! I'm Llama Scout, your AI assistant powered by Llama 3.3 70B. How can I help you today?</p>
            <div class="timestamp">Today, just now</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    display_messages = [msg for msg in st.session_state.messages if msg["role"] != "system"]
    for message in display_messages:
        timestamp = datetime.now().strftime("%I:%M %p")
        
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> 
                <p>{message['content']}</p>
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Llama Scout:</strong> 
                <p>{message['content']}</p>
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with custom styling
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    user_input = st.text_input(
        "",
        key="user_input",
        placeholder="Type your message here and press Enter...",
    )
    
    # Add buttons for quick prompts
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Help me write"):
            user_input = "Can you help me write a professional email?"
    with col2:
        if st.button("💡 Explain a concept"):
            user_input = "Explain machine learning in simple terms."
    with col3:
        if st.button("🧠 Creative ideas"):
            user_input = "Give me 5 creative project ideas using AI."
    
    st.markdown('</div>', unsafe_allow_html=True)

# Process user input
if user_input:
    # Set chat as started
    st.session_state.chat_started = True
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show typing indicator
    with st.spinner("Llama Scout is thinking..."):
        try:
            # Get response from Groq with improved parameters
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="llama-3.3-70b-versatile",
                temperature=temperature,  # Use the slider value
                max_tokens=max_tokens,    # Use the slider value
                top_p=0.9,                # Added parameter for better response quality
                frequency_penalty=0.2,    # Reduces repetition
                presence_penalty=0.1,     # Encourages topic diversity
            )

            # Get the assistant's response
            assistant_response = chat_completion.choices[0].message.content

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Rerun to update the chat display
            st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("*Powered by Groq & Llama 3.3 70B Versatile • Created with Streamlit*")
st.markdown("© 2023 Llama Scout AI Assistant")
st.markdown('</div>', unsafe_allow_html=True)
