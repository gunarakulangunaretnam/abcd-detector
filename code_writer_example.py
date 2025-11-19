#!/usr/bin/env python3
"""
Example: Writing and Testing Python Files Programmatically
This script demonstrates how to:
1. Write Python code to a file
2. Test the generated Python file
3. Execute and validate the code
"""

import os
import sys
import subprocess
import importlib.util


def write_python_file(filename, code_content):
    """
    Write Python code to a file
    
    Args:
        filename (str): Name of the file to create
        code_content (str): Python code to write
    """
    with open(filename, 'w') as f:
        f.write(code_content)
    print(f"✓ Successfully wrote {filename}")


def test_syntax(filename):
    """
    Test if the Python file has valid syntax
    
    Args:
        filename (str): Python file to test
    
    Returns:
        bool: True if syntax is valid, False otherwise
    """
    try:
        with open(filename, 'r') as f:
            compile(f.read(), filename, 'exec')
        print(f"✓ Syntax check passed for {filename}")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {filename}: {e}")
        return False


def run_python_file(filename):
    """
    Execute a Python file and capture output
    
    Args:
        filename (str): Python file to run
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            [sys.executable, filename],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"✓ Executed {filename}")
        print(f"  Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"  Errors: {result.stderr.strip()}")
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print(f"✗ Execution timeout for {filename}")
        return -1, "", "Timeout"
    except Exception as e:
        print(f"✗ Error executing {filename}: {e}")
        return -1, "", str(e)


def import_and_test_module(filename):
    """
    Import a Python file as a module and test its functions
    
    Args:
        filename (str): Python file to import
    
    Returns:
        module: Imported module object
    """
    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location("dynamic_module", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✓ Successfully imported {filename} as module")
        return module
    except Exception as e:
        print(f"✗ Error importing {filename}: {e}")
        return None


def test_function_output(module, function_name, args, expected_output):
    """
    Test a specific function from an imported module
    
    Args:
        module: The imported module
        function_name (str): Name of function to test
        args (tuple): Arguments to pass to function
        expected_output: Expected return value
    
    Returns:
        bool: True if test passed, False otherwise
    """
    try:
        func = getattr(module, function_name)
        result = func(*args)
        if result == expected_output:
            print(f"✓ Test passed: {function_name}{args} = {result}")
            return True
        else:
            print(f"✗ Test failed: {function_name}{args}")
            print(f"  Expected: {expected_output}, Got: {result}")
            return False
    except Exception as e:
        print(f"✗ Error testing {function_name}: {e}")
        return False


# ============================================
# EXAMPLE 1: Simple Calculator
# ============================================
def example_1_simple_calculator():
    print("\n" + "="*50)
    print("EXAMPLE 1: Creating and Testing a Simple Calculator")
    print("="*50)
    
    calculator_code = '''"""
Simple Calculator Module
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    # Test when run directly
    print("Testing Calculator:")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"20 / 5 = {divide(20, 5)}")
'''
    
    filename = "calculator.py"
    
    # Step 1: Write the file
    write_python_file(filename, calculator_code)
    
    # Step 2: Test syntax
    if not test_syntax(filename):
        return
    
    # Step 3: Run the file directly
    print("\n--- Running file directly ---")
    run_python_file(filename)
    
    # Step 4: Import and test specific functions
    print("\n--- Testing specific functions ---")
    module = import_and_test_module(filename)
    if module:
        test_function_output(module, "add", (5, 3), 8)
        test_function_output(module, "subtract", (10, 4), 6)
        test_function_output(module, "multiply", (6, 7), 42)
        test_function_output(module, "divide", (20, 5), 4.0)
    
    # Clean up
    os.remove(filename)
    print(f"\n✓ Cleaned up {filename}")


# ============================================
# EXAMPLE 2: Data Processor
# ============================================
def example_2_data_processor():
    print("\n" + "="*50)
    print("EXAMPLE 2: Creating and Testing a Data Processor")
    print("="*50)
    
    data_processor_code = '''"""
Data Processor Module
"""

def filter_even_numbers(numbers):
    """Filter and return only even numbers"""
    return [n for n in numbers if n % 2 == 0]

def calculate_average(numbers):
    """Calculate average of a list of numbers"""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def find_max_min(numbers):
    """Find maximum and minimum values"""
    if not numbers:
        return None, None
    return max(numbers), min(numbers)

if __name__ == "__main__":
    # Test when run directly
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Data: {data}")
    print(f"Even numbers: {filter_even_numbers(data)}")
    print(f"Average: {calculate_average(data)}")
    print(f"Max, Min: {find_max_min(data)}")
'''
    
    filename = "data_processor.py"
    
    # Step 1: Write the file
    write_python_file(filename, data_processor_code)
    
    # Step 2: Test syntax
    if not test_syntax(filename):
        return
    
    # Step 3: Run the file directly
    print("\n--- Running file directly ---")
    run_python_file(filename)
    
    # Step 4: Import and test specific functions
    print("\n--- Testing specific functions ---")
    module = import_and_test_module(filename)
    if module:
        test_function_output(module, "filter_even_numbers", ([1, 2, 3, 4, 5],), [2, 4])
        test_function_output(module, "calculate_average", ([10, 20, 30],), 20.0)
        test_function_output(module, "find_max_min", ([5, 1, 9, 3],), (9, 1))
    
    # Clean up
    os.remove(filename)
    print(f"\n✓ Cleaned up {filename}")


# ============================================
# EXAMPLE 3: Writing Test Files
# ============================================
def example_3_unittest_generation():
    print("\n" + "="*50)
    print("EXAMPLE 3: Generating and Running Unit Tests")
    print("="*50)
    
    # First, create the module to test
    string_utils_code = '''"""
String Utilities Module
"""

def reverse_string(s):
    """Reverse a string"""
    return s[::-1]

def is_palindrome(s):
    """Check if string is a palindrome"""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(s):
    """Count vowels in a string"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)
'''
    
    # Now create the test file
    test_code = '''"""
Unit Tests for String Utilities
"""
import unittest
from string_utils import reverse_string, is_palindrome, count_vowels

class TestStringUtils(unittest.TestCase):
    
    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("Python"), "nohtyP")
        self.assertEqual(reverse_string(""), "")
    
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(is_palindrome("hello"))
    
    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("Python"), 1)
        self.assertEqual(count_vowels("aeiou"), 5)

if __name__ == "__main__":
    unittest.main()
'''
    
    # Write both files
    write_python_file("string_utils.py", string_utils_code)
    write_python_file("test_string_utils.py", test_code)
    
    # Test syntax for both
    if test_syntax("string_utils.py") and test_syntax("test_string_utils.py"):
        # Run the unit tests
        print("\n--- Running unit tests ---")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "test_string_utils.py"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print("✓ All tests passed!")
        else:
            print("✗ Some tests failed")
    
    # Clean up
    for f in ["string_utils.py", "test_string_utils.py"]:
        if os.path.exists(f):
            os.remove(f)
    # Clean up pycache
    if os.path.exists("__pycache__"):
        import shutil
        shutil.rmtree("__pycache__")
    print(f"\n✓ Cleaned up generated files")


# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("Python File Writer and Tester Demo")
    print("="*50)
    
    # Run all examples
    example_1_simple_calculator()
    example_2_data_processor()
    example_3_unittest_generation()
    
    print("\n" + "="*50)
    print("All examples completed!")
    print("="*50)
