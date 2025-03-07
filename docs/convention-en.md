# IRASA Python Style Guide

This guide covers Python code conventions adopted from [PEP 8](https://peps.python.org/pep-0008/). Following these conventions will help you write clean, consistent, and readable Python code.

# Table of Contents

1. [Naming Conventions](#1-naming-conventions)
   - 1.1 Variables
   - 1.2 Functions
   - 1.3 Classes
   - 1.4 Constants
   - 1.5 Modules and Packages
2. [Indentation and Spacing](#2-indentation-and-spacing)
   - 2.1 Indentation
   - 2.2 Spacing After Commas
   - 2.3 Spacing Around Operators
   - 2.4 Line Length
3. [Comments](#3-comments)
   - 3.1 Single-Line Comments
   - 3.2 Multi-Line Comments
   - 3.3 Docstrings
4. [Imports](#4-imports)
   - 4.1 Import Placement
   - 4.2 Import Style
5. [Functions and Classes](#5-functions-and-classes)
   - 5.1 Functions and Methods
   - 5.2 Classes
6. [Exception Handling](#6-exception-handling)
7. [Other Best Practices](#7-other-best-practices)
   - 7.1 Avoid Code Duplication
   - 7.2 Use Appropriate Data Types
   - 7.3 Use Type Annotations
8. [Code Formatting](#8-code-formatting)
   - 8.1 Separate Code Blocks
   - 8.2 Clear Control Structures
9. [Data Structures and Control Flow](#9-data-structures-and-control-flow)
10. [Conclusion](#10-conclusion)


## 1. Naming Conventions

### 1.1 Variables
- Use lowercase letters with words separated by underscores (`snake_case`).
  - Example: `my_variable`, `user_age`

### 1.2 Functions
- Functions should use `snake_case` (lowercase letters with underscores).
  - Example: `calculate_total()`, `get_user_input()`

### 1.3 Classes
- Use `PascalCase` (each word starts with an uppercase letter).
  - Example: `CustomerAccount`, `UserProfile`

### 1.4 Constants
- Use uppercase letters with words separated by underscores (`UPPER_SNAKE_CASE`).
  - Example: `MAX_VALUE`, `PI`

### 1.5 Modules and Packages
- Module names should be lowercase, with underscores used if necessary (`snake_case`).
  - Example: `math_utilities`, `data_processor`

## 2. Indentation and Spacing

### 2.1 Indentation
- Use 4 spaces per indentation level. Do not use tabs.

### 2.2 Spacing After Commas
- Add a space after each comma in arguments or list elements.
  - Example: `my_function(1, 2, 3)`, `list_of_values = [1, 2, 3]`

### 2.3 Spacing Around Operators
- Add one space around operators like `+`, `=`, `-`, `*`, etc.
  - Example: `x = 5 + 10`, `result = a * b`

### 2.4 Line Length
- Limit all lines to 79 characters for code, and 72 characters for docstrings.
- If a line is too long, break it into multiple lines using parentheses or backslashes (`\`).

## 3. Comments

### 3.1 Single-Line Comments
- Use single-line comments for short explanations. Start with a capital letter and include a space after the `#`.
  - Example: `# This is a single-line comment`

### 3.2 Multi-Line Comments
- Use block comments for longer explanations, with a `#` at the beginning of each line.
  - Example:
    ```python
    # This is a multi-line comment
    # explaining the function below
    ```

### 3.3 Docstrings
- Use docstrings to document modules, classes, functions, or methods. Enclose docstrings in triple quotes (`"""`).
  - Example:
    ```python
    def add(a, b):
        """
        Adds two numbers and returns the result.
        
        Parameters:
        a (int): The first number
        b (int): The second number
        
        Returns:
        int: The sum of the two numbers
        """
        return a + b
    ```

## 4. Imports

### 4.1 Import Placement
- All imports should be placed at the top of the file, before other code.
- Group imports into three categories:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

### 4.2 Import Style
- Prefer `import module` over `from module import *` to avoid polluting the namespace.

## 5. Functions and Classes

### 5.1 Functions and Methods
- Functions and methods should be named descriptively using `snake_case`.
- Functions should have docstrings describing what they do.

### 5.2 Classes
- Class names should use `PascalCase`.
- Classes should also have docstrings that explain their purpose.

## 6. Exception Handling

- Use `try` and `except` blocks for error handling.
- Avoid using `except:` without specifying the error type.
- If catching a specific type of error, mention the error type in the `except` clause.

  - Example:
    ```python
    try:
        value = int(input("Enter a number: "))
    except ValueError:
        print("Invalid input.")
    ```

## 7. Other Best Practices

### 7.1 Avoid Code Duplication
- Avoid code duplication by breaking down the code into reusable functions or classes.

### 7.2 Use Appropriate Data Types
- Use the correct data types to improve code clarity and avoid errors.

### 7.3 Use Type Annotations
- If using Python 3.5 or higher, consider using type annotations to describe the types of parameters and return values.
  - Example:
    ```python
    def add_numbers(a: int, b: int) -> int:
        return a + b
    ```

## 8. Code Formatting

### 8.1 Separate Code Blocks
- Use blank lines to separate different code blocks, improving readability.

### 8.2 Clear Control Structures
- Use control structures such as `if`, `for`, `while` clearly and avoid writing overly complicated code.

## 9. Data Structures and Control Flow

- Choose appropriate data structures for the task. Use `list`, `tuple`, `set`, or `dict` as needed.
- Consider using `list comprehensions` or `generator expressions` for concise and efficient code.

## 10. Conclusion

Following these conventions will help you write cleaner, more consistent, and maintainable Python code. Make sure to always adhere to these standards for better collaboration in software development.
