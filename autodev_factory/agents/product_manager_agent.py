"""
Product Manager Agent for AutoDev Factory

Creates comprehensive Product Requirements Documents (PRD).
"""

import asyncio
from typing import Any, Dict, List, Optional
from pydantic import Field
from datetime import datetime
from .base_agent import BaseAgent, AgentResult


class ProductManagerAgent(BaseAgent):
    """
    Agent responsible for creating Product Requirements Documents.
    
    Features:
    - Problem definition
    - Target audience identification
    - Feature list generation
    - User flow design
    - Product scope definition
    - Technical requirements generation
    - API specification
    - Security requirements
    """
    
    name: str = "ProductManagerAgent"
    description: str = "Creates comprehensive Product Requirements Documents (PRD) for software projects"
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Create a PRD based on the selected idea.
        
        Args:
            input_data: Should contain:
                - idea: Selected tool idea
                - niche: Target niche information
                - trends: Related trends
                
        Returns:
            AgentResult with complete PRD
        """
        try:
            idea = input_data.get("idea", {})
            niche = input_data.get("niche", {})
            trends = input_data.get("trends", [])
            
            if not idea:
                return AgentResult(
                    success=False,
                    message="No idea provided for PRD generation"
                )
            
            # Generate PRD
            prd = await self._generate_prd(idea, niche, trends)
            
            return AgentResult(
                success=True,
                data={
                    "prd": prd,
                    "project_name": prd["project_name"],
                    "version": "1.0.0"
                },
                message=f"Created PRD for {prd['project_name']}"
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Failed to create PRD: {str(e)}"
            )
    
    async def _generate_prd(
        self, 
        idea: Dict[str, Any], 
        niche: Dict[str, Any],
        trends: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a comprehensive Product Requirements Document."""
        
        project_name = idea.get("name", "New Tool").replace(" ", "").lower()
        
        prd = {
            "project_name": idea.get("name", "New Software Tool"),
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            
            # 1. Executive Summary
            "executive_summary": {
                "problem_statement": self._generate_problem_statement(idea),
                "solution_overview": idea.get("description", ""),
                "value_proposition": self._generate_value_proposition(idea, niche),
                "success_metrics": self._define_success_metrics()
            },
            
            # 2. Target Audience
            "target_audience": {
                "primary_users": idea.get("target_audience", "Developers and businesses"),
                "user_personas": self._create_user_personas(niche),
                "user_stories": self._generate_user_stories(idea),
                "market_segment": niche.get("name", "General")
            },
            
            # 3. Features & Requirements
            "features": {
                "core_features": self._define_core_features(idea),
                "nice_to_have_features": self._define_nice_to_have_features(),
                "feature_priorities": self._prioritize_features(idea),
                "feature_descriptions": self._describe_features(idea)
            },
            
            # 4. User Flow & Experience
            "user_flow": {
                "user_journey_map": self._create_user_journey(),
                "wireframe_descriptions": self._describe_wireframes(),
                "key_interactions": self._define_key_interactions()
            },
            
            # 5. Technical Requirements
            "technical_requirements": {
                "functional_requirements": self._define_functional_requirements(idea),
                "non_functional_requirements": self._define_non_functional_requirements(),
                "performance_requirements": self._define_performance_requirements(),
                "scalability_requirements": self._define_scalability_requirements()
            },
            
            # 6. API Specifications
            "api_specifications": {
                "endpoints": self._define_api_endpoints(idea),
                "authentication_method": "JWT Token-based authentication",
                "rate_limiting": "100 requests per minute for free tier",
                "data_formats": ["JSON", "XML (optional)"]
            },
            
            # 7. Security Requirements
            "security_requirements": {
                "authentication": "Multi-factor authentication support",
                "authorization": "Role-based access control (RBAC)",
                "data_encryption": "AES-256 encryption at rest, TLS 1.3 in transit",
                "compliance": ["GDPR", "SOC 2 Type II", "OWASP Top 10"],
                "security_measures": self._define_security_measures()
            },
            
            # 8. Database Schema
            "database_schema": {
                "tables": self._define_database_tables(idea),
                "relationships": self._define_table_relationships(),
                "indexing_strategy": "Primary and secondary indexes on frequently queried fields"
            },
            
            # 9. Integration Requirements
            "integrations": {
                "third_party_apis": self._define_third_party_integrations(idea),
                "webhook_support": True,
                "api_versioning": "URL-based versioning (v1, v2, etc.)"
            },
            
            # 10. Deployment & Infrastructure
            "deployment": {
                "hosting_platform": "Cloud-native (AWS/GCP/Azure)",
                "containerization": "Docker containers",
                "orchestration": "Kubernetes",
                "ci_cd_pipeline": "GitHub Actions or GitLab CI"
            },
            
            # 11. Timeline & Milestones
            "timeline": {
                "phases": self._define_project_phases(),
                "estimated_duration": "8-12 weeks for MVP",
                "critical_path": self._identify_critical_path()
            },
            
            # 12. Risks & Mitigation
            "risks": {
                "technical_risks": self._identify_technical_risks(),
                "market_risks": self._identify_market_risks(),
                "mitigation_strategies": self._define_mitigation_strategies()
            }
        }
        
        return prd
    
    def _generate_problem_statement(self, idea: Dict[str, Any]) -> str:
        """Generate a clear problem statement."""
        return f"""
        Modern professionals struggle with efficient {idea.get('category', 'tool')} management. 
        Current solutions are either too complex, expensive, or lack essential features. 
        Users need an automated, intelligent solution that simplifies their workflow 
        while providing powerful insights and capabilities.
        """
    
    def _generate_value_proposition(self, idea: Dict[str, Any], niche: Dict[str, Any]) -> str:
        """Generate value proposition."""
        return f"""
        Our {idea.get('name', 'tool')} delivers AI-powered automation and insights 
        specifically designed for {niche.get('target_audience', 'professionals')}. 
        Unlike competitors, we offer seamless integration, intuitive UI, 
        and advanced features at an affordable price point.
        """
    
    def _define_success_metrics(self) -> List[str]:
        """Define success metrics for the product."""
        return [
            "User acquisition: 1000 active users in first month",
            "Retention rate: >60% after 30 days",
            "Customer satisfaction: NPS score >50",
            "Revenue: $10K MRR within 3 months",
            "Performance: <200ms average API response time",
            "Uptime: 99.9% availability"
        ]
    
    def _create_user_personas(self, niche: Dict[str, Any]) -> List[Dict[str, str]]:
        """Create user personas."""
        return [
            {
                "name": "Developer Dan",
                "role": "Software Developer",
                "goals": "Automate repetitive tasks, improve productivity",
                "pain_points": "Manual processes, lack of integration between tools"
            },
            {
                "name": "Business Betty",
                "role": "Business Owner/Manager",
                "goals": "Reduce costs, improve team efficiency",
                "pain_points": "Expensive enterprise solutions, steep learning curves"
            },
            {
                "name": "Startup Steve",
                "role": "Startup Founder",
                "goals": "Quick deployment, scalable solutions",
                "pain_points": "Limited budget, need for rapid iteration"
            }
        ]
    
    def _generate_user_stories(self, idea: Dict[str, Any]) -> List[str]:
        """Generate user stories."""
        return [
            "As a user, I want to easily set up the tool so that I can start using it quickly",
            "As a user, I want automated insights so that I can make data-driven decisions",
            "As a user, I want to integrate with my existing tools so that I don't have to switch contexts",
            "As a user, I want customizable dashboards so that I can see the metrics that matter to me",
            "As a user, I want export capabilities so that I can share reports with my team",
            "As an admin, I want user management features so that I can control access",
            "As a developer, I want API access so that I can build custom integrations"
        ]
    
    def _define_core_features(self, idea: Dict[str, Any]) -> List[Dict[str, str]]:
        """Define core features."""
        base_features = idea.get("key_features", [])
        
        return [
            {"name": "User Authentication", "priority": "P0", "description": "Secure login and registration"},
            {"name": "Dashboard", "priority": "P0", "description": "Main interface with key metrics"},
            {"name": "Data Processing Engine", "priority": "P0", "description": "Core automation logic"},
            {"name": "API Endpoints", "priority": "P0", "description": "RESTful API for integrations"},
            {"name": "Reporting System", "priority": "P1", "description": "Generate and export reports"},
            {"name": "Settings & Configuration", "priority": "P1", "description": "User preferences and tool settings"},
            * [{"name": feat, "priority": "P1", "description": f"Feature: {feat}"} for feat in base_features[:3]]
        ]
    
    def _define_nice_to_have_features(self) -> List[str]:
        """Define nice-to-have features."""
        return [
            "Dark mode theme",
            "Mobile app (iOS/Android)",
            "Browser extension",
            "Advanced analytics with ML predictions",
            "Team collaboration features",
            "White-label options",
            "Custom branding",
            "Webhook notifications"
        ]
    
    def _prioritize_features(self, idea: Dict[str, Any]) -> Dict[str, List[str]]:
        """Prioritize features using MoSCoW method."""
        return {
            "Must Have": ["Authentication", "Core functionality", "Basic UI", "API"],
            "Should Have": ["Reporting", "Integrations", "Advanced settings"],
            "Could Have": ["Mobile app", "Advanced analytics", "Collaboration"],
            "Won't Have (this release)": ["AI predictions", "White-label", "Enterprise SSO"]
        }
    
    def _describe_features(self, idea: Dict[str, Any]) -> Dict[str, str]:
        """Provide detailed feature descriptions."""
        return {
            "Authentication": "JWT-based authentication with optional 2FA",
            "Dashboard": "Real-time metrics visualization with customizable widgets",
            "Data Processing": "Automated background processing with queue management",
            "API": "RESTful API with comprehensive documentation",
            "Reporting": "PDF/CSV export with scheduled report generation"
        }
    
    def _create_user_journey(self) -> List[Dict[str, str]]:
        """Create user journey map."""
        return [
            {"stage": "Discovery", "action": "User finds the tool via search or referral"},
            {"stage": "Sign Up", "action": "User creates account and verifies email"},
            {"stage": "Onboarding", "action": "User completes setup wizard"},
            {"stage": "First Use", "action": "User runs first automation/task"},
            {"stage": "Regular Use", "action": "User integrates tool into daily workflow"},
            {"stage": "Advocacy", "action": "User recommends tool to others"}
        ]
    
    def _describe_wireframes(self) -> List[Dict[str, str]]:
        """Describe key wireframes."""
        return [
            {"page": "Landing Page", "elements": "Hero section, features, pricing, testimonials, CTA"},
            {"page": "Dashboard", "elements": "Navigation sidebar, metrics cards, charts, recent activity"},
            {"page": "Settings", "elements": "Profile settings, API keys, notifications, billing"},
            {"page": "Reports", "elements": "Date filters, export options, visualization charts"}
        ]
    
    def _define_key_interactions(self) -> List[str]:
        """Define key user interactions."""
        return [
            "One-click setup wizard",
            "Drag-and-drop dashboard customization",
            "Real-time data refresh",
            "Inline help tooltips",
            "Keyboard shortcuts for power users"
        ]
    
    def _define_functional_requirements(self, idea: Dict[str, Any]) -> List[str]:
        """Define functional requirements."""
        return [
            "System shall allow users to register and authenticate securely",
            "System shall process data according to configured rules",
            "System shall provide RESTful API endpoints",
            "System shall generate reports in multiple formats",
            "System shall send notifications for important events",
            "System shall maintain audit logs of all actions"
        ]
    
    def _define_non_functional_requirements(self) -> List[str]:
        """Define non-functional requirements."""
        return [
            "System shall handle 10,000 concurrent users",
            "System shall respond to API requests within 200ms (p95)",
            "System shall maintain 99.9% uptime",
            "System shall be GDPR compliant",
            "System shall support horizontal scaling"
        ]
    
    def _define_performance_requirements(self) -> Dict[str, Any]:
        """Define performance requirements."""
        return {
            "response_time": "<200ms for API calls",
            "throughput": "1000 requests/second",
            "concurrent_users": "10,000+",
            "data_processing": "Handle 1M records/hour"
        }
    
    def _define_scalability_requirements(self) -> List[str]:
        """Define scalability requirements."""
        return [
            "Horizontal scaling for API servers",
            "Database read replicas for high traffic",
            "CDN for static assets",
            "Auto-scaling based on CPU/memory usage",
            "Message queue for async processing"
        ]
    
    def _define_api_endpoints(self, idea: Dict[str, Any]) -> List[Dict[str, str]]:
        """Define API endpoints."""
        return [
            {"method": "POST", "path": "/api/v1/auth/register", "description": "User registration"},
            {"method": "POST", "path": "/api/v1/auth/login", "description": "User login"},
            {"method": "GET", "path": "/api/v1/dashboard", "description": "Get dashboard data"},
            {"method": "POST", "path": "/api/v1/process", "description": "Trigger data processing"},
            {"method": "GET", "path": "/api/v1/reports", "description": "List reports"},
            {"method": "GET", "path": "/api/v1/reports/{id}", "description": "Get specific report"},
            {"method": "POST", "path": "/api/v1/reports/export", "description": "Export report"}
        ]
    
    def _define_security_measures(self) -> List[str]:
        """Define security measures."""
        return [
            "Rate limiting on all endpoints",
            "SQL injection prevention",
            "XSS protection",
            "CSRF tokens",
            "Input validation and sanitization",
            "Regular security audits",
            "Vulnerability scanning"
        ]
    
    def _define_database_tables(self, idea: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define database tables."""
        return [
            {"name": "users", "columns": ["id", "email", "password_hash", "created_at", "updated_at"]},
            {"name": "projects", "columns": ["id", "user_id", "name", "config", "created_at"]},
            {"name": "tasks", "columns": ["id", "project_id", "status", "result", "created_at"]},
            {"name": "reports", "columns": ["id", "user_id", "data", "format", "created_at"]},
            {"name": "api_keys", "columns": ["id", "user_id", "key_hash", "permissions", "created_at"]}
        ]
    
    def _define_table_relationships(self) -> List[str]:
        """Define table relationships."""
        return [
            "users (1) -> (many) projects",
            "projects (1) -> (many) tasks",
            "users (1) -> (many) reports",
            "users (1) -> (many) api_keys"
        ]
    
    def _define_third_party_integrations(self, idea: Dict[str, Any]) -> List[str]:
        """Define third-party integrations."""
        return [
            "Google OAuth for authentication",
            "Stripe for payment processing",
            "SendGrid for email notifications",
            "Slack for team notifications",
            "GitHub for version control integration"
        ]
    
    def _define_project_phases(self) -> List[Dict[str, str]]:
        """Define project phases."""
        return [
            {"phase": "Phase 1", "duration": "2 weeks", "goal": "Core infrastructure and authentication"},
            {"phase": "Phase 2", "duration": "3 weeks", "goal": "Main functionality implementation"},
            {"phase": "Phase 3", "duration": "2 weeks", "goal": "UI/UX development"},
            {"phase": "Phase 4", "duration": "2 weeks", "goal": "Testing and bug fixes"},
            {"phase": "Phase 5", "duration": "1 week", "goal": "Deployment and launch"}
        ]
    
    def _identify_critical_path(self) -> List[str]:
        """Identify critical path items."""
        return [
            "Database schema design",
            "Authentication system",
            "Core processing engine",
            "API development",
            "Frontend dashboard"
        ]
    
    def _identify_technical_risks(self) -> List[Dict[str, str]]:
        """Identify technical risks."""
        return [
            {"risk": "Scalability issues", "impact": "High", "probability": "Medium"},
            {"risk": "Third-party API dependencies", "impact": "Medium", "probability": "Medium"},
            {"risk": "Security vulnerabilities", "impact": "High", "probability": "Low"}
        ]
    
    def _identify_market_risks(self) -> List[Dict[str, str]]:
        """Identify market risks."""
        return [
            {"risk": "Strong competition", "impact": "High", "probability": "Medium"},
            {"risk": "Low market demand", "impact": "High", "probability": "Low"},
            {"risk": "Price sensitivity", "impact": "Medium", "probability": "Medium"}
        ]
    
    def _define_mitigation_strategies(self) -> List[Dict[str, str]]:
        """Define mitigation strategies."""
        return [
            {"strategy": "Implement robust testing", "addresses": "Technical risks"},
            {"strategy": "Build scalable architecture from start", "addresses": "Scalability risks"},
            {"strategy": "Focus on unique value proposition", "addresses": "Competition"},
            {"strategy": "Iterative development with user feedback", "addresses": "Market fit"}
        ]
