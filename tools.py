import requests 
from llm import ARAA_SEARCH_URL 
from langchain_core.tools import tool
from bs4 import BeautifulSoup
import time 
from llm import VLLM_URL, VLLM_API_KEY, VLLM_MODEL


@tool
def araa_search(query: str) -> str:
    """Search using Araa-Search engine"""
    try:
        # Araa-Search API (adjust endpoint if different)
        resp = requests.post(
            f"{ARAA_SEARCH_URL}/search",  # Common Araa endpoint
            json={"query": query, "num_results": 8},
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        data = resp.json()
        
        # Handle common Araa response formats
        results = data.get("results") or data.get("data") or data.get("search_results", [])
        
        formatted = "ARAA-SEARCH RESULTS:\n\n"
        for i, result in enumerate(results[:6], 1):
            title = result.get("title") or result.get("name", "No title")
            url = result.get("url") or result.get("link", "")
            snippet = result.get("snippet") or result.get("description", "")[:180]
            
            formatted += f"{i}. **{title}**\n"
            formatted += f"   {url}\n"
            formatted += f"   {snippet}...\n\n"
        return formatted
        
    except Exception as e:
        # Fallback GET if POST fails
        try:
            resp = requests.get(f"{ARAA_SEARCH_URL}/search", params={"q": query}, timeout=12)
            data = resp.json()
            results = data.get("results", [])
            return "\n".join([f"{i}. {r.get('title')} ({r.get('url')})\n{r.get('snippet', '')[:150]}..."
                            for i, r in enumerate(results[:5])])
        except:
            return f"Araa-Search error: {str(e)}"

@tool
def get_content(urls: list[str]) -> str:
    """Fetch webpage content"""
    content = ""
    for url in urls[:3]:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            for tag in soup(["script", "style"]): tag.decompose()
            text = re.sub(r'\s+', ' ', soup.get_text(strip=True))[:2200]
            title = soup.title.string or url.split("/")[-1]
            content += f"\n## {title}\n\n{text[:450]}...\n\n"
            time.sleep(0.4)
        except: continue
    return content or "No content retrieved"

@tool
def summarize_content(text: str, query: str) -> str:
    """VLLM summarization"""
    from openai import OpenAI
    client = OpenAI(base_url=VLLM_URL, api_key=VLLM_API_KEY)
    resp = client.chat.completions.create(
        model=VLLM_MODEL,
        messages=[{"role": "user", "content": f"Query: '{query}'\n\nSummarize:\n\n{text[:3800]}" }],
        temperature=0.3, max_tokens=1000
    )
    return resp.choices[0].message.content.strip()

tools = [araa_search, get_content, summarize_content]  # Changed tool name
print("✅ Araa-Search tools ready")
