"""
File Structure Agent for AutoDev Factory

Creates complete project folder structures.
"""

from typing import Any, Dict, List
from .base_agent import BaseAgent, AgentResult


class FileStructureAgent(BaseAgent):
    """
    Agent responsible for creating project file structures.
    
    Features:
    - Folder structure creation
    - Module separation
    - Dependency management
    - Environment configuration
    - Docker setup
    - Config file generation
    """
    
    name: str = "FileStructureAgent"
    description: str = "Creates complete project folder structures"
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        try:
            architecture = input_data.get("architecture", {})
            prd = input_data.get("prd", {})
            project_name = prd.get("project_name", "project").lower().replace(" ", "-")
            
            structure = self._create_structure(project_name, architecture)
            
            return AgentResult(
                success=True,
                data={"structure": structure, "project_name": project_name},
                message=f"Created file structure for {project_name}"
            )
        except Exception as e:
            return AgentResult(success=False, message=f"Structure creation failed: {str(e)}")
    
    def _create_structure(self, project_name: str, architecture: Dict) -> Dict:
        return {
            "root": project_name,
            "directories": self._get_directories(),
            "files": self._get_files(project_name),
            "docker_files": self._get_docker_files(),
            "config_files": self._get_config_files(project_name)
        }
    
    def _get_directories(self) -> List[str]:
        return [
            "backend/app", "backend/app/api", "backend/app/core", 
            "backend/app/models", "backend/app/services", "backend/app/utils",
            "frontend/src", "frontend/src/components", "frontend/src/pages",
            "frontend/src/hooks", "frontend/src/utils", "frontend/src/styles",
            "tests/unit", "tests/integration", "tests/e2e",
            "docs", "scripts", "deployments", ".github/workflows"
        ]
    
    def _get_files(self, project_name: str) -> List[Dict]:
        return [
            {"path": "README.md", "type": "markdown"},
            {"path": "LICENSE", "type": "text"},
            {"path": ".gitignore", "type": "git"},
            {"path": "backend/requirements.txt", "type": "python-deps"},
            {"path": "backend/app/main.py", "type": "python"},
            {"path": "backend/app/__init__.py", "type": "python"},
            {"path": "frontend/package.json", "type": "node-deps"},
            {"path": "frontend/next.config.js", "type": "javascript"},
            {"path": "docker-compose.yml", "type": "yaml"},
            {"path": "Makefile", "type": "makefile"},
            {"path": ".env.example", "type": "env"}
        ]
    
    def _get_docker_files(self) -> List[Dict]:
        return [
            {"name": "Dockerfile.backend", "content": self._backend_dockerfile()},
            {"name": "Dockerfile.frontend", "content": self._frontend_dockerfile()},
            {"name": "docker-compose.yml", "content": self._docker_compose()}
        ]
    
    def _backend_dockerfile(self) -> str:
        return """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    def _frontend_dockerfile(self) -> str:
        return """FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
"""
    
    def _docker_compose(self) -> str:
        return """version: '3.8'
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
"""
    
    def _get_config_files(self, project_name: str) -> List[Dict]:
        return [
            {"name": ".env.example", "content": self._env_example()},
            {"name": "pyproject.toml", "content": self._pyproject(project_name)},
            {"name": ".pre-commit-config.yaml", "content": self._precommit_config()}
        ]
    
    def _env_example(self) -> str:
        return """DATABASE_URL=postgresql://user:pass@localhost:5432/app
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key
DEBUG=true
"""
    
    def _pyproject(self, project_name: str) -> str:
        return f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "Auto-generated project"
authors = ["AutoDev Factory"]

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
"""
    
    def _precommit_config(self) -> str:
        return """repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
-   repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
    -   id: flake8
"""
