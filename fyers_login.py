# FILE: fyers_login.py
from fyers_apiv3 import fyersModel
import webbrowser

# Yahan apna FYERS App ID aur Secret Key daalna
CLIENT_ID = "YOUR_CLIENT_ID-100" 
SECRET_KEY = "YOUR_SECRET_KEY"
REDIRECT_URI = "http://127.0.0.1:8501/" 

def generate_token():
    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )
    
    # Ye link browser mein khulega
    generate_token_url = session.generate_authcode()
    print("Please login via this URL:", generate_token_url)
    webbrowser.open(generate_token_url)
    
    # Login ke baad URL se 'auth_code' copy karke yahan daalna
    auth_code = input("Enter the 'auth_code' from the redirected URL: ")
    session.set_token(auth_code)
    
    response = session.generate_token()
    access_token = response["access_token"]
    
    with open("fyers_token.txt", "w") as f:
        f.write(access_token)
    
    print("✅ Token saved successfully! You can now run the Streamlit app.")

if __name__ == "__main__":
    generate_token()