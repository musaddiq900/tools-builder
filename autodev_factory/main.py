"""
AutoDev Factory - Main Entry Point

This is the main entry point for the AutoDev Factory system.
Run this script to start the autonomous AI developer agent.
"""

import asyncio
import click
import logging
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table

from config import get_settings
from core import AutoDevOrchestrator

# Initialize console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    🚀 AutoDev Factory - Autonomous AI Developer Agent
    
    Build complete software tools automatically with AI agents.
    """
    pass


@cli.command()
@click.option('--niche', default=None, help='Specific niche to focus on')
@click.option('--sources', multiple=True, help='Trend sources to use')
@click.option('--dry-run', is_flag=True, help='Run without creating actual projects')
def daily(niche, sources, dry_run):
    """
    Run the daily workflow to generate a new tool.
    
    This command executes the full daily workflow:
    1. Research trends
    2. Find profitable niche
    3. Generate tool idea
    4. Create product requirements
    5. Design architecture
    6. Generate codebase
    7. Test and debug
    8. Create documentation
    9. Push to GitHub
    """
    console.print(Panel.fit(
        "[bold blue]🚀 Starting Daily Workflow[/bold blue]\n\n"
        "Autonomous AI Developer Agent is initializing...",
        border_style="blue"
    ))
    
    settings = get_settings()
    
    # Show configuration warnings
    warnings = settings.validate_configuration()
    if warnings:
        for warning in warnings:
            console.print(f"[yellow]⚠️  {warning}[/yellow]")
        if not dry_run:
            console.print("[yellow]Continuing in demo mode...[/yellow]\n")
    
    # Run daily workflow
    orchestrator = AutoDevOrchestrator(dry_run=dry_run)
    
    workflow_params = {}
    if niche:
        workflow_params['preferred_niche'] = niche
    if sources:
        workflow_params['trend_sources'] = list(sources)
    
    result = asyncio.run(orchestrator.run_daily_workflow(**workflow_params))
    
    if result.success:
        console.print(Panel.fit(
            f"[bold green]✅ Daily Workflow Completed Successfully![/bold green]\n\n"
            f"Tool Created: [bold]{result.data.get('tool_name', 'Unknown')}[/bold]\n"
            f"Repository: {result.data.get('repo_url', 'N/A')}\n"
            f"Status: {result.data.get('status', 'Completed')}",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            f"[bold red]❌ Daily Workflow Failed[/bold red]\n\n"
            f"Error: {result.message}",
            border_style="red"
        ))


@cli.command()
@click.option('--github-token', envvar='GITHUB_TOKEN', help='GitHub token for authentication')
@click.option('--repo-name', required=True, help='Name of the repository to create')
def create_repo(github_token, repo_name):
    """
    Create a new GitHub repository.
    
    This command creates a new repository on GitHub
    and prepares it for code pushing.
    """
    console.print(f"[blue]Creating repository: {repo_name}...[/blue]")
    
    if not github_token:
        console.print("[red]Error: GitHub token is required.[/red]")
        console.print("Set GITHUB_TOKEN environment variable or use --github-token option.")
        return
    
    # Placeholder for GitHub repo creation
    console.print("[yellow]GitHub integration coming soon...[/yellow]")


@cli.command()
def status():
    """Show the current status of the AutoDev Factory."""
    settings = get_settings()
    
    table = Table(title="AutoDev Factory Status", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")
    
    # AI Models
    ai_status = "✅" if settings.has_openai_key or settings.has_anthropic_key else "❌"
    ai_details = []
    if settings.has_openai_key:
        ai_details.append("OpenAI configured")
    if settings.has_anthropic_key:
        ai_details.append("Anthropic configured")
    if not ai_details:
        ai_details.append("No API keys set")
    
    table.add_row("AI Models", ai_status, ", ".join(ai_details))
    
    # GitHub
    github_status = "✅" if settings.has_github_token else "❌"
    table.add_row("GitHub Integration", github_status, 
                  f"User: {settings.github_username}" if settings.github_username else "Not configured")
    
    # Database
    table.add_row("Database", "✅", settings.database_url.split(":///")[1] if ":///" in settings.database_url else "Configured")
    
    # Environment
    table.add_row("Environment", "🟢" if settings.environment == "development" else "🔴", 
                  settings.environment.title())
    
    console.print(table)
    
    # Show recent activity
    console.print("\n[bold]Recent Activity:[/bold]")
    output_dir = Path(settings.output_dir)
    if output_dir.exists():
        projects = list(output_dir.iterdir())
        if projects:
            for project in projects[-5:]:  # Last 5 projects
                console.print(f"  • {project.name}")
        else:
            console.print("  No projects created yet.")
    else:
        console.print("  Output directory does not exist yet.")


@cli.command()
def config():
    """Show current configuration."""
    settings = get_settings()
    
    table = Table(title="Configuration", show_header=True, header_style="bold blue")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Environment", settings.environment)
    table.add_row("Log Level", settings.log_level)
    table.add_row("Default Model", settings.default_model)
    table.add_row("Temperature", str(settings.temperature))
    table.add_row("Max Tokens", str(settings.max_tokens))
    table.add_row("Output Directory", str(settings.output_dir))
    table.add_row("Max Retries", str(settings.max_retries))
    table.add_row("Timeout (seconds)", str(settings.timeout_seconds))
    
    console.print(table)


@cli.command()
@click.argument('agent_name')
def test_agent(agent_name):
    """
    Test a specific agent.
    
    AGENT_NAME: Name of the agent to test
    (e.g., trend_research, niche_finder, idea_generator)
    """
    console.print(f"[blue]Testing agent: {agent_name}[/blue]")
    
    # Placeholder for agent testing
    console.print("[yellow]Agent testing framework coming soon...[/yellow]")


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
