import os
from dotenv import load_dotenv
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Import our custom logic modules
from persona_detector import update_persona, get_persona
from checklist_manager import generate_checklist_for_persona, mark_task_completed, get_checklist
from rag_engine import query_knowledge_base

# Load environment variables
load_dotenv()

# In-memory chat history
chat_histories = {}

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY is not set.")
        
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
except Exception as e:
    print(f"Failed to initialize LLM: {e}")
    llm = None

def get_system_prompt(session_id: str):
    persona = get_persona(session_id)
    checklist = get_checklist(session_id)
    
    prompt = f"""You are the friendly Autonomous Developer Onboarding Agent.

CURRENT CONTEXT
User Persona Data Found So Far:
Name: {persona.name or 'Unknown'}
Role: {persona.role or 'Unknown'}
Experience: {persona.experience or 'Unknown'}
Tech Stack: {persona.tech_stack or 'Unknown'}

"""
    if not persona.is_complete():
        prompt += """\nYour current goal is to naturaly ask questions to fill in any 'Unknown' fields above.
Once you have them all, tell the user you are generating their checklist, AND call the `generate_checklist` Tool. Do not stop asking until all 4 fields are collected."""
    else:
        prompt += "\nThe user profile is complete!"
        if not checklist:
            prompt += "\nCALL the `generate_checklist` Tool right now to create their tasks."
        else:
            task_str = json.dumps(checklist, indent=2)
            prompt += f"\nHere is their checklist:\n{task_str}\n\nYour goal is to help them complete these tasks. When they claim to finish one, CALL the `mark_task_completed` tool."
            
    prompt += "\n\nIf the user asks a question about company policy, repo setup, etc., USE the `query_knowledge_base` tool to search the docs before answering."
    return SystemMessage(content=prompt)

# Define python functions that the LLM can use as Tools
from langchain.tools import tool

@tool
def update_user_persona(name: str = "", role: str = "", experience: str = "", tech_stack: str = "") -> str:
    """Use this to save persona details when the user tells you about themselves."""
    # We cheat a little by using a global hack for session_id in this context
    # In production, pass it explicitly.
    global current_session_id
    update_persona(current_session_id, {"name": name, "role": role, "experience": experience, "tech_stack": tech_stack})
    return "Persona updated successfully in DB."

@tool
def generate_checklist() -> str:
    """Use this to generate the onboarding checklist AFTER the persona is 100% complete."""
    global current_session_id
    persona = get_persona(current_session_id)
    if not persona.is_complete():
        return "Failed: Need full persona first."
        
    tasks = generate_checklist_for_persona(current_session_id, persona.role, persona.experience, persona.tech_stack)
    return f"Checklist generated with {len(tasks)} tasks."

@tool
def mark_task_done(task_id: int) -> str:
    """Use this to check off a task when the user completes it. Pass the exact task integer ID."""
    global current_session_id
    persona = get_persona(current_session_id)
    return mark_task_completed(current_session_id, task_id, persona)

@tool
def search_company_docs(query: str) -> str:
    """Use this tool to search company documentation for answers."""
    return query_knowledge_base(query)

# Bind tools to LLM
tools = [update_user_persona, generate_checklist, mark_task_done, search_company_docs]
if llm:
    llm_with_tools = llm.bind_tools(tools)

current_session_id = None

def chat_with_agent(user_message: str, session_id: str) -> str:
    """Handles conversational loop with LangChain tool calling."""
    if not llm:
        return "Error: LLM not initialized (missing API Key)."
        
    global current_session_id
    current_session_id = session_id
    
    if session_id not in chat_histories:
        chat_histories[session_id] = []
        
    # Always inject the latest dynamic system prompt
    sys_prompt = get_system_prompt(session_id)
    
    messages = [sys_prompt] + chat_histories[session_id]
    messages.append(HumanMessage(content=user_message))
    
    try:
        response = llm_with_tools.invoke(messages)
        
        # Check if the LLM decided to call a tool
        if response.tool_calls:
            messages.append(AIMessage(content="", tool_calls=response.tool_calls))
            
            # Execute all requested tools
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                args = tool_call["args"]
                
                tool_result = ""
                if tool_name == "update_user_persona":
                    tool_result = update_user_persona.invoke(args)
                elif tool_name == "generate_checklist":
                    tool_result = generate_checklist.invoke(args)
                elif tool_name == "mark_task_done":
                    tool_result = mark_task_done.invoke(args)
                elif tool_name == "search_company_docs":
                    tool_result = search_company_docs.invoke(args)
                    
                from langchain.schema import ToolMessage
                messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
                
            # Second LLM call to summarize the tool response
            final_response = llm_with_tools.invoke(messages)
            chat_histories[session_id].append(HumanMessage(content=user_message))
            chat_histories[session_id].append(AIMessage(content=final_response.content))
            return final_response.content
        else:
            # Normal conversational response
            chat_histories[session_id].append(HumanMessage(content=user_message))
            chat_histories[session_id].append(AIMessage(content=response.content))
            return response.content
            
    except Exception as e:
        return f"Error with LLM execution: {str(e)}"

SYSTEM_PROMPT = """
You are an expert Autonomous Developer Onboarding Agent.
Your job is to act as a friendly HR representative and technical guide to seamlessly integrate new developers into the company's workflow.

Right now, your goals are to:
1. Welcome the user.
2. Ask questions to determine their: Name, Role, Experience Level, and Tech Stack.
"""

def chat_with_agent(user_message: str, session_id: str) -> str:
    """
    Handles the conversation loop with the LLM, managing message history.
    """
    if not llm:
        return "Error: LLM not initialized. Please ensure your GEMINI_API_KEY is set in backend/.env."

    # Initialize history for new sessions
    if session_id not in chat_histories:
        chat_histories[session_id] = [SystemMessage(content=SYSTEM_PROMPT)]
    
    # Append the user's message
    chat_histories[session_id].append(HumanMessage(content=user_message))
    
    try:
        # Call the LLM
        response = llm.invoke(chat_histories[session_id])
        
        # Append AI's response to the history so it remembers the context
        chat_histories[session_id].append(AIMessage(content=response.content))
        
        return response.content
    except Exception as e:
        return f"Error communicating with the LLM: {str(e)}"
