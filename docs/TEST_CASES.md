# Test Cases for Login System

| Test Case ID | Test Scenario | Pre-conditions | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC_001 | Verify Valid Admin Login | System is running, Admin account exists | 1. Enter username 'admin'<br>2. Enter password 'admin123'<br>3. Click Login | User logged in successfully | User logged in | Pass |
| TC_002 | Verify Valid User Login | System is running, User1 account exists | 1. Enter username 'user1'<br>2. Enter password 'pass123'<br>3. Click Login | User logged in successfully | User logged in | Pass |
| TC_003 | Check Password Strength Validation | System is running | 1. Call validate_password_strength with 'abcdef' | Returns True | Returns True | Pass |
| TC_004 | Verify Multiple Logins | System is running | 1. Login as admin<br>2. Logout<br>3. Login as admin again | Login successful both times | Login successful | Pass |
| TC_005 | Verify Invalid Password | System is running | 1. Enter username 'admin'<br>2. Enter password 'wrong' | Login fails, return False | Login fails | Pass |
| TC_006 | Verify Non-existent User | System is running | 1. Enter username 'unknown'<br>2. Enter password 'any' | Login fails, return False | Login fails | Pass |