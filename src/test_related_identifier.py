"""
Test-Related Code Detection Script
--------------------------------

This script identifies test functions and test files across multiple programming languages
using pattern matching. It helps filter out test code from production code during vulnerability
analysis or code review processes.

The FunctionTestAnalyzer class provides methods to:
1. Detect test functions based on language-specific patterns and conventions
2. Identify test files based on naming patterns

Supported Languages:
- Java: JUnit (@Test, @Before, @After, @BeforeEach, @AfterEach)
- C/C++: Google Test (TEST, TEST_F, TEST_P)
- C#: NUnit, MSTest, xUnit ([Test], [TestMethod], [Fact], [Theory])
- JavaScript: Jest, Mocha (test, it, describe, beforeEach, afterEach)
- Python: pytest, unittest (test_*, @pytest.mark, @unittest)

Usage Example:
    analyzer = FunctionTestAnalyzer()
    
    # Check if a function is test-related
    code = "@Test\npublic void testAdd() { assertEquals(4, 2 + 2); }"
    is_test = analyzer.is_test_function(code)
    
    # Check if a file is test-related
    filename = "test_calculator.py"
    is_test_file = analyzer.is_test_file(filename)

Test Function Detection Patterns:
- Java: Detects JUnit test methods with @Test, @Before, @After annotations
- C/C++: Detects Google Test macros (TEST, TEST_F, TEST_P)
- C#: Detects NUnit/MSTest/xUnit attributes ([Test], [Fact], [Theory])
- JavaScript: Detects Jest/Mocha test blocks (test(), it(), describe())
- Python: Detects pytest/unittest patterns (test_*, @pytest.mark, @unittest)

Test File Detection Patterns:
Files are identified as test-related if they match patterns like:
- Starts with 'test' or 'Test' (test_calculator.py, TestHelper.java)
- Ends with 'test' or 'Test' (calculator_test.cpp, CalculatorTest.cs)
- Contains 'Test' in the name (MyTestUtils.js)

Example Test Function Patterns:
    Java: @Test public void testAddition() { ... }
    Python: def test_calculation(): ...
    C++: TEST(CalculatorTest, AdditionWorks) { ... }
    JavaScript: test('addition', () => { ... })
    C#: [TestMethod] public void TestAddition() { ... }

Example Test File Names:
    - test_calculator.py (Python)
    - CalculatorTest.java (Java)
    - calculator_test.cpp (C++)
    - TestHelpers.cs (C#)
    - calculator.test.js (JavaScript)
"""

import re


