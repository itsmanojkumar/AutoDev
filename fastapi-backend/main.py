# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import re

from crewai import LLM, Agent, Crew, Task

# ==========================
# 🚀 Initialization
# ==========================
load_dotenv()
logging.basicConfig(level=logging.INFO)

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")

if not HF_TOKEN:
    raise ValueError("❌ Hugging Face API token missing. Please set HF_TOKEN in your .env file.")

# ==========================
# 🌍 FastAPI Setup
# ==========================
app = FastAPI(title="AI Web Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# 📦 Pydantic Model
# ==========================
class GenerateRequest(BaseModel):
    prompt: str

# ==========================
# 🧹 Helper Function
# ==========================
def cleanup_code_block(text: str) -> str:
    """Remove markdown, imports, and explanations from AI output."""
    if not text:
        return "() => (<div>No code generated</div>)"

    # Remove code fences and markdown junk
    text = re.sub(r"```(?:jsx|js|javascript|tsx|python)?", "", text)
    text = text.replace("```", "")

    # Remove imports, exports, and explanations
    text = re.sub(r"import\s+.*?;?", "", text)
    text = re.sub(r"export\s+default\s+.*", "", text)
    text = re.sub(r"Please\s+note[\s\S]*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^.*?(?=\(\s*=>)", "", text, flags=re.DOTALL)

    return text.strip()

# ==========================
# 🧠 LLM Setup
# ==========================
try:
    llm = LLM(
        model=f"huggingface/{HF_MODEL}",
        api_key=HF_TOKEN,
        temperature=0.7,
        max_tokens=512,
        verbose=True,
        stream=True
    )
    logging.info(f"✅ LLM initialized with model: {HF_MODEL}")
except Exception as e:
    logging.error(f"❌ Error initializing LLM: {e}")
    raise RuntimeError("Failed to initialize LLM. Ensure LiteLLM and Hugging Face token are valid.")

# ==========================
# 👨‍💻 Agents
# ==========================
frontend_agent = Agent(
    role="Senior Next.js frontend developer",
    goal="Generate clean React components based on UI prompts",
    backstory="10 years of experience in building production-grade frontend apps with Next.js and React.",
    llm=llm
)

backend_agent = Agent(
    role="Senior backend developer",
    goal="Generate minimal FastAPI endpoints supporting the frontend UI",
    backstory="10 years of experience building scalable APIs and databases using FastAPI and PostgreSQL.",
    llm=llm
)

# ==========================
# 🎯 Route: /api/generate-ui
# ==========================
@app.post("/api/generate-ui")
async def generate_ui(request: GenerateRequest):
    logging.info(f"🧩 Received UI generation request: {request.prompt}")

    frontend_prompt = (
        "You are a senior React UI developer.\n"
        "Given a UI description, generate a FULL React functional component "
        "that can run directly inside react-live.\n"
        "Rules:\n"
        "- Output ONLY valid React component code starting with: () => {...}\n"
        "- NO imports, exports, or markdown.\n"
        "- NO explanations or commentary.\n"
        "- Use React.useState for state when needed."
    )

    backend_prompt = (
        "You are a senior backend engineer.\n"
        "Given the frontend component and its purpose, generate a minimal FastAPI endpoint "
        "that supports its functionality. Output only the API code, no explanations."
    )

    try:
        # 🧠 Define tasks
        task_frontend = Task(
            description=f"Frontend component for: {request.prompt}",
            expected_output=frontend_prompt,
            agent=frontend_agent
        )
        task_backend = Task(
            description="Create a backend API to support the above frontend functionality.",
            expected_output=backend_prompt,
            agent=backend_agent
        )

        crew = Crew(agents=[frontend_agent, backend_agent], tasks=[task_frontend, task_backend])
        result = crew.kickoff()

        # ✅ Safe extractor for any CrewAI version
        def extract_task_output(task_result):
            for attr in ["output", "raw_output", "final_output", "result"]:
                if hasattr(task_result, attr):
                    value = getattr(task_result, attr)
                    if isinstance(value, dict):
                        return value.get("content", str(value))
                    return str(value)
            return str(task_result)

        frontend_code = cleanup_code_block(extract_task_output(result.tasks_output[0]))
        backend_code = cleanup_code_block(extract_task_output(result.tasks_output[1]))

        files = {
            "src/pages/index.tsx": frontend_code,
            "backend/main.py": backend_code,
        }

        return {"files": files}

    except Exception as e:
        logging.error(f"❌ Error generating code: {e}")
        return {
            "files": {
                "src/pages/index.tsx": "() => (<div>Error generating UI</div>)",
                "backend/main.py": "# Error generating backend"
            }
        }
