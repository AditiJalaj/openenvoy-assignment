
import re
import sys
import os
import glob
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
from enum import Enum
from pathlib import Path


class LineType(Enum):
    """Enumeration of line types that can be counted."""
    BLANK = "blank"
    COMMENT = "comment"
    CODE = "code"


class GranularLineType(Enum):
    """Enumeration of granular line types for detailed analysis."""
    IMPORT = "import"
    CLASS_DECLARATION = "class_declaration"
    METHOD_DECLARATION = "method_declaration"
    FUNCTION_DECLARATION = "function_declaration"
    VARIABLE_DECLARATION = "variable_declaration"
    FUNCTION_CALL = "function_call"
    CONTROL_FLOW = "control_flow"
    RETURN_STATEMENT = "return_statement"
    ASSIGNMENT = "assignment"
    OTHER_CODE = "other_code"


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
    
    def classify_line_granular(self, line: str) -> GranularLineType:
        """Classify a line into granular categories. Default implementation."""
        stripped = line.strip()
        
        if not stripped or self.is_blank_line(line):
            return GranularLineType.OTHER_CODE
        
        if self.is_comment_line(line):
            return GranularLineType.OTHER_CODE
        
        # Language-specific implementations can override this
        return GranularLineType.OTHER_CODE


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
    
    def classify_line_granular(self, line: str) -> GranularLineType:
        """Classify a Java line into granular categories."""
        stripped = line.strip()
        
        if not stripped or self.is_blank_line(line):
            return GranularLineType.OTHER_CODE
        
        if self.is_comment_line(line):
            return GranularLineType.OTHER_CODE
        
        # Import statements
        if re.match(r'^\s*import\s+', stripped):
            return GranularLineType.IMPORT
        
        # Class declarations
        if re.match(r'^\s*(public\s+|private\s+|protected\s+)?(static\s+)?(final\s+)?class\s+', stripped):
            return GranularLineType.CLASS_DECLARATION
        
        # Method declarations
        if re.match(r'^\s*(public\s+|private\s+|protected\s+)?(static\s+)?(final\s+)?(void|int|String|boolean|char|byte|short|long|float|double|\w+)\s+\w+\s*\(', stripped):
            return GranularLineType.METHOD_DECLARATION
        
        # Return statements (check before variable declarations)
        if re.match(r'^\s*return\s*', stripped):
            return GranularLineType.RETURN_STATEMENT
        
        # Control flow statements
        if re.match(r'^\s*(if|for|while|do|switch|case|catch|finally|try)\s*', stripped):
            return GranularLineType.CONTROL_FLOW
        
        # Variable declarations
        if re.match(r'^\s*(public\s+|private\s+|protected\s+)?(static\s+)?(final\s+)?(int|String|boolean|char|byte|short|long|float|double|\w+)\s+\w+\s*[=;]', stripped):
            return GranularLineType.VARIABLE_DECLARATION
        
        # Assignment statements (check before function calls to avoid conflicts)
        if '=' in stripped and not re.match(r'^\s*(if|for|while|do|switch|case|catch|finally|try|return)', stripped):
            return GranularLineType.ASSIGNMENT
        
        # Function calls (simplified detection)
        if re.search(r'\w+\s*\([^)]*\)', stripped) and not re.match(r'^\s*(if|for|while|do|switch|case|catch|finally|try)', stripped):
            return GranularLineType.FUNCTION_CALL
        
        return GranularLineType.OTHER_CODE


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
    
    def classify_line_granular(self, line: str) -> GranularLineType:
        """Classify a JavaScript line into granular categories."""
        stripped = line.strip()
        
        if not stripped or self.is_blank_line(line):
            return GranularLineType.OTHER_CODE
        
        if self.is_comment_line(line):
            return GranularLineType.OTHER_CODE
        
        # Import statements
        if re.match(r'^\s*(import\s+|const\s+\w+\s*=\s*require\s*\(|var\s+\w+\s*=\s*require\s*\()', stripped):
            return GranularLineType.IMPORT
        
        # Class declarations
        if re.match(r'^\s*(export\s+)?class\s+', stripped):
            return GranularLineType.CLASS_DECLARATION
        
        # Function declarations
        if re.match(r'^\s*(export\s+)?(function\s+\w+|const\s+\w+\s*=\s*\([^)]*\)\s*=>|const\s+\w+\s*=\s*function)', stripped):
            return GranularLineType.FUNCTION_DECLARATION
        
        # Variable declarations
        if re.match(r'^\s*(const|let|var)\s+\w+', stripped):
            return GranularLineType.VARIABLE_DECLARATION
        
        # Control flow statements
        if re.match(r'^\s*(if|for|while|do|switch|case|catch|finally|try)\s*', stripped):
            return GranularLineType.CONTROL_FLOW
        
        # Return statements
        if re.match(r'^\s*return\s+', stripped):
            return GranularLineType.RETURN_STATEMENT
        
        # Function calls
        if re.search(r'\w+\s*\([^)]*\)', stripped) and not re.match(r'^\s*(if|for|while|do|switch|case|catch|finally|try)', stripped):
            return GranularLineType.FUNCTION_CALL
        
        # Assignment statements
        if '=' in stripped and not re.match(r'^\s*(if|for|while|do|switch|case|catch|finally|try)', stripped):
            return GranularLineType.ASSIGNMENT
        
        return GranularLineType.OTHER_CODE


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
    
    def classify_line_granular(self, line: str) -> GranularLineType:
        """Classify a Python line into granular categories."""
        stripped = line.strip()
        
        if not stripped or self.is_blank_line(line):
            return GranularLineType.OTHER_CODE
        
        if self.is_comment_line(line):
            return GranularLineType.OTHER_CODE
        
        # Import statements
        if re.match(r'^\s*(import\s+|from\s+\w+\s+import)', stripped):
            return GranularLineType.IMPORT
        
        # Class declarations
        if re.match(r'^\s*class\s+\w+', stripped):
            return GranularLineType.CLASS_DECLARATION
        
        # Function declarations
        if re.match(r'^\s*def\s+\w+', stripped):
            return GranularLineType.FUNCTION_DECLARATION
        
        # Variable declarations (simplified - Python doesn't have explicit declarations)
        if re.match(r'^\s*\w+\s*=\s*[^=]', stripped) and not re.match(r'^\s*(if|for|while|def|class|import|from)', stripped):
            return GranularLineType.VARIABLE_DECLARATION
        
        # Control flow statements
        if re.match(r'^\s*(if|for|while|elif|else|try|except|finally|with)\s*', stripped):
            return GranularLineType.CONTROL_FLOW
        
        # Return statements
        if re.match(r'^\s*return\s+', stripped):
            return GranularLineType.RETURN_STATEMENT
        
        # Function calls
        if re.search(r'\w+\s*\([^)]*\)', stripped) and not re.match(r'^\s*(if|for|while|def|class|import|from)', stripped):
            return GranularLineType.FUNCTION_CALL
        
        # Assignment statements
        if '=' in stripped and not re.match(r'^\s*(if|for|while|def|class|import|from)', stripped):
            return GranularLineType.ASSIGNMENT
        
        return GranularLineType.OTHER_CODE


