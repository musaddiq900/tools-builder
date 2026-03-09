"""
Git Utilities for AutoDev Factory
"""

import subprocess
from pathlib import Path
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class GitUtils:
    """Utility class for Git operations."""
    
    @staticmethod
    def init_repo(path: str) -> bool:
        """Initialize a Git repository."""
        try:
            subprocess.run(
                ['git', 'init'],
                cwd=path,
                check=True,
                capture_output=True
            )
            logger.info(f"Initialized Git repo at: {path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to init Git repo: {e.stderr.decode()}")
            return False
    
    @staticmethod
    def add_all(path: str) -> bool:
        """Add all files to Git staging."""
        try:
            subprocess.run(
                ['git', 'add', '.'],
                cwd=path,
                check=True,
                capture_output=True
            )
            logger.info("Added all files to staging")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to add files: {e.stderr.decode()}")
            return False
    
    @staticmethod
    def commit(path: str, message: str) -> bool:
        """Commit staged changes."""
        try:
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=path,
                check=True,
                capture_output=True
            )
            logger.info(f"Committed: {message}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit: {e.stderr.decode()}")
            return False
    
    @staticmethod
    def create_branch(path: str, branch_name: str) -> bool:
        """Create a new branch."""
        try:
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=path,
                check=True,
                capture_output=True
            )
            logger.info(f"Created branch: {branch_name}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create branch: {e.stderr.decode()}")
            return False
    
    @staticmethod
    def push(path: str, remote: str = 'origin', branch: str = 'main') -> bool:
        """Push changes to remote."""
        try:
            subprocess.run(
                ['git', 'push', '-u', remote, branch],
                cwd=path,
                check=True,
                capture_output=True
            )
            logger.info(f"Pushed to {remote}/{branch}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to push: {e.stderr.decode()}")
            return False
    
    @staticmethod
    def create_readme(path: str, content: str) -> Path:
        """Create a README file."""
        readme_path = Path(path) / "README.md"
        readme_path.write_text(content)
        logger.info(f"Created README at: {readme_path}")
        return readme_path
    
    @staticmethod
    def create_gitignore(path: str, templates: List[str] = None) -> Path:
        """Create a .gitignore file."""
        if templates is None:
            templates = [
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                ".env",
                ".venv/",
                "venv/",
                "ENV/",
                "node_modules/",
                "dist/",
                "build/",
                "*.log",
                ".DS_Store"
            ]
        
        gitignore_content = "\n".join(templates)
        gitignore_path = Path(path) / ".gitignore"
        gitignore_path.write_text(gitignore_content)
        logger.info(f"Created .gitignore at: {gitignore_path}")
        return gitignore_path
