import argparse
import random
from playwright.sync_api import Page, sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument("keyword")
parser.add_argument("num_of_items")
parser.add_argument("pages_to_view")
args = parser.parse_args()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    browser_context = browser.new_context(storage_state="D:/Development/Pin_Hw/HW2/amazon_auth_state.json")
    page = browser_context.new_page()
    page.goto("https://www.amazon.com/")
    
    # Find the search box and enter the keyword
    search_box = page.locator("#twotabsearchtextbox")
    search_box.type(args.keyword, delay=random.randint(80, 120))
    page.wait_for_timeout(random.randint(100,150))
    # Click the search button
    search_button = page.locator("#nav-search-submit-button")
    search_button.click()
    
    # Wait for the search results page to load
    #page.wait_for_load_state("networkidle")
    
    # Extract data-asin from displayed products
    item_selector = "div[data-asin^='B0']"
    page.wait_for_timeout(1000)
    page.wait_for_selector(item_selector)
    product_elements = page.locator(item_selector)
    asin_list = []
    
    # Get all data-asin values from the product elements
    for i in range(product_elements.count()):
        asin_value = product_elements.nth(i).get_attribute("data-asin")
        if asin_value:  # Only add non-empty asin values
            asin_list.append(asin_value)
    
    # Print the extracted ASINs
    print(f"Found {len(asin_list)} products with ASINs:")
    for asin in asin_list:
        print(f"ASIN: {asin}")
    
    # Keep the browser open to view the results
    for asin in asin_list[:int(args.num_of_items)]:
        page.goto(f"https://www.amazon.com/product-reviews/{asin}")
        page.wait_for_timeout(1000)
        
        # Extract customer reviews for multiple pages
        for page_num in range(int(args.pages_to_view)):
            print(f"Extracting reviews from page {page_num + 1} for ASIN: {asin}")
            
            # Wait for review elements to load
            page.wait_for_selector('li[data-hook="review"]')
            
            # Extract review data
            reviews = page.locator('li[data-hook="review"]')
            review_data = []
            
            for i in range(reviews.count()):
                print(reviews.count(), i)
                review_element = reviews.nth(i)
                
                # Extract review details
                reviewer_name = review_element.locator('span[class="a-profile-name"]').first.text_content() or "N/A"
                review_title = review_element.locator("a[data-hook='review-title'] span").first.text_content() or "N/A"
                review_text = review_element.locator("span[data-hook='review-body'] span").first.text_content() or "N/A"
                review_rating = review_element.locator("i[data-hook='review-star-rating'] .a-icon-alt").first.text_content() or "N/A"
                review_date = review_element.locator("span[data-hook='review-date']").first.text_content() or "N/A"
                
                # Check for verified purchase
                verified_purchase = "No"
                try:
                    verified_element = review_element.locator("a[aria-label^='Verified Purchase:']")
                    if verified_element.count() > 0:
                        verified_purchase = "Yes"
                except:
                    verified_purchase = "No"
                
                review_data.append({
                    "reviewer_name": reviewer_name.strip(),
                    "review_title": review_title.strip(),
                    "review_text": review_text.strip(),
                    "review_rating": review_rating.strip(),
                    "review_date": review_date.strip(),
                    "verified_purchase": verified_purchase,
                    "page_number": page_num + 1
                })
            
            # Save reviews to output file
            output_filename = f"reviews_{asin}_page_{page_num + 1}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f"Product ASIN: {asin}\n")
                f.write(f"Page: {page_num + 1}\n")
                f.write("="*50 + "\n\n")
                
                for review in review_data:
                    f.write(f"Reviewer: {review['reviewer_name']}\n")
                    f.write(f"Title: {review['review_title']}\n")
                    f.write(f"Rating: {review['review_rating']}\n")
                    f.write(f"Date: {review['review_date']}\n")
                    f.write(f"Verified Purchase: {review['verified_purchase']}\n")
                    f.write(f"Review: {review['review_text']}\n")
                    f.write("-" * 30 + "\n\n")
            
            print(f"Saved {len(review_data)} reviews to {output_filename}")
            
            # Click next page if not the last page
            if page_num < int(args.pages_to_view) - 1:
                try:
                    next_button=page.get_by_role("link", name="Next page")
                    #next_button = page.locator("li[class='a-last'] a[href]")
                    if next_button.is_visible():
                        next_button.click()
                        page.wait_for_timeout(random.randint(1000, 2000))  # Random delay
                    else:
                        print("No more pages available")
                        break
                except Exception as e:
                    print(f"Could not navigate to next page: {e}")
                    break
        
    page.wait_for_timeout(5000)
    browser.close()