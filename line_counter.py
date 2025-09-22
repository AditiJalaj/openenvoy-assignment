
import re
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from enum import Enum


class LineType(Enum):
    """Enumeration of line types that can be counted."""
    BLANK = "blank"
    COMMENT = "comment"
    CODE = "code"


class LanguageSyntax(ABC):
    """Abstract base class for language-specific syntax rules."""
    
    @abstractmethod
    def is_blank_line(self, line: str) -> bool:
        """Check if a line is blank (whitespace only)."""
        pass
    
    @abstractmethod
    def is_comment_line(self, line: str) -> bool:
        """Check if a line is a comment line (no code, only comments)."""
        pass
    
    @abstractmethod
    def get_language_name(self) -> str:
        """Get the name of the programming language."""
        pass


class JavaSyntax(LanguageSyntax):
    """Java language syntax rules."""
    
    def __init__(self):
        # Single-line comment pattern
        self.single_line_comment = re.compile(r'^\s*//')
        # Multi-line comment start/end patterns
        self.multi_line_start = re.compile(r'^\s*/\*')
        self.multi_line_end = re.compile(r'\*/\s*$')
    
    def is_blank_line(self, line: str) -> bool:
        """Check if a line is blank (whitespace only)."""
        return not line.strip()
    
    def is_comment_line(self, line: str) -> bool:
        """Check if a line is a comment line (no code, only comments)."""
        stripped = line.strip()
        
        # Empty line is not a comment
        if not stripped:
            return False
        
        # Check for single-line comment
        if self.single_line_comment.match(stripped):
            return True
        
        # Check for multi-line comment (only if it starts with /* or ends with */)
        # But not if it's inline (has code before the comment)
        if (self.multi_line_start.match(stripped) or 
            (self.multi_line_end.search(stripped) and not self.multi_line_start.search(stripped) and 
             not re.search(r'\S.*/\*', stripped))):
            return True
        
        # Check if line is only whitespace and comment
        # Remove single-line comment and check if anything remains
        without_single_comment = re.sub(r'//.*$', '', stripped)
        if without_single_comment.strip():
            return False
        
        return True
    
    def get_language_name(self) -> str:
        """Get the name of the programming language."""
        return "Java"


class JavaScriptSyntax(LanguageSyntax):
    """JavaScript language syntax rules."""
    
    def __init__(self):
        # Single-line comment pattern
        self.single_line_comment = re.compile(r'^\s*//')
        # Multi-line comment start/end patterns
        self.multi_line_start = re.compile(r'^\s*/\*')
        self.multi_line_end = re.compile(r'\*/\s*$')
    
    def is_blank_line(self, line: str) -> bool:
        """Check if a line is blank (whitespace only)."""
        return not line.strip()
    
    def is_comment_line(self, line: str) -> bool:
        """Check if a line is a comment line (no code, only comments)."""
        stripped = line.strip()
        
        # Empty line is not a comment
        if not stripped:
            return False
        
        # Check for single-line comment
        if self.single_line_comment.match(stripped):
            return True
        
        # Check for multi-line comment (only if it starts with /* or ends with */)
        if (self.multi_line_start.match(stripped) or 
            (self.multi_line_end.search(stripped) and not self.multi_line_start.search(stripped))):
            return True
        
        # Check if line is only whitespace and comment
        # Remove single-line comment and check if anything remains
        without_single_comment = re.sub(r'//.*$', '', stripped)
        if without_single_comment.strip():
            return False
        
        return True
    
    def get_language_name(self) -> str:
        """Get the name of the programming language."""
        return "JavaScript"


class PythonSyntax(LanguageSyntax):
    """Python language syntax rules."""
    
    def __init__(self):
        # Single-line comment pattern
        self.single_line_comment = re.compile(r'^\s*#')
        # Multi-line string patterns (docstrings)
        self.triple_quote_start = re.compile(r'^\s*"""')
        self.triple_quote_end = re.compile(r'"""\s*$')
    
    def is_blank_line(self, line: str) -> bool:
        """Check if a line is blank (whitespace only)."""
        return not line.strip()
    
    def is_comment_line(self, line: str) -> bool:
        """Check if a line is a comment line (no code, only comments)."""
        stripped = line.strip()
        
        # Empty line is not a comment
        if not stripped:
            return False
        
        # Check for single-line comment
        if self.single_line_comment.match(stripped):
            return True
        
        # Check for multi-line string (docstring) - only if it starts with """ or ends with """
        if (self.triple_quote_start.match(stripped) or 
            (self.triple_quote_end.search(stripped) and not self.triple_quote_start.search(stripped))):
            return True
        
        # Check if line is only whitespace and comment
        # Remove single-line comment and check if anything remains
        without_single_comment = re.sub(r'#.*$', '', stripped)
        if without_single_comment.strip():
            return False
        
        return True
    
    def get_language_name(self) -> str:
        """Get the name of the programming language."""
        return "Python"


class LineCounter:
    """Main class for counting lines of code."""
    
    def __init__(self, syntax: LanguageSyntax):
        """Initialize the line counter with a specific language syntax."""
        self.syntax = syntax
    
    def count_lines(self, file_path: str) -> Dict[str, int]:
        """
        Count lines in a source file.
        
        Args:
            file_path: Path to the source file
            
        Returns:
            Dictionary with counts for 'blank', 'comment', 'code', and 'total'
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")
        
        counts = {
            'blank': 0,
            'comment': 0,
            'code': 0,
            'total': len(lines)
        }
        
        in_multi_line_comment = False
        
        for line in lines:
            # Remove trailing newline for processing
            line = line.rstrip('\n\r')
            
            if self.syntax.is_blank_line(line):
                counts['blank'] += 1
            elif self.syntax.is_comment_line(line):
                counts['comment'] += 1
            else:
                counts['code'] += 1
        
        return counts
    
    def print_results(self, file_path: str, counts: Dict[str, int]) -> None:
        """Print the counting results in a formatted way."""
        print(f"Lines of code counter for {file_path}")
        print(f"Language: {self.syntax.get_language_name()}")
        print(f"Blank: {counts['blank']}")
        print(f"Comments: {counts['comment']}")
        print(f"Code: {counts['code']}")
        print(f"Total: {counts['total']}")


def detect_language(file_path: str) -> LanguageSyntax:
    """
    Detect the programming language based on file extension.
    
    Args:
        file_path: Path to the source file
        
    Returns:
        Appropriate LanguageSyntax instance
    """
    extension = file_path.lower().split('.')[-1]
    
    language_map = {
        'java': JavaSyntax,
        'js': JavaScriptSyntax,
        'jsx': JavaScriptSyntax,
        'ts': JavaScriptSyntax,
        'tsx': JavaScriptSyntax,
        'py': PythonSyntax,
    }
    
    if extension in language_map:
        return language_map[extension]()
    else:
        # Default to Java syntax for unknown extensions
        return JavaSyntax()


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) != 2:
        print("Usage: python line_counter.py <file_path>")
        print("Example: python line_counter.py Main.java")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # Detect language and create counter
        syntax = detect_language(file_path)
        counter = LineCounter(syntax)
        
        # Count lines
        counts = counter.count_lines(file_path)
        
        # Print results
        counter.print_results(file_path, counts)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
