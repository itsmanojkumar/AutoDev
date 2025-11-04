# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import re

from crewai import LLM, Agent, Crew, Task  # ✅ Added Crew and Task imports

load_dotenv()
logging.basicConfig(level=logging.INFO)

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Hugging Face API token missing. Set HF_TOKEN in your .env")

MODEL_NAME = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

def cleanup_code_block(text: str) -> str:
    """Strip markdown, imports, exports, and commentary."""
    if not text:
        return "() => (<div>No code generated</div>)"

    # Remove markdown code fences
    text = re.sub(r"```(?:jsx|js|javascript)?", "", text)
    text = text.replace("```", "")

    # Remove import/export lines
    text = re.sub(r"^.*?(?=\(\s*=>)", "", text, flags=re.DOTALL)
    text = re.sub(r"import\s+.*?;?", "", text)
    text = re.sub(r"export\s+default\s+.*", "", text)

    # Remove trailing explanations
    text = re.sub(r"Please\s+note[\s\S]*$", "", text, flags=re.IGNORECASE)

    # Trim whitespace
    return text.strip()

# Initialize global LLM
llm = LLM(
    model=f"huggingface/meta-llama/Llama-3.1-8B-Instruct",
    stream=True,
    api_key=HF_TOKEN
)

# Initialize a senior frontend dev agent
dev_agent = Agent(
    role="Senior Next.js frontend developer",
    goal="Write and debug React code based on UI prompts",
    backstory="Expert frontend engineer with 10 years of experience",
    max_execution_time=300,
    max_retry_limit=3,
    llm=llm
)   

backend_agent = Agent(
    role="Senior backend developer with expertise in rest APIs/graphql and databases",
    goal="Write and debug backend code based on frotend UI",
    backstory="Expert backend engineer with 10 years of experience",
    max_execution_time=300,
    max_retry_limit=3,
    llm=llm,
    
)   


@app.post("/api/generate-ui")
async def generate_ui(request: GenerateRequest):
    """
    Generate a React functional component runnable inside react-live.
    Returns JSON: { "code": "<component code>" }
    """
    system_prompt = (
        "You are an expert senior React UI engineer.\n"
        "Given a UI description, generate a FULL React functional component runnable inside react-live.\n\n"
        "STRICT RULES:\n"
        "- Output ONLY the component code starting with: () => { ... }\n"
        "- NO imports, NO exports.\n"
        "- NO markdown.\n"
        "- NO explanations, NO commentary, NO descriptions.\n"
        "- Use React.useState if state is needed.\n"
        "- The output MUST be valid React code runnable by react-live.\n"
        "- Output nothing else.\n"
    )

    user_prompt = (
        f'Given this UI description: "{request.prompt}"\n\n'
        "Return ONLY the component code that follows the rules above."
    )

    try:
        # ✅ Define a CrewAI task
        task1 = Task(
            description=user_prompt,
            expected_output=system_prompt,
            agent=dev_agent
        )
        task2 = Task(
            description="Based on the frontend component generated, create a suitable backend API to support it.",
            expected_output="A backend API code snippet that supports the frontend component.",
            agent=backend_agent
        )

        # ✅ Create and run a CrewAI crew (runs the agent + task)
        crew = Crew(agents=[dev_agent], tasks=[task1])
        backend_output = Crew(agents=[backend_agent], tasks=[task2])
        result = crew.kickoff()
        backend_result = backend_output.kickoff()
        print(backend_result)
        print(result)

        # ✅ Cleanup output
        code = cleanup_code_block(result.output if hasattr(result, "output") else str(result))
        return {
            "code": code,
            "backend_code": str(backend_result)
            }

    except Exception as e:
        logging.error(f"Error generating UI: {e}")
        return {"code": "() => (<div>Error generating UI</div>)"}
