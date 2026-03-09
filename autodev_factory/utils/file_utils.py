"""
File Utilities for AutoDev Factory
"""

import os
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def create_directory(path: str, exist_ok: bool = True) -> Path:
        """Create a directory if it doesn't exist."""
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=exist_ok)
        logger.info(f"Created directory: {dir_path}")
        return dir_path
    
    @staticmethod
    def write_file(path: str, content: str, overwrite: bool = True) -> Path:
        """Write content to a file."""
        file_path = Path(path)
        
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {file_path}")
        
        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(content)
        logger.info(f"Written file: {file_path}")
        return file_path
    
    @staticmethod
    def read_file(path: str) -> str:
        """Read content from a file."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return file_path.read_text()
    
    @staticmethod
    def copy_file(src: str, dst: str) -> Path:
        """Copy a file from src to dst."""
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        logger.info(f"Copied file: {src_path} -> {dst_path}")
        return dst_path
    
    @staticmethod
    def delete_file(path: str) -> bool:
        """Delete a file."""
        file_path = Path(path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
            return True
        return False
    
    @staticmethod
    def create_project_structure(base_path: str, structure: dict) -> Path:
        """
        Create a project structure from a dictionary.
        
        Example structure:
        {
            'src': {
                'components': {},
                'utils': {}
            },
            'tests': {},
            'README.md': '# Project'
        }
        """
        base = Path(base_path)
        base.mkdir(parents=True, exist_ok=True)
        
        for name, content in structure.items():
            path = base / name
            
            if isinstance(content, dict):
                # It's a directory
                if content:  # Has sub-items
                    FileUtils.create_project_structure(str(path), content)
                else:
                    # Empty directory
                    path.mkdir(exist_ok=True)
            else:
                # It's a file with content
                path.write_text(content or "")
        
        logger.info(f"Created project structure at: {base}")
        return base
    
    @staticmethod
    def get_file_size(path: str) -> int:
        """Get file size in bytes."""
        return Path(path).stat().st_size
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> list:
        """List files in a directory matching a pattern."""
        return [str(f) for f in Path(directory).glob(pattern)]
