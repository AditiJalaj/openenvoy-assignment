#!/usr/bin/env python3
"""
Unit tests for the Line Counter tool.
"""

import unittest
import tempfile
import os
from line_counter import LineCounter, JavaSyntax, JavaScriptSyntax, PythonSyntax, detect_language


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
        # Use the actual Main.java file
        temp_file = "Main.java"
        
        try:
            counts = self.counter.count_lines(temp_file)
            
            # Expected results based on the example
            self.assertEqual(counts['blank'], 3)
            self.assertEqual(counts['comment'], 3)
            self.assertEqual(counts['code'], 6)
            self.assertEqual(counts['total'], 12)
        except FileNotFoundError:
            self.fail("Main.java file not found")
    
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


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
