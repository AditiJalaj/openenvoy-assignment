#!/usr/bin/env python3
"""
Unit tests for the Line Counter tool.
"""

import unittest
import tempfile
import os
import shutil
from line_counter import LineCounter, JavaSyntax, JavaScriptSyntax, PythonSyntax, detect_language, GranularLineType


class TestJavaSyntax(unittest.TestCase):
    """Test cases for Java syntax detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.syntax = JavaSyntax()
    
    def test_blank_line_detection(self):
        """Test detection of blank lines."""
        self.assertTrue(self.syntax.is_blank_line(""))
        self.assertTrue(self.syntax.is_blank_line("   "))
        self.assertTrue(self.syntax.is_blank_line("\t\t"))
        self.assertTrue(self.syntax.is_blank_line("  \t  "))
        self.assertFalse(self.syntax.is_blank_line("public class Main"))
        self.assertFalse(self.syntax.is_blank_line("  // comment"))
    
    def test_single_line_comment_detection(self):
        """Test detection of single-line comments."""
        self.assertTrue(self.syntax.is_comment_line("// This is a comment"))
        self.assertTrue(self.syntax.is_comment_line("  // Indented comment"))
        self.assertTrue(self.syntax.is_comment_line("\t// Tab indented comment"))
        self.assertFalse(self.syntax.is_comment_line("System.out.println(); // inline comment"))
        self.assertFalse(self.syntax.is_comment_line("public class Main"))
        self.assertFalse(self.syntax.is_comment_line(""))
    
    def test_multi_line_comment_detection(self):
        """Test detection of multi-line comments."""
        self.assertTrue(self.syntax.is_comment_line("/* This is a comment */"))
        self.assertTrue(self.syntax.is_comment_line("  /* Indented comment */"))
        self.assertTrue(self.syntax.is_comment_line("/* Start of comment"))
        self.assertTrue(self.syntax.is_comment_line("End of comment */"))
        self.assertFalse(self.syntax.is_comment_line("int x = 5; /* inline comment */"))
    
    def test_language_name(self):
        """Test language name retrieval."""
        self.assertEqual(self.syntax.get_language_name(), "Java")
    
    def test_granular_classification(self):
        """Test granular line classification for Java."""
        # Import statements
        self.assertEqual(self.syntax.classify_line_granular("import java.util.*;"), GranularLineType.IMPORT)
        self.assertEqual(self.syntax.classify_line_granular("  import java.io.File;"), GranularLineType.IMPORT)
        
        # Class declarations
        self.assertEqual(self.syntax.classify_line_granular("public class Main {"), GranularLineType.CLASS_DECLARATION)
        self.assertEqual(self.syntax.classify_line_granular("  private static final class Helper {"), GranularLineType.CLASS_DECLARATION)
        
        # Method declarations
        self.assertEqual(self.syntax.classify_line_granular("public static void main(String[] args) {"), GranularLineType.METHOD_DECLARATION)
        self.assertEqual(self.syntax.classify_line_granular("  private int getValue() {"), GranularLineType.METHOD_DECLARATION)
        
        # Variable declarations
        self.assertEqual(self.syntax.classify_line_granular("int x = 5;"), GranularLineType.VARIABLE_DECLARATION)
        self.assertEqual(self.syntax.classify_line_granular("  String name = \"test\";"), GranularLineType.VARIABLE_DECLARATION)
        
        # Control flow
        self.assertEqual(self.syntax.classify_line_granular("if (condition) {"), GranularLineType.CONTROL_FLOW)
        self.assertEqual(self.syntax.classify_line_granular("  for (int i = 0; i < 10; i++) {"), GranularLineType.CONTROL_FLOW)
        
        # Return statements
        self.assertEqual(self.syntax.classify_line_granular("return result;"), GranularLineType.RETURN_STATEMENT)
        self.assertEqual(self.syntax.classify_line_granular("  return 42;"), GranularLineType.RETURN_STATEMENT)
        
        # Function calls
        self.assertEqual(self.syntax.classify_line_granular("System.out.println(\"Hello\");"), GranularLineType.FUNCTION_CALL)
        self.assertEqual(self.syntax.classify_line_granular("  obj.method();"), GranularLineType.FUNCTION_CALL)
        
        # Assignment statements
        self.assertEqual(self.syntax.classify_line_granular("x = y + z;"), GranularLineType.ASSIGNMENT)
        self.assertEqual(self.syntax.classify_line_granular("  result = calculate();"), GranularLineType.ASSIGNMENT)
        
        # Comments and blank lines
        self.assertEqual(self.syntax.classify_line_granular("// This is a comment"), GranularLineType.OTHER_CODE)
        self.assertEqual(self.syntax.classify_line_granular(""), GranularLineType.OTHER_CODE)


class TestJavaScriptSyntax(unittest.TestCase):
    """Test cases for JavaScript syntax detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.syntax = JavaScriptSyntax()
    
    def test_blank_line_detection(self):
        """Test detection of blank lines."""
        self.assertTrue(self.syntax.is_blank_line(""))
        self.assertTrue(self.syntax.is_blank_line("   "))
        self.assertFalse(self.syntax.is_blank_line("console.log('hello');"))
    
    def test_single_line_comment_detection(self):
        """Test detection of single-line comments."""
        self.assertTrue(self.syntax.is_comment_line("// This is a comment"))
        self.assertTrue(self.syntax.is_comment_line("  // Indented comment"))
        self.assertFalse(self.syntax.is_comment_line("console.log('hello'); // inline comment"))
    
    def test_language_name(self):
        """Test language name retrieval."""
        self.assertEqual(self.syntax.get_language_name(), "JavaScript")


