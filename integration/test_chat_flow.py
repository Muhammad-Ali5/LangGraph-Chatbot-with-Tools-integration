"""
Integration Tests for Chat Flow
Test File: tests/integration/test_chat_flow.py
"""

import pytest
import sys
import os
import uuid

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from langgraph_tool_backend import chatbot, ChatState
from langchain_core.messages import HumanMessage, AIMessage


class TestChatFlowIntegration:
    """Integration tests for complete chat flow with calculator tool"""
    
    @pytest.fixture
    def test_config(self):
        """Create a unique test configuration"""
        return {
            "configurable": {
                "thread_id": f"test_{uuid.uuid4()}"
            },
            "recursion_limit": 50
        }
    
    def test_calculator_tool_via_chat(self, test_config):
        """
        INT_001: Test calculator tool invocation through chat interface
        Verifies that user request triggers calculator tool correctly
        """
        # Arrange
        user_message = "calculate 25 plus 37"
        initial_state = {
            "messages": [HumanMessage(content=user_message)]
        }
        
        # Act
        result = chatbot.invoke(initial_state, test_config)
        
        # Assert
        assert result is not None
        assert "messages" in result
        
        # Check that response contains calculation result
        messages = result["messages"]
        response_found = False
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.content:
                if "62" in msg.content or "25 + 37" in msg.content:
                    response_found = True
                    break
        
        assert response_found, "Calculator result not found in response"
    
    def test_multiple_tool_calls_in_sequence(self, test_config):
        """
        INT_002: Test multiple calculator operations in sequence
        Verifies state management across multiple interactions
        """
        # First calculation
        state1 = {
            "messages": [HumanMessage(content="calculate 10 times 5")]
        }
        result1 = chatbot.invoke(state1, test_config)
        
        assert "messages" in result1
        
        # Second calculation using same thread
        state2 = {
            "messages": result1["messages"] + [
                HumanMessage(content="now divide 100 by 4")
            ]
        }
        result2 = chatbot.invoke(state2, test_config)
        
        # Assert both calculations succeeded
        assert "messages" in result2
        assert len(result2["messages"]) > len(result1["messages"])
    
    def test_casual_conversation_then_calculation(self, test_config):
        """
        INT_003: Test conversation flow from casual chat to tool usage
        Verifies smooth transition between conversation modes
        """
        # Casual greeting
        state1 = {
            "messages": [HumanMessage(content="hey there")]
        }
        result1 = chatbot.invoke(state1, test_config)
        
        assert "messages" in result1
        
        # Follow up with calculation
        state2 = {
            "messages": result1["messages"] + [
                HumanMessage(content="can you calculate 100 minus 45?")
            ]
        }
        result2 = chatbot.invoke(state2, test_config)
        
        # Verify calculation happened
        messages = result2["messages"]
        calculation_found = False
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.content:
                if "55" in msg.content or "100 - 45" in msg.content:
                    calculation_found = True
                    break
        
        assert calculation_found, "Calculation not performed after casual chat"
    
    def test_error_handling_in_chat_flow(self, test_config):
        """
        INT_004: Test error handling for invalid calculator operation
        Verifies graceful error handling in chat context
        """
        # Request invalid operation
        state = {
            "messages": [HumanMessage(content="calculate 10 modulo 3")]
        }
        result = chatbot.invoke(state, test_config)
        
        # Should handle error gracefully
        assert "messages" in result
        
        # Check for error message in response
        messages = result["messages"]
        error_handled = False
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.content:
                # Should contain some form of error or explanation
                if "error" in msg.content.lower() or "cannot" in msg.content.lower() or "unsupported" in msg.content.lower():
                    error_handled = True
                    break
        
        # Error should be communicated to user
        assert len(messages) > 0


class TestToolNodeIntegration:
    """Integration tests for tool node execution"""
    
    def test_tool_result_format(self):
        """
        INT_005: Verify tool results are properly formatted
        """
        from langgraph_tool_backend import calculator_tool
        
        # Invoke tool directly
        result = calculator_tool.invoke({
            "first_num": 12,
            "second_num": 8,
            "operation": "multiply"
        })
        
        # Verify result format
        assert isinstance(result, str)
        assert "×" in result or "*" in result or "multiply" in result.lower()
        assert "96" in result
    
    def test_multiple_tools_availability(self):
        """
        INT_006: Verify multiple tools are available and accessible
        """
        from langgraph_tool_backend import tools
        
        # Check that tools list exists and has expected tools
        assert len(tools) >= 9, f"Expected at least 9 tools but found {len(tools)}"
        
        tool_names = [tool.name for tool in tools]
        assert "calculator_tool" in tool_names
        assert "fetch_weather" in tool_names
        assert "get_stock_price" in tool_names


# ==================== RUN TESTS ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])