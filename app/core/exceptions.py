import sys
from typing import Type
from dataclasses import dataclass

@dataclass
class ErrorLocation:
    """
    Stores information about where an error occurred in the code.
    Using a dataclass makes the structure more explicit and maintainable.
    """
    filename: str
    line_number: int
    error_message: str

class CustomException(Exception):
    """
    A custom exception class that provides detailed error information
    including the file name and line number where the error occurred.
    
    Example usage:
        try:
            # Some code that might raise an error
            result = 1 / 0
        except Exception as e:
            raise CustomException(e)
    """
    
    def __init__(self, error: Exception) -> None:
        """
        Initialize the custom exception with error details.
        
        Args:
            error: The original exception that was raised
        """
        self.error_location = self._get_error_details(error)
        super().__init__(str(self))
    
    def _get_error_details(self, error: Exception) -> ErrorLocation:
        """
        Extract error details from the system's exception info.
        
        Args:
            error: The exception to analyze
            
        Returns:
            ErrorLocation object containing error details
        """
        _, _, exc_tb = sys.exc_info()
        if exc_tb is None:
            return ErrorLocation("unknown", 0, str(error))
            
        return ErrorLocation(
            filename=exc_tb.tb_frame.f_code.co_filename,
            line_number=exc_tb.tb_lineno,
            error_message=str(error)
        )
    
    def __str__(self) -> str:
        """
        Create a formatted error message string.
        
        Returns:
            Formatted error message with file, line number, and error details
        """
        return (
            f"Error occurred in file '{self.error_location.filename}' "
            f"at line {self.error_location.line_number}: "
            f"{self.error_location.error_message}"
        )