class TestPythonSyntax(unittest.TestCase):
    """Test cases for Python syntax detection."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.syntax = PythonSyntax()
    
    def test_blank_line_detection(self):
        """Test detection of blank lines."""
        self.assertTrue(self.syntax.is_blank_line(""))
        self.assertTrue(self.syntax.is_blank_line("   "))
        self.assertFalse(self.syntax.is_blank_line("print('hello')"))
    
    def test_single_line_comment_detection(self):
        """Test detection of single-line comments."""
        self.assertTrue(self.syntax.is_comment_line("# This is a comment"))
        self.assertTrue(self.syntax.is_comment_line("  # Indented comment"))
        self.assertFalse(self.syntax.is_comment_line("print('hello')  # inline comment"))
    
    def test_docstring_detection(self):
        """Test detection of docstrings."""
        self.assertTrue(self.syntax.is_comment_line('""" This is a docstring """'))
        self.assertTrue(self.syntax.is_comment_line('  """ Indented docstring """'))
        self.assertTrue(self.syntax.is_comment_line('""" Start of docstring'))
        self.assertTrue(self.syntax.is_comment_line('End of docstring """'))
    
    def test_language_name(self):
        """Test language name retrieval."""
        self.assertEqual(self.syntax.get_language_name(), "Python")


class TestLineCounter(unittest.TestCase):
    """Test cases for the LineCounter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.syntax = JavaSyntax()
        self.counter = LineCounter(self.syntax)
    
    def test_count_java_example(self):
        """Test counting the provided Java example."""
        # Create a temporary file with the Java example
        java_code = """import java.util.*;

