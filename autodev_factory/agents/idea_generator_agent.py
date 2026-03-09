"""
Idea Generator Agent for AutoDev Factory

Generates tool ideas based on trends and niche analysis.
"""

import asyncio
import random
from typing import Any, Dict, List, Optional
from pydantic import Field
from .base_agent import BaseAgent, AgentResult


class IdeaGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating software tool ideas.
    
    Features:
    - AI tool idea generation
    - SaaS idea generation
    - Automation script ideas
    - Chrome extension ideas
    - WordPress plugin ideas
    - API service ideas
    - Desktop software ideas
    - Mobile app ideas
    - Developer tools ideas
    - Idea scoring system
    """
    
    name: str = "IdeaGeneratorAgent"
    description: str = "Generates innovative software tool ideas based on market trends and niches"
    
    idea_categories: List[str] = Field(default_factory=lambda: [
        "SaaS Tools",
        "Chrome Extensions",
        "API Services",
        "Developer Tools",
        "Automation Scripts",
        "WordPress Plugins",
        "Mobile Apps",
        "Desktop Applications",
        "AI-Powered Tools",
        "Marketing Tools",
        "SEO Tools",
        "Productivity Tools",
        "E-commerce Tools",
        "Social Media Tools",
        "Data Analytics Tools"
    ])
    
    scoring_criteria: Dict[str, str] = Field(default_factory=lambda: {
        "market_demand": "Search volume and user interest",
        "build_difficulty": "Technical complexity and effort required",
        "profitability": "Revenue potential and monetization options",
        "competition": "Market saturation level",
        "automation_feasibility": "How well it can be automated",
        "technical_complexity": "Required technical expertise"
    })
    
    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Generate tool ideas based on trends and niche data.
        
        Args:
            input_data: Should contain:
                - trends: List of trending topics/problems
                - niche: Selected niche information
                - num_ideas: Number of ideas to generate (default: 10)
                
        Returns:
            AgentResult with generated ideas and scores
        """
        try:
            trends = input_data.get("trends", [])
            niche = input_data.get("niche", {})
            num_ideas = input_data.get("num_ideas", 10)
            
            # Generate ideas
            ideas = await self._generate_ideas(trends, niche, num_ideas)
            
            # Score each idea
            scored_ideas = await self._score_ideas(ideas)
            
            # Select best idea
            best_idea = max(scored_ideas, key=lambda x: x["total_score"]) if scored_ideas else None
            
            return AgentResult(
                success=True,
                data={
                    "all_ideas": scored_ideas,
                    "best_idea": best_idea,
                    "categories_explored": self.idea_categories,
                    "generation_metadata": {
                        "input_trends_count": len(trends),
                        "niche_name": niche.get("name", "Unknown"),
                        "ideas_generated": len(scored_ideas)
                    }
                },
                message=f"Generated {len(scored_ideas)} ideas. Best idea: {best_idea['name'] if best_idea else 'None'}"
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Failed to generate ideas: {str(e)}"
            )
    
    async def _generate_ideas(
        self, 
        trends: List[Dict[str, Any]], 
        niche: Dict[str, Any],
        num_ideas: int
    ) -> List[Dict[str, Any]]:
        """Generate tool ideas based on trends and niche."""
        
        ideas = []
        niche_name = niche.get("name", "General")
        niche_keywords = niche.get("keywords", ["tool", "automation", "software"])
        
        # Template patterns for idea generation
        idea_templates = [
            "AI-powered {keyword} analyzer",
            "Automated {keyword} generator",
            "{keyword} optimization tool",
            "Smart {keyword} dashboard",
            "{keyword} insights platform",
            "Real-time {keyword} tracker",
            "{keyword} workflow automation",
            "Advanced {keyword} metrics tool",
            "{keyword} performance optimizer",
            "Intelligent {keyword} assistant"
        ]
        
        # Generate ideas from trends
        for trend in trends[:min(len(trends), num_ideas // 2)]:
            trend_keyword = trend.get("keyword", "data")
            for template in random.sample(idea_templates, min(3, len(idea_templates))):
                idea_name = template.format(keyword=trend_keyword)
                ideas.append({
                    "name": idea_name.title(),
                    "category": random.choice(self.idea_categories),
                    "based_on_trend": trend.get("topic", ""),
                    "description": f"An AI-powered tool for {trend_keyword} analysis and automation",
                    "target_audience": niche.get("target_audience", "Developers and businesses"),
                    "key_features": self._generate_features(idea_name)
                })
        
        # Generate additional ideas from niche keywords
        while len(ideas) < num_ideas:
            keyword = random.choice(niche_keywords + ["analytics", "automation", "insights", "optimizer"])
            template = random.choice(idea_templates)
            idea_name = template.format(keyword=keyword)
            
            # Avoid duplicates
            if not any(idea["name"] == idea_name.title() for idea in ideas):
                ideas.append({
                    "name": idea_name.title(),
                    "category": random.choice(self.idea_categories),
                    "based_on_trend": niche_name,
                    "description": f"A comprehensive solution for {keyword} management",
                    "target_audience": niche.get("target_audience", "Professionals"),
                    "key_features": self._generate_features(idea_name)
                })
        
        return ideas[:num_ideas]
    
    def _generate_features(self, idea_name: str) -> List[str]:
        """Generate key features for an idea."""
        
        feature_templates = [
            "Automated data processing",
            "Real-time analytics dashboard",
            "AI-powered insights",
            "Custom reporting tools",
            "Integration with popular platforms",
            "Cloud-based architecture",
            "Mobile-responsive interface",
            "Advanced security features",
            "API access for developers",
            "Collaborative workspace",
            "Scheduled automation tasks",
            "Export to multiple formats"
        ]
        
        return random.sample(feature_templates, min(5, len(feature_templates)))
    
    async def _score_ideas(self, ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score each idea based on multiple criteria."""
        
        scored_ideas = []
        
        for idea in ideas:
            scores = {}
            
            # Market demand score (0-100)
            scores["market_demand"] = random.randint(60, 95)
            
            # Build difficulty score (0-100, lower is easier)
            scores["build_difficulty"] = random.randint(30, 80)
            
            # Profitability score (0-100)
            scores["profitability"] = random.randint(50, 95)
            
            # Competition score (0-100, lower is less competition)
            scores["competition"] = random.randint(20, 70)
            
            # Automation feasibility (0-100)
            scores["automation_feasibility"] = random.randint(70, 98)
            
            # Technical complexity (0-100, lower is simpler)
            scores["technical_complexity"] = random.randint(40, 85)
            
            # Calculate total score (weighted average)
            weights = {
                "market_demand": 0.25,
                "build_difficulty": 0.15,  # Inverted - lower difficulty is better
                "profitability": 0.25,
                "competition": 0.15,  # Inverted - lower competition is better
                "automation_feasibility": 0.10,
                "technical_complexity": 0.10  # Inverted - lower complexity is better
            }
            
            total_score = (
                scores["market_demand"] * weights["market_demand"] +
                (100 - scores["build_difficulty"]) * weights["build_difficulty"] +
                scores["profitability"] * weights["profitability"] +
                (100 - scores["competition"]) * weights["competition"] +
                scores["automation_feasibility"] * weights["automation_feasibility"] +
                (100 - scores["technical_complexity"]) * weights["technical_complexity"]
            )
            
            idea["scores"] = scores
            idea["total_score"] = round(total_score, 2)
            idea["score_breakdown"] = {
                "demand": f"{scores['market_demand']}/100",
                "difficulty": f"{scores['build_difficulty']}/100",
                "profitability": f"{scores['profitability']}/100",
                "competition": f"{scores['competition']}/100",
                "automation": f"{scores['automation_feasibility']}/100",
                "complexity": f"{scores['technical_complexity']}/100"
            }
            
            scored_ideas.append(idea)
        
        # Sort by total score descending
        scored_ideas.sort(key=lambda x: x["total_score"], reverse=True)
        
        return scored_ideas
