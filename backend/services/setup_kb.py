# setup_large_enterprise_kb.py
import random
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in .env file!")

# Folder for documents
DOCS_PATH = Path("docs")
DOCS_PATH.mkdir(exist_ok=True)

# --- Enterprise document templates ---
TEMPLATES = [
    "Executive Summary:\n{summary}\n\nKey Metrics:\n{metrics}\n\nRecommendations:\n{recommendations}\n",
    "Project Report:\nProject: {project_name}\nStatus: {status}\nTasks Completed: {tasks_completed}\nPending Tasks: {tasks_pending}\nNotes: {notes}\n",
    "Policy Document:\nTitle: {policy_name}\nEffective Date: {date}\nPurpose: {purpose}\nScope: {scope}\nResponsibilities: {responsibilities}\n",
    "Meeting Minutes:\nDate: {date}\nAttendees: {attendees}\nDiscussion Points:\n{discussion_points}\nAction Items:\n{action_items}\n",
]

COMPANIES = ["Acme Corp", "Globex Inc", "Initech", "Umbrella Corp", "Cyberdyne Systems"]
PROJECTS = ["AI Integration", "Cloud Migration", "Data Pipeline Optimization", "Security Audit", "Compliance Review"]
POLICIES = ["Data Privacy Policy", "Acceptable Use Policy", "Remote Work Policy", "Information Security Policy"]
NAMES = ["Alice Smith", "Bob Johnson", "Carol Lee", "David Brown", "Eve Davis", "Frank Wilson", "Grace Miller", "Hank Thompson"]
STATUSES = ["On Track", "Delayed", "Completed", "Pending Review", "Under Analysis"]

def random_text(n_words=50):
    words = ["performance","report","analysis","strategy","implementation","evaluation",
             "system","team","project","deadline","deliverable","efficiency","optimization",
             "risk","security","compliance","management","stakeholders","objective","goal",
             "integration","automation","workflow","timeline","benchmark","review"]
    return " ".join(random.choices(words, k=n_words))

def generate_enterprise_docs(n=100):
    print(f"[INFO] Generating {n} enterprise-like documents...")
    for i in range(n):
        template = random.choice(TEMPLATES)
        content = template.format(
            summary=random_text(30),
            metrics=random_text(20),
            recommendations=random_text(25),
            project_name=random.choice(PROJECTS),
            status=random.choice(STATUSES),
            tasks_completed=random_text(15),
            tasks_pending=random_text(10),
            notes=random_text(15),
            policy_name=random.choice(POLICIES),
            date=f"{random.randint(2020,2026)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            purpose=random_text(20),
            scope=random_text(20),
            responsibilities=random_text(20),
            attendees=", ".join(random.sample(NAMES, k=3)),
            discussion_points=random_text(25),
            action_items=random_text(15)
        )
        file_path = DOCS_PATH / f"enterprise_doc_{i+1}.txt"
        file_path.write_text(content, encoding="utf-8")
    print(f"[INFO] Finished generating {n} documents.")

# Generate documents if docs folder is empty
if not any(DOCS_PATH.iterdir()):
    generate_enterprise_docs(n=120)

# --- Load documents ---
documents = []
for file in DOCS_PATH.glob("*.txt"):
    text = file.read_text(encoding="utf-8")
    documents.append(text)
print(f"[INFO] Loaded {len(documents)} documents.")

# --- Split documents into chunks ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs_chunks = text_splitter.split_text("\n\n".join(documents))
print(f"[INFO] Split into {len(docs_chunks)} chunks.")

# --- Create embeddings ---
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = FAISS.from_texts(docs_chunks, embeddings)
vectorstore_path = Path("enterprise_kb_large.faiss")
vectorstore.save_local(str(vectorstore_path))
print(f"[INFO] FAISS KB saved to {vectorstore_path}")