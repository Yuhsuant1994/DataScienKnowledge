import os
import time
from typing import Dict, List

import requests
import streamlit as st

# Configure the page
st.set_page_config(page_title="AI Search Chatbot", page_icon="🤖", layout="wide")

# API endpoint (use environment variable if available, otherwise localhost)
API_URL = os.getenv("API_URL", "http://localhost:8001/api/search_graph")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "tool_references" not in st.session_state:
    st.session_state.tool_references = []

if "response_times" not in st.session_state:
    st.session_state.response_times = []

# Sidebar with model information
with st.sidebar:
    st.title("⚙️ Configuration")

    st.subheader("🤖 LLM Model")
    st.info("**Model:** qwen/qwen3-32b")
    st.write("**Provider:** Groq")

    st.subheader("🔧 Available Tools")
    st.markdown(
        """
    - **📚 ArXiv** - Query academic papers
    - **📖 Wikipedia** - Query Wikipedia articles
    - **🔍 Tavily Search** - Web search for current info
    """
    )

    st.subheader("API Settings")
    api_url = st.text_input("API Endpoint", value=API_URL)

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.tool_references = []
        st.session_state.response_times = []
        st.rerun()

# Main chat interface
st.title("AI Search Chatbot")
st.markdown("Ask me anything! I can search ArXiv papers, Wikipedia, and the web.")

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display tool references and response time if available
        if message["role"] == "assistant" and idx < len(
            st.session_state.tool_references
        ):
            # Display response time
            if idx < len(st.session_state.response_times):
                response_time = st.session_state.response_times[idx]
                st.caption(f"⏱️ Response time: {response_time:.2f}s")

            tools = st.session_state.tool_references[idx]
            if tools:
                with st.expander("📚 References & Tools Used", expanded=False):
                    for i, tool in enumerate(tools, 1):
                        tool_name = tool.get("tool", "Unknown")
                        query = tool.get("ai_gen_query", "")

                        # Format tool name with icons
                        tool_icon = {
                            "arxiv": "📚",
                            "wikipedia": "📖",
                            "tavily_search_results_json": "🔍",
                        }.get(tool_name, "🔧")

                        st.markdown(
                            f"**{i}. {tool_icon} {tool_name.replace('_', ' ').title()}**"
                        )
                        if query:
                            st.code(query, language=None)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Start timer
                start_time = time.time()

                # Make API request
                response = requests.post(api_url, params={"query": prompt}, timeout=60)
                response.raise_for_status()
                data = response.json()

                # Calculate response time
                end_time = time.time()
                response_time = end_time - start_time

                # Extract response and tools
                assistant_response = data.get(
                    "response", "I couldn't generate a response."
                )
                tools_used = data.get("tools", [])

                # Display response
                st.markdown(assistant_response)

                # Display response time
                st.caption(f"⏱️ Response time: {response_time:.2f}s")

                # Display tool references
                if tools_used:
                    with st.expander("📚 References & Tools Used", expanded=True):
                        for i, tool in enumerate(tools_used, 1):
                            tool_name = tool.get("tool", "Unknown")
                            query = tool.get("ai_gen_query", "")

                            # Format tool name with icons
                            tool_icon = {
                                "arxiv": "📚",
                                "wikipedia": "📖",
                                "tavily_search_results_json": "🔍",
                            }.get(tool_name, "🔧")

                            st.markdown(
                                f"**{i}. {tool_icon} {tool_name.replace('_', ' ').title()}**"
                            )
                            if query:
                                st.code(query, language=None)

                # Add assistant message to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )
                st.session_state.tool_references.append(tools_used)
                st.session_state.response_times.append(response_time)

            except requests.exceptions.RequestException as e:
                error_message = f"❌ Error connecting to API: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )
                st.session_state.tool_references.append([])
                st.session_state.response_times.append(0)
            except Exception as e:
                error_message = f"❌ An error occurred: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )
                st.session_state.tool_references.append([])
                st.session_state.response_times.append(0)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>AI gen UI to test LangGraph app</p>
    </div>
    """,
    unsafe_allow_html=True,
)
