from fyers_apiv3 import fyersModel
import webbrowser
from urllib.parse import urlparse, parse_qs

# Yahan apna FYERS App ID aur Secret Key daalna
CLIENT_ID = "O21QCP3N13-100" 
SECRET_KEY = "3NG2SE8M9W"
REDIRECT_URI = "https://www.google.com" 

def generate_token():
    session = fyersModel.SessionModel(
        client_id=CLIENT_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )
    
    generate_token_url = session.generate_authcode()
    print("Please login via this URL:", generate_token_url)
    webbrowser.open(generate_token_url)
    
    # Yahan tu chahe poora URL paste karde, script khud auth_code nikal legi
    user_input = input("Enter the redirected URL or auth_code: ").strip()
    
    if "auth_code=" in user_input:
        parsed_url = urlparse(user_input)
        query_params = parse_qs(parsed_url.query)
        auth_code = query_params.get("auth_code", [None])[0]
    else:
        auth_code = user_input
        
    if not auth_code:
        print("❌ Error: Could not extract auth_code!")
        return
        
    session.set_token(auth_code)
    
    response = session.generate_token()
    print("API Response:", response)
    
    access_token = response["access_token"]
    
    with open("fyers_token.txt", "w") as f:
        f.write(access_token)
    
    print("✅ Token saved successfully! You can now run the Streamlit app.")

if __name__ == "__main__":
    generate_token()
