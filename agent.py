# Cell 3: COMPLETE FUNCTION CALLING AGENT (Zero parsing errors)
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from llm import VLLM_URL, VLLM_API_KEY, VLLM_MODEL
from langchain_openai import ChatOpenAI
from tools import tools

# 1. FULL TOOLS DEFINITION
tools_openai = [
    {
        "type": "function",
        "function": {
            "name": "araa_search",
            "description": "Search current web information using Araa-Search",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "get_content",
            "description": "Fetch full content from URLs",
            "parameters": {
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of URLs"
                    }
                },
                "required": ["urls"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_content",
            "description": "Summarize text content for a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to summarize"},
                    "query": {"type": "string", "description": "Original query"}
                },
                "required": ["text", "query"]
            }
        }
    }
]

# 2. FIXED LLM (Correct params for vLLM)
llm = ChatOpenAI(
    model=VLLM_MODEL,
    temperature=0.1,
    openai_api_key=VLLM_API_KEY,  # Fixed param name
    openai_api_base=VLLM_URL
)

# 3. Bind tools
llm_func = llm.bind_tools(tools_openai)

# 4. Simple prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """Research assistant with web tools.
    
Use araa_search for current info, get_content for details, summarize_content for final answer.
    
Respond naturally - tools auto-trigger."""),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# 5. Create agent executor
from langchain_classic.agents import AgentExecutor,create_tool_calling_agent
agent = create_tool_calling_agent(llm_func, tools_openai, prompt)  # Your tools list
FUNC_AGENT = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("✅ Complete function calling agent ready!")
print("FUNC_AGENT.invoke({'input': 'query'})")
