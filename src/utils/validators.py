"""
Input validation and sanitization utilities
"""
import re
from typing import List, Optional
from pathlib import Path


class QueryValidator:
    """Validates and sanitizes user queries"""

    # Dangerous SQL keywords that should not be in queries
    DANGEROUS_KEYWORDS = [
        "DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE",
        "INSERT", "UPDATE", "GRANT", "REVOKE", "EXEC",
        "EXECUTE", "SHUTDOWN", "KILL"
    ]

    @classmethod
    def is_safe_query(cls, query: str) -> bool:
        """
        Check if a query is safe (read-only)

        Args:
            query: SQL query string

        Returns:
            True if query is safe, False otherwise
        """
        query_upper = query.upper()

        # Check for dangerous keywords
        for keyword in cls.DANGEROUS_KEYWORDS:
            if re.search(rf'\b{keyword}\b', query_upper):
                return False

        return True

    @classmethod
    def sanitize_input(cls, text: str) -> str:
        """
        Sanitize user input to prevent injection attacks

        Args:
            text: User input string

        Returns:
            Sanitized string
        """
        # Remove null bytes
        text = text.replace('\x00', '')

        # Trim whitespace
        text = text.strip()

        return text

    @classmethod
    def validate_file_path(cls, file_path: str) -> bool:
        """
        Validate that a file path is safe and accessible

        Args:
            file_path: Path to validate

        Returns:
            True if path is valid
        """
        try:
            path = Path(file_path)

            # Check if path exists
            if not path.exists():
                return False

            # Check if it's a file (not directory)
            if not path.is_file():
                return False

            # Check file extension is allowed
            allowed_extensions = {
                '.txt', '.pdf', '.csv', '.xlsx', '.xls',
                '.json', '.md', '.doc', '.docx'
            }

            if path.suffix.lower() not in allowed_extensions:
                return False

            return True

        except Exception:
            return False

    @classmethod
    def validate_table_name(cls, table_name: str) -> bool:
        """
        Validate database table name

        Args:
            table_name: Name to validate

        Returns:
            True if valid table name
        """
        # Only allow alphanumeric, underscore, and dot (for schema.table)
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$'
        return bool(re.match(pattern, table_name))

    @classmethod
    def validate_column_name(cls, column_name: str) -> bool:
        """
        Validate database column name

        Args:
            column_name: Name to validate

        Returns:
            True if valid column name
        """
        # Only allow alphanumeric and underscore
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, column_name))


class FileValidator:
    """Validates uploaded files"""

    # Maximum file size (1GB)
    MAX_FILE_SIZE = 1024 * 1024 * 1024

    @classmethod
    def validate_file_size(cls, file_path: str) -> bool:
        """
        Check if file size is within limits

        Args:
            file_path: Path to file

        Returns:
            True if file size is acceptable
        """
        try:
            size = Path(file_path).stat().st_size
            return size <= cls.MAX_FILE_SIZE
        except Exception:
            return False

    @classmethod
    def get_file_extension(cls, file_path: str) -> Optional[str]:
        """
        Get file extension

        Args:
            file_path: Path to file

        Returns:
            File extension or None
        """
        try:
            return Path(file_path).suffix.lower()
        except Exception:
            return None


__all__ = ["QueryValidator", "FileValidator"]