class LineCounter:
    """Main class for counting lines of code."""
    
    def __init__(self, syntax: LanguageSyntax):
        """Initialize the line counter with a specific language syntax."""
        self.syntax = syntax
        self.granular_counts = {}
    
    def count_lines(self, file_path: str, granular: bool = False) -> Dict[str, int]:
        """
        Count lines in a source file.
        
        Args:
            file_path: Path to the source file
            granular: Whether to include granular line classification
            
        Returns:
            Dictionary with counts for 'blank', 'comment', 'code', 'total', and optionally granular counts
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
        
        # Initialize granular counts if requested
        if granular:
            for granular_type in GranularLineType:
                counts[granular_type.value] = 0
        
        for line in lines:
            # Remove trailing newline for processing
            line = line.rstrip('\n\r')
            
            if self.syntax.is_blank_line(line):
                counts['blank'] += 1
            elif self.syntax.is_comment_line(line):
                counts['comment'] += 1
            else:
                counts['code'] += 1
                
                # Add granular classification if requested
                if granular:
                    granular_type = self.syntax.classify_line_granular(line)
                    counts[granular_type.value] += 1
        
        return counts
    
    def count_multiple_files(self, file_paths: List[str], granular: bool = False) -> Dict[str, int]:
        """
        Count lines across multiple files.
        
        Args:
            file_paths: List of file paths to process
            granular: Whether to include granular line classification
            
        Returns:
            Aggregated counts across all files
        """
        total_counts = {
            'blank': 0,
            'comment': 0,
            'code': 0,
            'total': 0
        }
        
        if granular:
            for granular_type in GranularLineType:
                total_counts[granular_type.value] = 0
        
        for file_path in file_paths:
            try:
                # Detect language for each file
                syntax = detect_language(file_path)
                counter = LineCounter(syntax)
                counts = counter.count_lines(file_path, granular)
                
                # Aggregate counts
                for key in total_counts:
                    total_counts[key] += counts.get(key, 0)
                    
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {str(e)}")
                continue
        
        return total_counts
    
    def count_directory(self, directory_path: str, extensions: Optional[List[str]] = None, granular: bool = False) -> Dict[str, int]:
        """
        Count lines across all files in a directory tree.
        
        Args:
            directory_path: Path to the directory to scan
            extensions: List of file extensions to include (e.g., ['.java', '.py'])
            granular: Whether to include granular line classification
            
        Returns:
            Aggregated counts across all files in the directory
        """
        if extensions is None:
            extensions = ['.java', '.js', '.jsx', '.ts', '.tsx', '.py']
        
        file_paths = []
        
        # Walk through directory tree
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file_path.endswith(ext) for ext in extensions):
                    file_paths.append(file_path)
        
        return self.count_multiple_files(file_paths, granular)
    
    def print_results(self, file_path: str, counts: Dict[str, int], granular: bool = False) -> None:
        """Print the counting results in a formatted way."""
        print(f"Lines of code counter for {file_path}")
        print(f"Language: {self.syntax.get_language_name()}")
        print(f"Blank: {counts['blank']}")
        print(f"Comments: {counts['comment']}")
        print(f"Code: {counts['code']}")
        print(f"Total: {counts['total']}")
        
        if granular:
            print("\nGranular breakdown:")
            for granular_type in GranularLineType:
                if granular_type.value in counts and counts[granular_type.value] > 0:
                    print(f"  {granular_type.value.replace('_', ' ').title()}: {counts[granular_type.value]}")
    
    def print_aggregated_results(self, source: str, counts: Dict[str, int], granular: bool = False) -> None:
        """Print aggregated results for multiple files or directories."""
        print(f"Lines of code counter for {source}")
        print(f"Blank: {counts['blank']}")
        print(f"Comments: {counts['comment']}")
        print(f"Code: {counts['code']}")
        print(f"Total: {counts['total']}")
        
        if granular:
            print("\nGranular breakdown:")
            for granular_type in GranularLineType:
                if granular_type.value in counts and counts[granular_type.value] > 0:
                    print(f"  {granular_type.value.replace('_', ' ').title()}: {counts[granular_type.value]}")


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
    if len(sys.argv) < 2:
        print("Usage: python line_counter.py <file_path_or_directory> [--granular] [--extensions ext1,ext2]")
        print("Examples:")
        print("  python line_counter.py Main.java")
        print("  python line_counter.py Main.java --granular")
        print("  python line_counter.py /path/to/directory --granular")
        print("  python line_counter.py /path/to/directory --extensions .java,.py")
        sys.exit(1)
    
    source_path = sys.argv[1]
    granular = "--granular" in sys.argv
    extensions = None
    
    # Parse extensions if provided
    if "--extensions" in sys.argv:
        try:
            ext_idx = sys.argv.index("--extensions")
            extensions = sys.argv[ext_idx + 1].split(",")
            extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        except (IndexError, ValueError):
            print("Error: --extensions requires a comma-separated list of extensions")
            sys.exit(1)
    
    try:
        if os.path.isfile(source_path):
            # Single file processing
            syntax = detect_language(source_path)
            counter = LineCounter(syntax)
            counts = counter.count_lines(source_path, granular)
            counter.print_results(source_path, counts, granular)
            
        elif os.path.isdir(source_path):
            # Directory processing
            counter = LineCounter(JavaSyntax())  # Dummy syntax for directory processing
            counts = counter.count_directory(source_path, extensions, granular)
            counter.print_aggregated_results(f"directory '{source_path}'", counts, granular)
            
        else:
            print(f"Error: '{source_path}' is not a valid file or directory")
            sys.exit(1)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
