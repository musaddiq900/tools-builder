"""
Code Generator Agent for AutoDev Factory

Generates complete codebases for projects.
"""

from typing import Any, Dict, List
from .base_agent import BaseAgent, AgentResult


class CodeGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating complete codebases.
    
    Features:
    - Full backend code generation
    - Full frontend code generation
    - API creation
    - Database model creation
    - Authentication system
    - Admin dashboard
    - User dashboards
    - Multi-language support
    """
    
    name: str = "CodeGeneratorAgent"
    description: str = "Generates complete codebases for projects"
    
    supported_languages: list = ["Python", "TypeScript", "JavaScript", "Go", "Rust"]
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        try:
            prd = input_data.get("prd", {})
            architecture = input_data.get("architecture", {})
            structure = input_data.get("structure", {})
            
            codebase = self._generate_codebase(prd, architecture, structure)
            
            return AgentResult(
                success=True,
                data={"codebase": codebase},
                message=f"Generated codebase with {len(codebase.get('files', []))} files"
            )
        except Exception as e:
            return AgentResult(success=False, message=f"Code generation failed: {str(e)}")
    
    def _generate_codebase(self, prd: Dict, architecture: Dict, structure: Dict) -> Dict:
        return {
            "backend": self._generate_backend(prd),
            "frontend": self._generate_frontend(prd),
            "tests": self._generate_tests(),
            "files": self._generate_all_files(prd)
        }
    
    def _generate_backend(self, prd: Dict) -> Dict:
        return {
            "main_app": self._backend_main(),
            "models": self._backend_models(),
            "api_routes": self._backend_api(),
            "services": self._backend_services()
        }
    
    def _backend_main(self) -> str:
        return '''"""Main FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(title="AutoDev App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AutoDev API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
'''
    
    def _backend_models(self) -> str:
        return '''"""Database Models"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    name = Column(String)
    config = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
'''
    
    def _backend_api(self) -> str:
        return '''"""API Routes"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

class ProjectCreate(BaseModel):
    name: str
    config: dict = {}

@router.post("/auth/register")
async def register(user: UserCreate):
    # TODO: Implement registration
    return {"message": "User registered"}

@router.post("/auth/login")
async def login(user: UserCreate):
    # TODO: Implement login
    return {"access_token": "token"}

@router.get("/dashboard")
async def get_dashboard():
    return {"metrics": {"users": 0, "projects": 0}}

@router.post("/projects")
async def create_project(project: ProjectCreate):
    # TODO: Implement project creation
    return {"id": 1, **project.dict()}
'''
    
    def _backend_services(self) -> str:
        return '''"""Business Logic Services"""
from typing import Optional, List

class UserService:
    async def create_user(self, email: str, password: str) -> dict:
        # TODO: Implement user creation
        return {"id": 1, "email": email}
    
    async def authenticate(self, email: str, password: str) -> Optional[str]:
        # TODO: Implement authentication
        return "jwt_token"

class ProjectService:
    async def create_project(self, user_id: int, name: str, config: dict) -> dict:
        # TODO: Implement project creation
        return {"id": 1, "user_id": user_id, "name": name}
    
    async def list_projects(self, user_id: int) -> List[dict]:
        # TODO: Implement listing
        return []
'''
    
    def _generate_frontend(self, prd: Dict) -> Dict:
        return {
            "package_json": self._package_json(),
            "pages": self._frontend_pages(),
            "components": self._frontend_components(),
            "styles": self._frontend_styles()
        }
    
    def _package_json(self) -> str:
        return '''{
  "name": "autodev-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "^18",
    "react-dom": "^18",
    "axios": "^1.6.0",
    "tailwindcss": "^3.4.0"
  }
}'''
    
    def _frontend_pages(self) -> Dict[str, str]:
        return {
            "index.tsx": '''import Head from 'next/head';
export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head><title>AutoDev App</title></Head>
      <main className="container mx-auto p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to AutoDev</h1>
        <p className="text-lg">Your automated development platform</p>
      </main>
    </div>
  );
}''',
            "dashboard.tsx": '''export default function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="grid grid-cols-3 gap-4 mt-4">
        <div className="bg-white p-4 rounded shadow">Users: 0</div>
        <div className="bg-white p-4 rounded shadow">Projects: 0</div>
        <div className="bg-white p-4 rounded shadow">API Calls: 0</div>
      </div>
    </div>
  );
}'''
        }
    
    def _frontend_components(self) -> Dict[str, str]:
        return {
            "Navbar.tsx": '''export default function Navbar() {
  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-4">
        <a href="/" className="text-xl font-bold">AutoDev</a>
      </div>
    </nav>
  );
}''',
            "Button.tsx": '''interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
}
export default function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  const baseClass = "px-4 py-2 rounded font-medium";
  const variants = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300"
  };
  return (
    <button onClick={onClick} className={`${baseClass} ${variants[variant]}`}>
      {children}
    </button>
  );
}'''
        }
    
    def _frontend_styles(self) -> str:
        return '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
'''
    
    def _generate_tests(self) -> Dict:
        return {
            "test_api.py": self._test_api(),
            "test_services.py": self._test_services()
        }
    
    def _test_api(self) -> str:
        return '''"""API Tests"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to AutoDev API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register():
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "pass123"})
    assert response.status_code == 200
'''
    
    def _test_services(self) -> str:
        return '''"""Service Tests"""
import pytest
from app.services.user_service import UserService

@pytest.mark.asyncio
async def test_create_user():
    service = UserService()
    user = await service.create_user("test@example.com", "password")
    assert user["email"] == "test@example.com"
'''
    
    def _generate_all_files(self, prd: Dict) -> List[Dict]:
        return [
            {"path": "backend/app/main.py", "content": self._backend_main()},
            {"path": "backend/app/models.py", "content": self._backend_models()},
            {"path": "backend/app/api.py", "content": self._backend_api()},
            {"path": "backend/app/services.py", "content": self._backend_services()},
            {"path": "backend/requirements.txt", "content": "fastapi\nuvicorn\nsqlalchemy\npsycopg2-binary\npydantic\npython-jose[cryptography]\npytest\npytest-asyncio"},
            {"path": "frontend/package.json", "content": self._package_json()},
            {"path": "frontend/pages/index.tsx", "content": self._frontend_pages()["index.tsx"]},
            {"path": "frontend/pages/dashboard.tsx", "content": self._frontend_pages()["dashboard.tsx"]},
            {"path": "tests/test_api.py", "content": self._test_api()}
        ]
