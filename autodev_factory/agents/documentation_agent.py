"""
Documentation Agent for AutoDev Factory

Generates comprehensive documentation for projects.
"""

from typing import Any, Dict, List
from datetime import datetime
from .base_agent import BaseAgent, AgentResult


class DocumentationAgent(BaseAgent):
    """
    Agent responsible for generating documentation.
    
    Features:
    - README generation
    - API documentation
    - Setup guide
    - Installation instructions
    - Developer documentation
    - Architecture diagrams
    - Code documentation
    """
    
    name: str = "DocumentationAgent"
    description: str = "Generates comprehensive documentation for projects"
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        try:
            prd = input_data.get("prd", {})
            codebase = input_data.get("codebase", {})
            project_name = prd.get("project_name", "Project")
            
            docs = self._generate_docs(prd, codebase, project_name)
            
            return AgentResult(
                success=True,
                data={"documentation": docs},
                message=f"Generated documentation for {project_name}"
            )
        except Exception as e:
            return AgentResult(success=False, message=f"Documentation failed: {str(e)}")
    
    def _generate_docs(self, prd: Dict, codebase: Dict, project_name: str) -> Dict:
        return {
            "readme": self._generate_readme(prd, project_name),
            "api_docs": self._generate_api_docs(prd),
            "installation_guide": self._generate_installation_guide(),
            "architecture_doc": self._generate_architecture_doc()
        }
    
    def _generate_readme(self, prd: Dict, project_name: str) -> str:
        features = prd.get("features", {}).get("core_features", [])
        feature_list = "\n".join([f"- {f.get('name', '')}" for f in features[:5]])
        
        return f"""# {project_name}

## Description
Auto-generated software tool built by AutoDev Factory.

## Features
{feature_list}

## Installation
```bash
git clone https://github.com/username/{project_name.lower().replace(' ', '-')}
cd {project_name.lower().replace(' ', '-')}
docker-compose up -d
```

## Usage
```bash
# Start backend
cd backend && uvicorn app.main:app --reload

# Start frontend  
cd frontend && npm run dev
```

## API Documentation
See [API Docs](docs/api.md)

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: Next.js (TypeScript)
- Database: PostgreSQL
- Cache: Redis

## License
MIT License
"""
    
    def _generate_api_docs(self, prd: Dict) -> str:
        endpoints = prd.get("api_specifications", {}).get("endpoints", [])
        
        doc = "# API Documentation\n\n## Endpoints\n\n"
        for ep in endpoints:
            doc += f"### {ep.get('method', 'GET')} {ep.get('path', '/')}\n"
            doc += f"{ep.get('description', '')}\n\n"
        
        return doc
    
    def _generate_installation_guide(self) -> str:
        return """# Installation Guide

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

## Quick Start
1. Clone repository
2. Copy `.env.example` to `.env`
3. Run `docker-compose up -d`
4. Access at http://localhost:3000

## Development Setup
See docs/development.md
"""
    
    def _generate_architecture_doc(self) -> str:
        return """# Architecture Documentation

## System Overview
Microservices architecture with separate frontend and backend.

## Components
- API Gateway
- Auth Service
- Core Service
- Worker Service
- Database (PostgreSQL)
- Cache (Redis)

## Data Flow
Client → Load Balancer → API Gateway → Services → Database
"""
