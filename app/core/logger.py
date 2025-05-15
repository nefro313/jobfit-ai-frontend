"""
Logging Configuration Module for AI Job Application Assistant

This module provides a comprehensive logging setup that combines:
1. Session-based logging (logs organized by timestamp)
2. Level-specific log files (debug.log, info.log, error.log)
3. Integration with application settings
4. Module-specific loggers for better traceability
5. Rotating file handlers to manage log file sizes
"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from app.core.config import settings
# Import settings conditionally to handle initialization order



class CustomLogger:
    """
    Custom logging class that provides:
    - Session-based logging directories (organized by timestamp)
    - Console output with simple formatting
    - Multiple log files with different levels and detailed formatting
    - Log rotation to manage file sizes
    """
    
    _instance = None  # Singleton instance
    _initialized = False  # Track if logger has been initialized
    
    @classmethod
    def get_instance(cls, **kwargs) -> 'CustomLogger':
        """Get or create the singleton logger instance"""
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance
    
    def __init__(
        self, 
        app_name: str = "job-assistant",
        log_dir: str = "logs",
        log_level: Optional[str] = None,
        enable_session_dirs: bool = True,
        console_level: Optional[str] = None
    ):
        """
        Initialize the custom logger.
        
        Args:
            app_name: Name of the application for the root logger
            log_dir: Directory to store log files
            log_level: Overall log level (from settings or override)
            enable_session_dirs: Create timestamp subdirectories for logs
            console_level: Specific level for console output
        """
        # Skip if already initialized (singleton pattern)
        if self._initialized:
            return
            
        self.app_name = app_name
        self.log_dir = Path(log_dir)
        self.log_level = log_level or getattr(settings, 'LOG_LEVEL', 'INFO')
        self.enable_session_dirs = enable_session_dirs
        
        # Determine numeric log level
        self.numeric_level = self._get_numeric_level(self.log_level)
        
        # Console specific level (default to same as overall)
        self.console_level = self._get_numeric_level(console_level or self.log_level)
        
        # Create base log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create session directory if enabled
        if self.enable_session_dirs:
            self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.session_dir = self.log_dir / self.timestamp
            self.session_dir.mkdir(exist_ok=True)
            self.log_path = self.session_dir
        else:
            self.log_path = self.log_dir
        
        # Initialize root logger
        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(self.numeric_level)
        
        # Clear existing handlers to avoid duplicates
        self.root_logger.handlers = []
        
        # Initialize handlers
        self._setup_console_handler()
        self._setup_file_handlers()
        
        # Mark as initialized
        CustomLogger._initialized = True
        
        # Log startup message
        self.root_logger.info(f"Logging initialized at level: {self.log_level}")
        self.root_logger.info(f"Log files location: {self.log_path}")
    
    def _get_numeric_level(self, level_name: str) -> int:
        """Convert string log level to numeric value"""
        numeric_level = getattr(logging, level_name.upper(), None)
        if not isinstance(numeric_level, int):
            print(f"Invalid log level: {level_name}, defaulting to INFO")
            return logging.INFO
        return numeric_level
    
    def _setup_console_handler(self):
        """Set up console handler with simple formatting"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.console_level)
        
        console_format = logging.Formatter(
            '%(asctime)s - %(levelname)-8s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.root_logger.addHandler(console_handler)
    
    def _setup_file_handlers(self):
        """Set up file handlers for different log levels"""
        handlers = {
            'debug': (logging.DEBUG, 'debug.log'),
            'info': (logging.INFO, 'info.log'),
            'warning': (logging.WARNING, 'warning.log'),
            'error': (logging.ERROR, 'error.log')
        }
        
        detailed_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(filename)s:%(lineno)d:%(funcName)s] - '
            '%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        for name, (level, filename) in handlers.items():
            # Skip handlers for levels below the configured level
            if level < self.numeric_level:
                continue
                
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_path / filename,
                maxBytes=10*1024*1024,  # 10 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(detailed_format)
            self.root_logger.addHandler(file_handler)
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: Name of the module requesting the logger
                  If None, returns the root logger
                  
        Returns:
            logging.Logger: Logger instance for the specified module
        """
        if name is None:
            return self.root_logger
        return logging.getLogger(name)


# Global functions for easy access

def setup_logging(
    app_name: str = "job-assistant",
    log_dir: str = "logs",
    log_level: Optional[str] = None,
    enable_session_dirs: bool = True,
    console_level: Optional[str] = None
) -> logging.Logger:
    """
    Configure and initialize the logging system.
    
    Args:
        app_name: Name of the application
        log_dir: Directory to store log files
        log_level: Overall logging level
        enable_session_dirs: Whether to create timestamp subdirectories
        console_level: Specific level for console output
        
    Returns:
        logging.Logger: Root logger instance
    """
    custom_logger = CustomLogger.get_instance(
        app_name=app_name,
        log_dir=log_dir,
        log_level=log_level,
        enable_session_dirs=enable_session_dirs,
        console_level=console_level
    )
    return custom_logger.get_logger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module requesting the logger
              If None, returns the root logger
              
    Returns:
        logging.Logger: Logger instance for the specified module
    """
    # Ensure the custom logger is initialized
    if not CustomLogger._initialized:
        setup_logging()
    
    # Return the requested logger
    return CustomLogger.get_instance().get_logger(name)