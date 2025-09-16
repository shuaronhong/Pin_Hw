from playwright.sync_api import sync_playwright
import json

# --- Configuration ---
AUTH_FILE_PATH = "D:/Development/Pin_Hw/HW2/amazon_auth_state.json"
AMAZON_LOGIN_URL = "https://www.amazon.com/"

def save_amazon_auth_state():
    """
    Launches a browser, allows the user to log in manually, and then
    saves the authentication state to a file.
    """
    with sync_playwright() as p:
        # We MUST run in headed mode to be able to log in manually.
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(f"Navigating to Amazon main page: {AMAZON_LOGIN_URL}")
        page.goto(AMAZON_LOGIN_URL, timeout=60000)

        # Click the sign in button
        print("Clicking sign in button...")
        sign_in_button = page.locator("#nav-link-accountList")
        sign_in_button.click()
        
        # Wait for the login page to load
        page.wait_for_load_state("networkidle")

        # --- THIS IS THE CRITICAL PART ---
        print("\n" + "="*50)
        print("Please log in to your Amazon account in the browser window.")
        print("Enter your credentials and solve any CAPTCHAs or 2FA prompts that appear.")
        input("After you have successfully logged in, press Enter here to continue...")
        print("="*50 + "\n")

        # Now that we are logged in, we can save the storage state.
        print(f"Saving authentication state to {AUTH_FILE_PATH}...")
        storage_state = context.storage_state()
        
        with open(AUTH_FILE_PATH, 'w') as f:
            json.dump(storage_state, f, indent=4)
        
        print("Authentication state saved successfully.")
        browser.close()

if __name__ == "__main__":
    save_amazon_auth_state()