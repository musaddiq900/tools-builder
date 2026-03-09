"""
Niche Finder Agent

This agent identifies profitable micro-niches based on trend data.
"""

from typing import Dict, Any, List
import logging
from .base_agent import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


class NicheFinderAgent(BaseAgent):
    """
    Agent responsible for finding profitable niches.
    
    Analyzes:
    - Competition level
    - Search volume
    - Monetization potential
    - Market difficulty
    """
    
    name: str = "NicheFinderAgent"
    description: str = "Identifies profitable micro-niches with low competition and high demand"
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute niche analysis.
        
        Args:
            input_data: Contains:
                - trends: List of trending topics from TrendResearchAgent
                - preferences: User preferences for niches
                
        Returns:
            AgentResult with best niche recommendations
        """
        try:
            trends = input_data.get("trends", [])
            preferences = input_data.get("preferences", {})
            
            # Define known niches
            niches = self._get_known_niches()
            
            # Score each niche based on trends and market data
            scored_niches = await self._score_niches(niches, trends, preferences)
            
            # Select top niche
            best_niche = max(scored_niches, key=lambda x: x["total_score"]) if scored_niches else None
            
            result_data = {
                "best_niche": best_niche,
                "all_niches": scored_niches,
                "recommendation_confidence": best_niche["total_score"] / 100 if best_niche else 0
            }
            
            return AgentResult(
                success=True,
                data=result_data,
                message=f"Identified best niche: {best_niche['name']}" if best_niche else "No suitable niche found"
            )
            
        except Exception as e:
            logger.error(f"Niche finding failed: {str(e)}", exc_info=True)
            return AgentResult(
                success=False,
                message=f"Niche finding failed: {str(e)}"
            )
    
    def _get_known_niches(self) -> List[Dict[str, Any]]:
        """Get list of known profitable niches."""
        return [
            {
                "name": "seo_tools",
                "display_name": "SEO Tools",
                "description": "Tools for search engine optimization",
                "target_audience": "marketers, website owners, agencies",
                "examples": ["keyword research", "backlink analysis", "rank tracking"]
            },
            {
                "name": "shopify_automation",
                "display_name": "Shopify Automation",
                "description": "Tools for Shopify store automation",
                "target_audience": "e-commerce store owners",
                "examples": ["inventory management", "order processing", "customer support"]
            },
            {
                "name": "youtube_automation",
                "display_name": "YouTube Automation",
                "description": "Tools for YouTube content creators",
                "target_audience": "YouTubers, video creators",
                "examples": ["thumbnail generation", "title optimization", "analytics"]
            },
            {
                "name": "ai_content_tools",
                "display_name": "AI Content Tools",
                "description": "AI-powered content creation tools",
                "target_audience": "content creators, marketers, writers",
                "examples": ["article writing", "social media posts", "email copywriting"]
            },
            {
                "name": "chrome_extensions",
                "display_name": "Chrome Extensions",
                "description": "Browser extension tools",
                "target_audience": "general users, professionals",
                "examples": ["productivity boosters", "automation tools", "enhancement utilities"]
            },
            {
                "name": "marketing_automation",
                "display_name": "Marketing Automation",
                "description": "Marketing workflow automation",
                "target_audience": "marketers, businesses",
                "examples": ["email campaigns", "social scheduling", "lead nurturing"]
            },
            {
                "name": "saas_micro_tools",
                "display_name": "SaaS Micro Tools",
                "description": "Small, focused SaaS applications",
                "target_audience": "businesses, professionals",
                "examples": ["invoice generators", "scheduling tools", "form builders"]
            },
            {
                "name": "developer_tools",
                "display_name": "Developer Tools",
                "description": "Tools for software developers",
                "target_audience": "developers, engineers",
                "examples": ["code generators", "debugging tools", "API clients"]
            },
            {
                "name": "productivity_tools",
                "display_name": "Productivity Tools",
                "description": "Personal and team productivity",
                "target_audience": "professionals, teams",
                "examples": ["task managers", "time trackers", "note-taking apps"]
            },
            {
                "name": "analytics_tools",
                "display_name": "Analytics Tools",
                "description": "Data analytics and visualization",
                "target_audience": "analysts, businesses",
                "examples": ["dashboards", "reporting tools", "data connectors"]
            }
        ]
    
    async def _score_niches(
        self, 
        niches: List[Dict[str, Any]], 
        trends: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Score each niche based on multiple factors."""
        scored_niches = []
        
        for niche in niches:
            # Calculate scores
            competition_score = self._calculate_competition_score(niche)
            demand_score = self._calculate_demand_score(niche, trends)
            monetization_score = self._calculate_monetization_score(niche)
            difficulty_score = self._calculate_difficulty_score(niche)
            
            # Weighted total score
            weights = {
                "competition": 0.25,
                "demand": 0.35,
                "monetization": 0.25,
                "difficulty": 0.15
            }
            
            total_score = (
                competition_score * weights["competition"] +
                demand_score * weights["demand"] +
                monetization_score * weights["monetization"] +
                difficulty_score * weights["difficulty"]
            )
            
            scored_niche = {
                **niche,
                "scores": {
                    "competition": competition_score,
                    "demand": demand_score,
                    "monetization": monetization_score,
                    "difficulty": difficulty_score
                },
                "total_score": round(total_score, 2),
                "opportunity_level": self._get_opportunity_level(total_score)
            }
            
            scored_niches.append(scored_niche)
        
        # Sort by total score descending
        return sorted(scored_niches, key=lambda x: x["total_score"], reverse=True)
    
    def _calculate_competition_score(self, niche: Dict[str, Any]) -> float:
        """Calculate competition score (0-100). Lower competition = higher score."""
        # Mock implementation - would use real market data in production
        competition_levels = {
            "seo_tools": 65,  # High competition
            "shopify_automation": 55,
            "youtube_automation": 45,
            "ai_content_tools": 70,  # Very high competition
            "chrome_extensions": 50,
            "marketing_automation": 60,
            "saas_micro_tools": 40,  # Lower competition
            "developer_tools": 55,
            "productivity_tools": 65,
            "analytics_tools": 50
        }
        
        base_competition = competition_levels.get(niche["name"], 50)
        # Invert so lower competition = higher score
        return round(100 - base_competition, 2)
    
    def _calculate_demand_score(self, niche: Dict[str, Any], trends: List[Dict[str, Any]]) -> float:
        """Calculate demand score based on trends (0-100)."""
        # Check if niche matches any trending topics
        niche_keywords = niche["name"].replace("_", " ").split()
        niche_keywords.extend(niche.get("examples", []))
        
        trend_matches = 0
        total_trend_score = 0
        
        for trend in trends:
            topic = trend.get("topic", "").lower()
            for keyword in niche_keywords:
                if keyword.lower() in topic:
                    trend_matches += 1
                    total_trend_score += trend.get("score", 0)
        
        if trend_matches == 0:
            return 50.0  # Neutral score
        
        # Scale based on matches and trend scores
        demand_score = min(100, 50 + (trend_matches * 10) + (total_trend_score / 10))
        return round(demand_score, 2)
    
    def _calculate_monetization_score(self, niche: Dict[str, Any]) -> float:
        """Calculate monetization potential score (0-100)."""
        monetization_potential = {
            "seo_tools": 85,
            "shopify_automation": 90,
            "youtube_automation": 75,
            "ai_content_tools": 80,
            "chrome_extensions": 65,
            "marketing_automation": 88,
            "saas_micro_tools": 82,
            "developer_tools": 70,
            "productivity_tools": 72,
            "analytics_tools": 78
        }
        
        return float(monetization_potential.get(niche["name"], 70))
    
    def _calculate_difficulty_score(self, niche: Dict[str, Any]) -> float:
        """Calculate build difficulty score (0-100). Lower difficulty = higher score."""
        difficulty_levels = {
            "seo_tools": 60,
            "shopify_automation": 65,
            "youtube_automation": 55,
            "ai_content_tools": 70,
            "chrome_extensions": 45,  # Easier to build
            "marketing_automation": 75,
            "saas_micro_tools": 50,
            "developer_tools": 65,
            "productivity_tools": 55,
            "analytics_tools": 70
        }
        
        base_difficulty = difficulty_levels.get(niche["name"], 60)
        # Invert so lower difficulty = higher score
        return round(100 - base_difficulty, 2)
    
    def _get_opportunity_level(self, score: float) -> str:
        """Get opportunity level based on score."""
        if score >= 75:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 45:
            return "moderate"
        else:
            return "low"