// file created on 1st Jan 2020
// author: @openenvoy
public class Main {

// This is another comment line
public static void main(String[] args) {
System.out.println("Hello world!"); // code, not comment 11
}
}
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            # Expected results based on the example
            self.assertEqual(counts['blank'], 2)
            self.assertEqual(counts['comment'], 3)
            self.assertEqual(counts['code'], 6)
            self.assertEqual(counts['total'], 11)
        finally:
            os.unlink(temp_file)
    
    def test_count_simple_java_file(self):
        """Test counting a simple Java file."""
        java_code = """public class Test {
    // This is a comment
    public void method() {
        System.out.println("Hello");
    }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 1)
            self.assertEqual(counts['code'], 5)
            self.assertEqual(counts['total'], 6)
        finally:
            os.unlink(temp_file)
    
    def test_count_file_with_blank_lines(self):
        """Test counting a file with blank lines."""
        java_code = """public class Test {

    // Comment line
    
    public void method() {
        System.out.println("Hello");
    }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            self.assertEqual(counts['blank'], 2)
            self.assertEqual(counts['comment'], 1)
            self.assertEqual(counts['code'], 5)
            self.assertEqual(counts['total'], 8)
        finally:
            os.unlink(temp_file)
    
    def test_count_empty_file(self):
        """Test counting an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 0)
            self.assertEqual(counts['code'], 0)
            self.assertEqual(counts['total'], 0)
        finally:
            os.unlink(temp_file)
    
    def test_count_file_not_found(self):
        """Test handling of non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.counter.count_lines("nonexistent.java")
    
    def test_print_results(self):
        """Test the print_results method."""
        counts = {'blank': 2, 'comment': 3, 'code': 5, 'total': 10}
        
        # Capture stdout
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            self.counter.print_results("test.java", counts)
            output = captured_output.getvalue()
            
            self.assertIn("Lines of code counter for test.java", output)
            self.assertIn("Language: Java", output)
            self.assertIn("Blank: 2", output)
            self.assertIn("Comments: 3", output)
            self.assertIn("Code: 5", output)
            self.assertIn("Total: 10", output)
        finally:
            sys.stdout = old_stdout


class TestLanguageDetection(unittest.TestCase):
    """Test cases for language detection."""
    
    def test_detect_java(self):
        """Test detection of Java files."""
        syntax = detect_language("Main.java")
        self.assertIsInstance(syntax, JavaSyntax)
        
        syntax = detect_language("Test.JAVA")
        self.assertIsInstance(syntax, JavaSyntax)
    
    def test_detect_javascript(self):
        """Test detection of JavaScript files."""
        syntax = detect_language("script.js")
        self.assertIsInstance(syntax, JavaScriptSyntax)
        
        syntax = detect_language("component.jsx")
        self.assertIsInstance(syntax, JavaScriptSyntax)
        
        syntax = detect_language("typescript.ts")
        self.assertIsInstance(syntax, JavaScriptSyntax)
        
        syntax = detect_language("react.tsx")
        self.assertIsInstance(syntax, JavaScriptSyntax)
    
    def test_detect_python(self):
        """Test detection of Python files."""
        syntax = detect_language("script.py")
        self.assertIsInstance(syntax, PythonSyntax)
        
        syntax = detect_language("module.PY")
        self.assertIsInstance(syntax, PythonSyntax)
    
    def test_detect_unknown_extension(self):
        """Test detection of unknown file extensions (defaults to Java)."""
        syntax = detect_language("file.unknown")
        self.assertIsInstance(syntax, JavaSyntax)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.syntax = JavaSyntax()
        self.counter = LineCounter(self.syntax)
    
    def test_inline_comments(self):
        """Test handling of inline comments."""
        java_code = """public class Test {
    public void method() {
        System.out.println("Hello"); // This is an inline comment
    }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            # The line with inline comment should be counted as code, not comment
            self.assertEqual(counts['comment'], 0)
            self.assertEqual(counts['code'], 5)
        finally:
            os.unlink(temp_file)
    
    def test_mixed_whitespace_blank_lines(self):
        """Test blank lines with various whitespace characters."""
        java_code = """public class Test {
    
    public void method() {
        System.out.println("Hello");
    }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            self.assertEqual(counts['blank'], 1)
            self.assertEqual(counts['code'], 5)
        finally:
            os.unlink(temp_file)
    
    def test_only_comments_file(self):
        """Test a file containing only comments."""
        java_code = """// This is a comment
// Another comment
// Yet another comment"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 3)
            self.assertEqual(counts['code'], 0)
            self.assertEqual(counts['total'], 3)
        finally:
            os.unlink(temp_file)


class TestAdvancedFeatures(unittest.TestCase):
    """Test cases for advanced features like multiple files and granular classification."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.syntax = JavaSyntax()
        self.counter = LineCounter(self.syntax)
        self.temp_dir = None
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_granular_counting(self):
        """Test granular line counting."""
        java_code = """import java.util.*;
// This is a comment
public class Test {
    private int value = 5;
    
    public void method() {
        if (value > 0) {
            System.out.println("Hello");
            return;
        }
    }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(java_code)
            temp_file = f.name
        
        try:
            counts = self.counter.count_lines(temp_file, granular=True)
            
            # Basic counts
            self.assertEqual(counts['blank'], 1)
            self.assertEqual(counts['comment'], 1)
            self.assertEqual(counts['code'], 10)
            self.assertEqual(counts['total'], 12)
            
            # Granular counts
            self.assertEqual(counts['import'], 1)
            self.assertEqual(counts['class_declaration'], 1)
            self.assertEqual(counts['method_declaration'], 1)
            self.assertEqual(counts['variable_declaration'], 1)
            self.assertEqual(counts['control_flow'], 1)
            self.assertEqual(counts['function_call'], 1)
            self.assertEqual(counts['return_statement'], 1)
            
        finally:
            os.unlink(temp_file)
    
    def test_multiple_files(self):
        """Test counting multiple files."""
        # Create temporary files
        java_code1 = """public class Test1 {
    public void method1() {
        System.out.println("Hello");
    }
}"""
        
        java_code2 = """public class Test2 {
    public void method2() {
        System.out.println("World");
    }
}"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f1:
            f1.write(java_code1)
            temp_file1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f2:
            f2.write(java_code2)
            temp_file2 = f2.name
        
        try:
            counts = self.counter.count_multiple_files([temp_file1, temp_file2])
            
            # Aggregated counts
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 0)
            self.assertEqual(counts['code'], 10)  # 5 lines per file
            self.assertEqual(counts['total'], 10)
            
        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)
    
    def test_directory_scanning(self):
        """Test directory scanning."""
        # Create temporary directory structure
        self.temp_dir = tempfile.mkdtemp()
        
        # Create subdirectory
        subdir = os.path.join(self.temp_dir, "subdir")
        os.makedirs(subdir)
        
        # Create Java files
        java_code1 = """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}"""
        
        java_code2 = """public class Helper {
    public void help() {
        System.out.println("Help");
    }
}"""
        
        # Write files
        with open(os.path.join(self.temp_dir, "Main.java"), 'w') as f:
            f.write(java_code1)
        
        with open(os.path.join(subdir, "Helper.java"), 'w') as f:
            f.write(java_code2)
        
        # Create a non-Java file (should be ignored)
        with open(os.path.join(self.temp_dir, "readme.txt"), 'w') as f:
            f.write("This is a readme file")
        
        try:
            counts = self.counter.count_directory(self.temp_dir, ['.java'])
            
            # Should count both Java files
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 0)
            self.assertEqual(counts['code'], 10)  # 5 lines per file
            self.assertEqual(counts['total'], 10)
            
        finally:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
    
    def test_mixed_language_files(self):
        """Test counting files with different languages."""
        # Create files with different extensions
        java_code = """public class JavaTest {
    public void method() {
        System.out.println("Java");
    }
}"""
        
        js_code = """function jsTest() {
    console.log("JavaScript");
}"""
        
        py_code = """def py_test():
    print("Python")"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f1:
            f1.write(java_code)
            temp_file1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f2:
            f2.write(js_code)
            temp_file2 = f2.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f3:
            f3.write(py_code)
            temp_file3 = f3.name
        
        try:
            counts = self.counter.count_multiple_files([temp_file1, temp_file2, temp_file3])
            
            # Should count all files
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 0)
            self.assertEqual(counts['code'], 10)  # 5+3+2 lines per file
            self.assertEqual(counts['total'], 10)
            
        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)
            os.unlink(temp_file3)
    
    def test_granular_classification_javascript(self):
        """Test granular classification for JavaScript."""
        js_syntax = JavaScriptSyntax()
        
        # Import statements
        self.assertEqual(js_syntax.classify_line_granular("import React from 'react';"), GranularLineType.IMPORT)
        self.assertEqual(js_syntax.classify_line_granular("const fs = require('fs');"), GranularLineType.IMPORT)
        
        # Class declarations
        self.assertEqual(js_syntax.classify_line_granular("class MyClass {"), GranularLineType.CLASS_DECLARATION)
        self.assertEqual(js_syntax.classify_line_granular("export class Component {"), GranularLineType.CLASS_DECLARATION)
        
        # Function declarations
        self.assertEqual(js_syntax.classify_line_granular("function myFunction() {"), GranularLineType.FUNCTION_DECLARATION)
        self.assertEqual(js_syntax.classify_line_granular("const arrow = () => {"), GranularLineType.FUNCTION_DECLARATION)
        
        # Variable declarations
        self.assertEqual(js_syntax.classify_line_granular("const name = 'test';"), GranularLineType.VARIABLE_DECLARATION)
        self.assertEqual(js_syntax.classify_line_granular("let count = 0;"), GranularLineType.VARIABLE_DECLARATION)
    
    def test_granular_classification_python(self):
        """Test granular classification for Python."""
        py_syntax = PythonSyntax()
        
        # Import statements
        self.assertEqual(py_syntax.classify_line_granular("import os"), GranularLineType.IMPORT)
        self.assertEqual(py_syntax.classify_line_granular("from sys import argv"), GranularLineType.IMPORT)
        
        # Class declarations
        self.assertEqual(py_syntax.classify_line_granular("class MyClass:"), GranularLineType.CLASS_DECLARATION)
        
        # Function declarations
        self.assertEqual(py_syntax.classify_line_granular("def my_function():"), GranularLineType.FUNCTION_DECLARATION)
        
        # Variable declarations
        self.assertEqual(py_syntax.classify_line_granular("name = 'test'"), GranularLineType.VARIABLE_DECLARATION)
        
        # Control flow
        self.assertEqual(py_syntax.classify_line_granular("if condition:"), GranularLineType.CONTROL_FLOW)
        self.assertEqual(py_syntax.classify_line_granular("for item in items:"), GranularLineType.CONTROL_FLOW)
    
    def test_error_handling_multiple_files(self):
        """Test error handling when processing multiple files."""
        # Test with non-existent file
        counts = self.counter.count_multiple_files(["nonexistent.java"])
        
        # Should return zero counts for non-existent files
        self.assertEqual(counts['blank'], 0)
        self.assertEqual(counts['comment'], 0)
        self.assertEqual(counts['code'], 0)
        self.assertEqual(counts['total'], 0)
    
    def test_empty_directory(self):
        """Test counting an empty directory."""
        self.temp_dir = tempfile.mkdtemp()
        
        try:
            counts = self.counter.count_directory(self.temp_dir)
            
            # Should return zero counts
            self.assertEqual(counts['blank'], 0)
            self.assertEqual(counts['comment'], 0)
            self.assertEqual(counts['code'], 0)
            self.assertEqual(counts['total'], 0)
            
        finally:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
