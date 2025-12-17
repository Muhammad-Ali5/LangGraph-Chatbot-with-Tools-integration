import unittest
import sys
import os

# Add src to python path to import LoginManager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from login_manager import LoginManager

class TestLoginSystem(unittest.TestCase):
    def setUp(self):
        self.login_manager = LoginManager()

    # Positive Test Cases
    def test_login_success(self):
        """Test Case 1: Valid Admin Login"""
        self.assertTrue(self.login_manager.login("admin", "admin123"), "Admin should be able to login with direct credentials")

    def test_user_login_success(self):
        """Test Case 2: Valid User Login"""
        self.assertTrue(self.login_manager.login("user1", "pass123"), "Standard user should be able to login")
        
    def test_password_strength_valid(self):
        """Test Case 3: Valid Password Strength"""
        self.assertTrue(self.login_manager.validate_password_strength("strongpass"), "Password > 6 chars should be valid")

    def test_login_persistence(self):
         """Test Case 4: Repeated Login"""
         self.assertTrue(self.login_manager.login("admin", "admin123"))
         self.assertTrue(self.login_manager.login("admin", "admin123"), "Should be able to login multiple times")

    # Negative Test Cases
    def test_login_wrong_password(self):
        """Test Case 5: Invalid Password"""
        self.assertFalse(self.login_manager.login("admin", "wrongpass"), "Login should fail with wrong password")

    def test_login_nonexistent_user(self):
        """Test Case 6: Non-existent User"""
        self.assertFalse(self.login_manager.login("ghost", "pass123"), "Login should fail for non-existent user")
    
    def test_empty_credentials(self):
        """Test Case 7: Empty Credentials (Extra Negative)"""
        self.assertFalse(self.login_manager.login("", ""), "Login should fail with empty credentials")

if __name__ == '__main__':
    unittest.main()
