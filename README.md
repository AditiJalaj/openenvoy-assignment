# openenvoy-assignment# Lines of Code Counter


Assignment by Aditi Jalaj


A Python tool for counting lines of code in source files, supporting multiple programming languages.

## Features

- **Multi-language support**: Java, JavaScript, TypeScript, Python
- **Accurate counting**: Distinguishes between blank lines, comment lines, and code lines
- **Extensible design**: Easy to add support for new programming languages
- **Command-line interface**: Simple to use from the terminal
- **Comprehensive testing**: Full test suite with 24 test cases

## Usage

### Command Line

```bash
python line_counter.py <file_path>
```

Examples:

```bash
python line_counter.py Main.java
python line_counter.py script.js
python line_counter.py module.py
```

### Programmatic Usage

```python
from line_counter import LineCounter, JavaSyntax, detect_language

# Detect language automatically
syntax = detect_language("Main.java")
counter = LineCounter(syntax)

# Count lines
counts = counter.count_lines("Main.java")
print(f"Blank: {counts['blank']}")
print(f"Comments: {counts['comment']}")
print(f"Code: {counts['code']}")
print(f"Total: {counts['total']}")
```

## Supported Languages

- **Java** (.java)
- **JavaScript** (.js, .jsx)
- **TypeScript** (.ts, .tsx)
- **Python** (.py)

## Line Classification

The tool classifies each line as one of three types:

1. **Blank lines**: Lines containing only whitespace
2. **Comment lines**: Lines containing only comments (no code)
3. **Code lines**: Lines containing actual code (may include inline comments)

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
python test_line_counter.py
```

The test suite includes:

- Unit tests for each language syntax
- Edge case testing
- File I/O testing
- Integration tests

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
