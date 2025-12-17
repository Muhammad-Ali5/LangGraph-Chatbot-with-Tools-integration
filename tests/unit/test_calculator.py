"""
Unit Tests for Calculator Tool
Test File: tests/unit/test_calculator.py
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from langgraph_tool_backend import calculator_tool


class TestCalculatorTool:
    """Test suite for calculator_tool function"""
    
    # ==================== POSITIVE TEST CASES ====================
    
    def test_addition_positive_numbers(self):
        """
        TC_CALC_001: Verify successful addition of two positive numbers
        Test Type: Positive
        """
        # Arrange
        first_num = 25
        second_num = 37
        operation = "add"
        
        # Act
        result = calculator_tool.invoke({
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation
        })
        
        # Assert
        assert result == "25 + 37 = 62", f"Expected '25 + 37 = 62' but got '{result}'"
        assert "62" in result
    
    def test_subtraction_operation(self):
        """
        TC_CALC_002: Verify successful subtraction of two numbers
        Test Type: Positive
        """
        # Arrange
        first_num = 100
        second_num = 45
        operation = "subtract"
        
        # Act
        result = calculator_tool.invoke({
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation
        })
        
        # Assert
        assert result == "100 - 45 = 55", f"Expected '100 - 45 = 55' but got '{result}'"
        assert "55" in result
    
    def test_multiplication_operation(self):
        """
        TC_CALC_003: Verify successful multiplication of two numbers
        Test Type: Positive
        """
        # Arrange
        first_num = 12
        second_num = 8
        operation = "multiply"
        
        # Act
        result = calculator_tool.invoke({
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation
        })
        
        # Assert
        assert result == "12 × 8 = 96", f"Expected '12 × 8 = 96' but got '{result}'"
        assert "96" in result
    
    def test_division_operation(self):
        """
        TC_CALC_004: Verify successful division of two numbers
        Test Type: Positive
        """
        # Arrange
        first_num = 100
        second_num = 4
        operation = "divide"
        
        # Act
        result = calculator_tool.invoke({
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation
        })
        
        # Assert
        assert result == "100 ÷ 4 = 25.0", f"Expected '100 ÷ 4 = 25.0' but got '{result}'"
        assert "25.0" in result
    
    # ==================== NEGATIVE TEST CASES ====================
    
    def test_division_by_zero(self):
        """
        TC_CALC_005: Verify error handling for division by zero
        Test Type: Negative
        """
        # Arrange
        first_num = 50
        second_num = 0
        operation = "divide"
        
        # Act
        result = calculator_tool.invoke({
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation
        })
        
        # Assert
        assert "Error: Division by zero is not allowed" in result, \
            f"Expected error message but got '{result}'"
        assert "⚠️" in result or "Error" in result
    
    def test_invalid_operation(self):
        """
        TC_CALC_006: Verify error handling for unsupported operation
        Test Type: Negative
        """
        # Arrange
        first_num = 10
        second_num = 5
        operation = "modulo"
        
        # Act
        result = calculator_tool.invoke({
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation
        })
        
        # Assert
        assert "Unsupported operation" in result, \
            f"Expected unsupported operation error but got '{result}'"
        assert "modulo" in result
        assert "add, subtract, multiply, or divide" in result


class TestCalculatorEdgeCases:
    """Additional edge case tests for calculator tool"""
    
    def test_negative_numbers_addition(self):
        """Test addition with negative numbers"""
        result = calculator_tool.invoke({
            "first_num": -10,
            "second_num": 5,
            "operation": "add"
        })
        assert "-10 + 5 = -5" in result
    
    def test_decimal_numbers_multiplication(self):
        """Test multiplication with decimal numbers"""
        result = calculator_tool.invoke({
            "first_num": 2.5,
            "second_num": 4,
            "operation": "multiply"
        })
        assert "10" in result or "10.0" in result
    
    def test_large_numbers(self):
        """Test with large numbers"""
        result = calculator_tool.invoke({
            "first_num": 1000000,
            "second_num": 2000000,
            "operation": "add"
        })
        assert "3000000" in result


# ==================== PYTEST FIXTURES ====================

@pytest.fixture
def calculator_data():
    """Fixture providing test data"""
    return {
        "valid_operations": ["add", "subtract", "multiply", "divide"],
        "invalid_operations": ["modulo", "power", "root", "invalid"]
    }


# ==================== RUN TESTS ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])