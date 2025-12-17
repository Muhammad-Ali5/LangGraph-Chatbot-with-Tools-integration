class LoginManager:
    def __init__(self):
        # In a real system, this would be a database
        self.users = {
            "admin": "admin123",
            "user1": "pass123"
        }

    def login(self, username, password):
        """
        Validates the login credentials.
        Returns True if successful, False otherwise.
        """
        if not username or not password:
            return False
            
        if username in self.users and self.users[username] == password:
            return True
        return False

    def validate_password_strength(self, password):
        """
        Checks if password meets strength requirements
        """
        if len(password) < 6:
            return False
        return True