class FunctionTestAnalyzer:
    def __init__(self):
        # Patterns to identify test function declarations
        self.function_patterns = {
            # Java test method patterns
            'java': [
                r'@Test\s+.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'@Before\s+.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'@After\s+.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'@BeforeEach\s+.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'@AfterEach\s+.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)'
            ],
            # C/C++ test function patterns
            'cpp': [
                r'TEST\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)',
                r'TEST_F\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)',
                r'TEST_P\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)'
            ],
            # C# test method patterns
            'csharp': [
                r'\[Test(?:Case)?\]\s*.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'\[TestMethod\]\s*.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'\[Fact\]\s*.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)',
                r'\[Theory\]\s*.*?(?:public\s+)?void\s+(\w+)\s*\([^\)]*\)'
            ],
            # JavaScript test function patterns
            'javascript': [
                r'test\s*\(\s*[\'"].*?[\'"]\s*,\s*(?:function|\([^\)]*\)\s*=>)',
                r'it\s*\(\s*[\'"].*?[\'"]\s*,\s*(?:function|\([^\)]*\)\s*=>)',
                r'describe\s*\(\s*[\'"].*?[\'"]\s*,\s*(?:function|\([^\)]*\)\s*=>)',
                r'beforeEach\s*\(\s*(?:function|\([^\)]*\)\s*=>)',
                r'afterEach\s*\(\s*(?:function|\([^\)]*\)\s*=>)'
            ],
            # Python test function patterns
            'python': [
                r'@pytest\.mark\..*?\s*def\s+(\w+)\s*\([^\)]*\):',
                r'@unittest\..*?\s*def\s+(\w+)\s*\([^\)]*\):',
                r'def\s+(test_\w+)\s*\([^\)]*\):',  # unittest style test_* functions
                r'@pytest\.fixture\s*.*?def\s+(\w+)\s*\([^\)]*\):',
                r'@pytest\.(?:mark\.)?parametrize\s*.*?def\s+(\w+)\s*\([^\)]*\):'
            ]
        }

        # Test indicators specifically for matching file names
        self.test_indicators = [
            r'^test',  # File starts with 'test'
            r'test$',  # File ends with 'test'
            r'Test',  # File contains 'Test'
            r'_test$',  # File ends with '_test'
            r'^test_',  # File starts with 'test_'
            r'_Test$',  # File ends with '_Test'
            r'^Test'  # File starts with 'Test'
        ]

    def is_test_function(self, function_code: str) -> bool:
        """
        Analyze if a function is test-related by checking against all language patterns.

        Args:
            function_code: Complete function code as string

        Returns:
            bool: True if the function is identified as a test function
        """
        # Check against all language patterns
        for patterns in self.function_patterns.values():
            for pattern in patterns:
                if re.search(pattern, function_code, re.MULTILINE):
                    return True
        return False

    def is_test_file(self, filename: str) -> bool:
        """
        Check if a file is test-related based on its name.

        Args:
            filename: Name of the file to check

        Returns:
            bool: True if the file appears to be test-related
        """
        for pattern in self.test_indicators:
            if re.search(pattern, filename, re.IGNORECASE):
                return True
        return False


# Example usage
if __name__ == "__main__":
    analyzer = FunctionTestAnalyzer()

    # Test function examples
    test_functions = [
        # Java
        ("@Test\npublic void testAdd() { assertEquals(4, 2 + 2); }", "Java test"),
        ("public void testAdd() { assertEquals(4, 2 + 2); }", "Java without @Test"),
        # Python
        ("def test_calculation():\n    assert calc(2, 2) == 4", "Python test"),
        ("@pytest.mark.parametrize('input,expected', [(1,2)])\ndef test_param(input, expected):",
         "Pytest parametrized test"),
        # JavaScript
        ("test('addition', () => { expect(add(2, 2)).toBe(4); })", "JavaScript test"),
        ("it('should add numbers', function() { expect(add(2, 2)).toBe(4); })", "JavaScript it block"),
        # C++
        ("TEST(CalculatorTest, AdditionWorks) { ASSERT_EQ(4, add(2, 2)); }", "C++ test"),
        ("TEST_F(CalculatorFixture, AdditionWorks) { ASSERT_EQ(4, add(2, 2)); }", "C++ fixture test"),
        # C#
        ("[TestMethod]\npublic void TestAddition() { Assert.AreEqual(4, Add(2, 2)); }", "C# test"),
        ("[Fact]\npublic void TestAddition() { Assert.Equal(4, Add(2, 2)); }", "C# fact test"),
        # Non-test functions
        ("public int add(int a, int b) { return a + b; }", "Regular Java function"),
        ("def calculate_test_score():\n    return total / count", "Regular Python function"),
        ("function processData(data) { return data * 2; }", "Regular JavaScript function")
    ]

    # Test file name examples
    test_files = [
        "test_calculator.py",
        "CalculatorTest.java",
        "calculator_test.cpp",
        "TestHelpers.cs",
        "calculator.py",
        "utils.js",
        "tests/helper.py",
        "src/main.py"
    ]

    print("\nTesting function detection:")
    for function_code, description in test_functions:
        is_test = analyzer.is_test_function(function_code)
        status = "TEST" if is_test else "NOT TEST"
        print(f"\n{description}:")
        print(f"Status: {status}")
        print(f"Code:\n{function_code}")

    print("\nTesting file name detection:")
    for filename in test_files:
        is_test = analyzer.is_test_file(filename)
        status = "TEST" if is_test else "NOT TEST"
        print(f"{filename}: {status}")
