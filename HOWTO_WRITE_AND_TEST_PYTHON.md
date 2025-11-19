# How to Write and Test Python Files Programmatically

## Overview
This guide explains how to create Python programs that can dynamically write and test Python code files.

## Key Concepts

### 1. **Writing Python Files**
Use Python's built-in file operations to write code:

```python
def write_python_file(filename, code_content):
    with open(filename, 'w') as f:
        f.write(code_content)
```

### 2. **Testing Syntax**
Validate Python syntax before execution using the `compile()` function:

```python
def test_syntax(filename):
    try:
        with open(filename, 'r') as f:
            compile(f.read(), filename, 'exec')
        return True
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        return False
```

### 3. **Running Python Files**
Execute Python files as subprocesses and capture output:

```python
import subprocess
import sys

def run_python_file(filename):
    result = subprocess.run(
        [sys.executable, filename],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.returncode, result.stdout, result.stderr
```

### 4. **Dynamic Module Import**
Import and test functions from generated files:

```python
import importlib.util

def import_and_test_module(filename):
    spec = importlib.util.spec_from_file_location("dynamic_module", filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

### 5. **Function Testing**
Test specific functions with assertions:

```python
def test_function_output(module, function_name, args, expected_output):
    func = getattr(module, function_name)
    result = func(*args)
    assert result == expected_output, f"Expected {expected_output}, got {result}"
```

## Complete Workflow

```
1. Generate Code String
   ↓
2. Write to File
   ↓
3. Syntax Validation
   ↓
4. Execute/Import
   ↓
5. Test Functions
   ↓
6. Clean Up (optional)
```

## Practical Example

```python
# 1. Define the code to generate
calculator_code = '''
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
'''

# 2. Write to file
with open('calculator.py', 'w') as f:
    f.write(calculator_code)

# 3. Import and test
import importlib.util
spec = importlib.util.spec_from_file_location("calc", "calculator.py")
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)

# 4. Test functions
assert calc.add(2, 3) == 5
assert calc.multiply(4, 5) == 20
print("All tests passed!")
```

## Advanced: Unit Test Generation

You can also generate unittest files programmatically:

```python
test_code = '''
import unittest
from calculator import add, multiply

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20)

if __name__ == "__main__":
    unittest.main()
'''

with open('test_calculator.py', 'w') as f:
    f.write(test_code)

# Run tests
import subprocess
subprocess.run([sys.executable, '-m', 'unittest', 'test_calculator.py'])
```

## Use Cases

1. **Code Generation Tools**: Generate boilerplate code, API clients, or data models
2. **Testing Frameworks**: Dynamically create test cases based on configurations
3. **Education**: Create interactive coding tutorials that generate and test code
4. **Template Systems**: Generate code from templates with variable substitution
5. **CI/CD Pipelines**: Automatically generate and test configuration files

## Best Practices

✅ **Always validate syntax** before execution  
✅ **Use subprocess with timeout** to prevent hanging  
✅ **Clean up generated files** after testing  
✅ **Handle exceptions** gracefully  
✅ **Use context managers** for file operations  
✅ **Capture stdout/stderr** for debugging  

## Running the Demo

Run the complete demonstration:

```bash
python3 code_writer_example.py
```

This will show three examples:
1. Simple calculator with function testing
2. Data processor with list operations
3. Unit test generation and execution

## Security Note

⚠️ **Warning**: Dynamically executing generated code can be dangerous. Always:
- Validate and sanitize input
- Run in isolated environments
- Never execute untrusted code
- Use proper error handling

---

**See `code_writer_example.py` for a complete working implementation!**
