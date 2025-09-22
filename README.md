# openenvoy-assignment# Lines of Code Counter


Assignment by Aditi Jalaj

A Python tool for counting lines of code in source files, supporting multiple programming languages.

## Features

- **Multi-language support**: Java, JavaScript, TypeScript, Python
- **Accurate counting**: Distinguishes between blank lines, comment lines, and code lines
- **Granular classification**: Detailed breakdown of code types (imports, classes, methods, etc.)
- **Multiple files support**: Process single files, multiple files, or entire directories
- **Directory scanning**: Recursive directory traversal with file filtering
- **Extensible design**: Easy to add support for new programming languages
- **Command-line interface**: Simple to use from the terminal
- **Comprehensive testing**: Full test suite with 33 test cases

## Usage

### Command Line

```bash
python line_counter.py <file_path_or_directory> [--granular] [--extensions ext1,ext2]
```


Examples:

```bash
# Single file
python line_counter.py Main.java
python line_counter.py script.js
python line_counter.py module.py

# Single file with granular breakdown
python line_counter.py Main.java --granular

# Directory scanning
python line_counter.py /path/to/project --granular
python line_counter.py /path/to/project --extensions .java,.py
python line_counter.py /path/to/project --granular --extensions .js,.ts
```

### Programmatic Usage

```python
from line_counter import LineCounter, JavaSyntax, detect_language


# Single file with basic counting
syntax = detect_language("Main.java")
counter = LineCounter(syntax)
counts = counter.count_lines("Main.java")
print(f"Blank: {counts['blank']}")
print(f"Comments: {counts['comment']}")
print(f"Code: {counts['code']}")
print(f"Total: {counts['total']}")

# Single file with granular counting
counts = counter.count_lines("Main.java", granular=True)
print(f"Imports: {counts['import']}")
print(f"Classes: {counts['class_declaration']}")
print(f"Methods: {counts['method_declaration']}")

# Multiple files
file_paths = ["file1.java", "file2.js", "file3.py"]
counts = counter.count_multiple_files(file_paths, granular=True)

# Directory scanning
counts = counter.count_directory("/path/to/project", [".java", ".py"], granular=True)
```

## Supported Languages

- **Java** (.java)
- **JavaScript** (.js, .jsx)
- **TypeScript** (.ts, .tsx)
- **Python** (.py)

## Line Classification

### Basic Classification

The tool classifies each line as one of three basic types:

1. **Blank lines**: Lines containing only whitespace
2. **Comment lines**: Lines containing only comments (no code)
3. **Code lines**: Lines containing actual code (may include inline comments)

### Granular Classification (with --granular flag)

When using the `--granular` flag, code lines are further classified into:

- **Import**: Import statements (`import`, `from`, `require`, etc.)
- **Class Declaration**: Class definitions
- **Method Declaration**: Method/function definitions
- **Function Declaration**: Function definitions (JavaScript/Python)
- **Variable Declaration**: Variable declarations
- **Function Call**: Function/method calls
- **Control Flow**: `if`, `for`, `while`, `switch`, etc.
- **Return Statement**: `return` statements
- **Assignment**: Assignment operations
- **Other Code**: Other code that doesn't fit the above categories


## Example Output

For the provided Java example:

```java
import java.util.*;

// file created on 1st Jan 2020
// author: @openenvoy
public class Main {

// This is another comment line
public static void main(String[] args) {
System.out.println("Hello world!"); // code, not comment 11
}
}
```

Output:

```
Lines of code counter for Main.java
Language: Java
Blank: 3
Comments: 3
Code: 6
Total: 12
```

## Architecture

The tool is designed with extensibility in mind:

- **`LanguageSyntax`**: Abstract base class for language-specific rules
- **`LineCounter`**: Main counting logic
- **Language implementations**: `JavaSyntax`, `JavaScriptSyntax`, `PythonSyntax`

### Adding New Languages

To add support for a new language, create a new class inheriting from `LanguageSyntax`:

```python
class NewLanguageSyntax(LanguageSyntax):
    def __init__(self):
        # Define comment patterns
        self.single_line_comment = re.compile(r'^\s*#')
        # ... other patterns

    def is_blank_line(self, line: str) -> bool:
        # Implement blank line detection
        pass

    def is_comment_line(self, line: str) -> bool:
        # Implement comment line detection
        pass

    def get_language_name(self) -> str:
        return "NewLanguage"
```

## Testing

Run the test suite:

```bash
python unit_test.py
```

The test suite includes:

- Unit tests for each language syntax
- Edge case testing
- File I/O testing
- Integration tests

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Advanced Features

### ✅ **Implemented Features:**

- **Multiple files support**: Process multiple files at once
- **Directory scanning**: Recursive directory traversal with file filtering
- **Granular classification**: Detailed breakdown of code types
- **Multi-line comment support**: Basic support for `/* */` and `"""` comments
- **Language auto-detection**: Automatic language detection by file extension
- **Error handling**: Graceful handling of file errors and missing files

### 🔮 **Future Enhancements:**

- **Configuration file support**: YAML/JSON configuration files
- **Additional language support**: C/C++, Go, Rust, etc.
- **Advanced multi-line comment parsing**: Full multi-line comment block detection
- **Code complexity metrics**: Cyclomatic complexity, nesting depth
- **Output formats**: JSON, CSV, XML output options
- **IDE integration**: VS Code extension, IntelliJ plugin
