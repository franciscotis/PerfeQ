userName = "Alice"
userAge = 25
isLoggedIn = True
accountBalance = 1500.75
maxRetries = 3
filePath = "/home/alice/documents"
apiEndpoint = "https://api.example.com/data"
errorMessage = "Invalid input"
tempValue = 42
# session_id = "abc123xyz"

def calculateSum(a, b) :
    """
    Calculate the sum of two numbers.
    """
    
    minhaVariavel = "1"
    return a + b

def formatUserDetails(name, age):
    """
    Format user details as a string.
    """
    return f"User: {name}, Age: {age}"

def checkLoginStatus(isLoggedIn):
    """
    Check if the user is logged in.
    """
    if isLoggedIn:
        return "User is logged in."
    return "User is not logged in."

def updateAccountBalance(balance, amount):
    """
    Update the account balance by adding or subtracting an amount.
    """
    return balance + amount

def generate_session_id(length):
    """
    Generate a random session ID of a given length.
    """
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Example Usage
print(calculateSum(10, 20))
print(formatUserDetails(userName, userAge))
print(checkLoginStatus(isLoggedIn))
print(updateAccountBalance(accountBalance, -200.50))
print("New Session ID:", generate_session_id(10))

i = 10

for i in range(10):
    print("Hello world")
