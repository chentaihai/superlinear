#!/usr/bin/env python3
"""
Instagram Image Downloader v2 - Enhanced Version

This script downloads all images from an Instagram profile page with improved detection.
Features:
- Better image URL detection (multiple Instagram domains)
- Post link extraction for higher resolution images
- Login verification
- More robust scrolling

Usage:
    python instagram_image_downloader_v2.py <profile_url> [--output-dir DIR] [--headless] [--manual-login]

Example:
    python instagram_image_downloader_v2.py https://www.instagram.com/username/ --manual-login --max-scrolls 100
"""

import os
import sys
import time
import re
import json
import requests
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def setup_driver(headless=False, user_data_dir=None):
    """Setup Chrome driver with advanced options."""
    chrome_options = Options()
    
    # Disable automation detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Anti-detection techniques
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    
    if headless:
        chrome_options.add_argument('--headless')
    else:
        # Non-headless options for better compatibility
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
    
    # User agent to mimic real browser
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Use persistent user data if provided (for saving login session)
    if user_data_dir:
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Use webdriver-manager to automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.chrome = window.chrome || {};
            window.chrome.runtime = window.chrome.runtime || {};
        '''
    })
    
    return driver

def wait_for_login(driver, timeout=720):
    """
    Wait for user to manually log in and verify login success.
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum wait time in seconds
    
    Returns:
        True if login appears successful, False otherwise
    """
    logger.info("Waiting for manual login...")
    logger.info("Please log in to Instagram in the opened browser window.")
    logger.info(f"You have {timeout} seconds to complete login.")
    
    start_time = time.time()
    last_url = driver.current_url
    
    try:
        while time.time() - start_time < timeout:
            current_url = driver.current_url
            
            # Check if we're on a login page
            if "accounts/login" in current_url or "login" in current_url:
                logger.info("Still on login page...")
                time.sleep(2)
                continue
            
            # Check if we're on the target profile page
            if "instagram.com" in current_url and current_url != last_url:
                logger.info(f"URL changed to: {current_url}")
                
                # Check for login indicators
                try:
                    # Look for profile elements that indicate successful login
                    profile_elements = driver.find_elements(By.XPATH, "//article | //div[contains(@class, '_aagu')] | //img[contains(@src, 'cdninstagram.com')]")
                    if len(profile_elements) > 0:
                        logger.info("Login appears successful. Found profile elements.")
                        return True
                except:
                    pass
            
            last_url = current_url
            time.sleep(3)
        
        logger.warning("Login timeout reached. Continuing anyway...")
        return False
        
    except Exception as e:
        logger.error(f"Error during login wait: {e}")
        return False

def extract_all_image_urls(driver, scroll_pause_time=2.5, max_scrolls=100):
    """
    Advanced image URL extraction with multiple detection methods.
    
    Args:
        driver: Selenium WebDriver instance
        scroll_pause_time: Time to wait between scrolls (seconds)
        max_scrolls: Maximum number of scroll attempts
        
    Returns:
        Tuple of (image_urls, post_urls)
    """
    image_urls = set()
    post_urls = set()
    
    # Instagram image domains to look for
    instagram_domains = [
        'cdninstagram.com',
        'instagram.fsin1-1.fna.fbcdn.net',
        'instagram.fsin1-2.fna.fbcdn.net',
        'instagram.fsin1-3.fna.fbcdn.net',
        'instagram.fsin1-4.fna.fbcdn.net',
        'scontent.cdninstagram.com',
        'scontent-ams2-1.cdninstagram.com',
        'scontent-ams3-1.cdninstagram.com',
        'scontent-ams4-1.cdninstagram.com',
    ]
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    
    logger.info(f"Starting to scroll through page (max {max_scrolls} times)...")
    
    for i in range(max_scrolls):
        scroll_attempts += 1
        
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        # Get current page source
        page_source = driver.page_source
        
        # Method 1: Extract from img tags
        img_elements = driver.find_elements(By.TAG_NAME, 'img')
        for img in img_elements:
            try:
                src = img.get_attribute('src')
                srcset = img.get_attribute('srcset')
                
                if src and is_instagram_image_url(src, instagram_domains):
                    image_urls.add(src)
                    logger.debug(f"Found image from img tag: {src[:80]}...")
                
                if srcset:
                    # Parse srcset (e.g., "url1 1x, url2 2x")
                    for srcset_item in srcset.split(','):
                        url = srcset_item.strip().split(' ')[0]
                        if url and is_instagram_image_url(url, instagram_domains):
                            image_urls.add(url)
                            logger.debug(f"Found image from srcset: {url[:80]}...")
            except Exception as e:
                logger.debug(f"Error processing img element: {e}")
        
        # Method 2: Extract from CSS backgrounds
        all_elements = driver.find_elements(By.XPATH, "//*[@style]")
        for element in all_elements:
            try:
                style = element.get_attribute('style')
                if 'background-image' in style.lower():
                    # Extract URL from background-image: url(...)
                    url_match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', style)
                    if url_match:
                        url = url_match.group(1)
                        if is_instagram_image_url(url, instagram_domains):
                            image_urls.add(url)
                            logger.debug(f"Found image from background: {url[:80]}...")
            except:
                pass
        
        # Method 3: Extract post links for potential higher resolution images
        post_link_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/') or contains(@href, '/reel/')]")
        for link in post_link_elements:
            try:
                href = link.get_attribute('href')
                if href and 'instagram.com' in href and '/p/' in href:
                    post_urls.add(href)
                    logger.debug(f"Found post link: {href}")
            except:
                pass
        
        # Method 4: Regex search in page source for Instagram image URLs
        for domain in instagram_domains:
            pattern = fr'https?://[^"\'\s]*{domain}[^"\'\s]*\.(?:jpg|jpeg|png|gif|webp)(?:\?[^"\'\s]*)?'
            matches = re.findall(pattern, page_source, re.IGNORECASE)
            for match in matches:
                image_urls.add(match)
        
        # Check for scroll completion
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logger.info(f"No more content to load after {scroll_attempts} scrolls")
            break
        
        last_height = new_height
        
        # Progress update
        logger.info(f"Scroll {scroll_attempts}: Found {len(image_urls)} image URLs and {len(post_urls)} post links")
        
        # Random pause variation to mimic human behavior
        time.sleep(scroll_pause_time + (i % 3) * 0.5)
    
    logger.info(f"Extraction complete: {len(image_urls)} image URLs, {len(post_urls)} post links")
    return list(image_urls), list(post_urls)

def is_instagram_image_url(url, instagram_domains=None):
    """
    Check if URL is likely an Instagram image URL.
    
    Args:
        url: URL to check
        instagram_domains: List of Instagram domains to check
        
    Returns:
        True if URL appears to be an Instagram image
    """
    if not url:
        return False
    
    url_lower = url.lower()
    
    # Check for image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if any(ext in url_lower for ext in image_extensions):
        # Check for Instagram domains
        if instagram_domains:
            if any(domain in url_lower for domain in instagram_domains):
                return True
        
        # Also accept any URL with 'instagram' in domain
        if 'instagram' in url_lower:
            return True
    
    return False

def download_image(url, output_dir, index):
    """
    Download a single image with improved error handling.
    
    Args:
        url: Image URL
        output_dir: Directory to save the image
        index: Index for filename
        
    Returns:
        Tuple (success, filename, error_message)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, stream=True, timeout=30, headers=headers)
        response.raise_for_status()
        
        # Determine filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # Clean filename
        if not filename or '.' not in filename:
            ext = get_extension_from_url(url)
            filename = f"instagram_image_{index:04d}{ext}"
        else:
            # Remove query parameters and clean
            filename = filename.split('?')[0]
            # Ensure safe filename
            filename = re.sub(r'[^\w\-\.]', '_', filename)
        
        filepath = os.path.join(output_dir, filename)
        
        # Ensure unique filename
        counter = 1
        base, ext = os.path.splitext(filepath)
        while os.path.exists(filepath):
            filepath = f"{base}_{counter}{ext}"
            counter += 1
        
        # Get final filename
        final_filename = os.path.basename(filepath)
        
        # Download with chunking
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Verify file was downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            logger.debug(f"Downloaded: {final_filename} ({os.path.getsize(filepath)} bytes)")
            return True, final_filename, None
        else:
            logger.error(f"File downloaded but appears empty: {final_filename}")
            return False, None, "Downloaded file is empty"
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout downloading {url[:80]}...")
        return False, None, "Timeout"
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error downloading {url[:80]}: {e}")
        return False, None, f"HTTP error: {e}"
    except Exception as e:
        logger.error(f"Error downloading {url[:80]}: {e}")
        return False, None, str(e)

def get_extension_from_url(url):
    """Extract file extension from URL."""
    url_lower = url.lower()
    if '.jpg' in url_lower or '.jpeg' in url_lower:
        return '.jpg'
    elif '.png' in url_lower:
        return '.png'
    elif '.gif' in url_lower:
        return '.gif'
    elif '.webp' in url_lower:
        return '.webp'
    else:
        # Default to .jpg if unknown
        return '.jpg'

def download_images_parallel(urls, output_dir, max_workers=5):
    """
    Download images in parallel using thread pool.
    
    Args:
        urls: List of image URLs
        output_dir: Directory to save images
        max_workers: Maximum number of parallel downloads
        
    Returns:
        Dictionary with download statistics
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    results = {
        'total': len(urls),
        'success': 0,
        'failed': 0,
        'failed_urls': [],
        'downloaded_files': []
    }
    
    if not urls:
        logger.warning("No URLs to download")
        return results
    
    logger.info(f"Starting parallel download of {len(urls)} images with {max_workers} workers...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_image, url, output_dir, i): url
            for i, url in enumerate(urls)
        }
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                success, filename, error = future.result()
                if success:
                    results['success'] += 1
                    results['downloaded_files'].append(filename)
                    logger.info(f"✓ Downloaded: {filename}")
                else:
                    results['failed'] += 1
                    results['failed_urls'].append((url, error))
                    logger.warning(f"✗ Failed: {url[:80]}... - {error}")
            except Exception as e:
                results['failed'] += 1
                results['failed_urls'].append((url, str(e)))
                logger.error(f"✗ Unexpected error for {url[:80]}: {e}")
    
    return results

def save_metadata(image_urls, post_urls, output_dir):
    """Save metadata about the downloaded images."""
    metadata = {
        'download_date': datetime.now().isoformat(),
        'total_images': len(image_urls),
        'total_posts': len(post_urls),
        'image_urls': image_urls,
        'post_urls': post_urls
    }
    
    metadata_file = os.path.join(output_dir, 'download_metadata.json')
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Metadata saved to: {metadata_file}")
    return metadata_file

def main():
    parser = argparse.ArgumentParser(description='Download images from Instagram profile (Enhanced Version)')
    parser.add_argument('profile_url', help='Instagram profile URL (e.g., https://www.instagram.com/username/)')
    parser.add_argument('--output-dir', '-o', default='instagram_images',
                        help='Output directory for downloaded images (default: instagram_images)')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode (no GUI)')
    parser.add_argument('--manual-login', action='store_true',
                        help='Pause for manual login. Use this if the profile is private or requires login.')
    parser.add_argument('--login-timeout', type=int, default=720,
                        help='Wait time in seconds for manual login (default: 720)')
    parser.add_argument('--max-scrolls', type=int, default=100,
                        help='Maximum number of scroll attempts (default: 100)')
    parser.add_argument('--scroll-pause', type=float, default=2.5,
                        help='Pause time between scrolls in seconds (default: 2.5)')
    parser.add_argument('--max-workers', type=int, default=5,
                        help='Maximum parallel downloads (default: 5)')
    parser.add_argument('--save-metadata', action='store_true',
                        help='Save metadata about downloaded images')
    parser.add_argument('--user-data-dir', default=None,
                        help='Chrome user data directory for persistent sessions')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.profile_url.startswith('https://www.instagram.com/'):
        logger.warning(f"URL doesn't look like an Instagram profile: {args.profile_url}")
        logger.warning("Make sure to use the full profile URL (e.g., https://www.instagram.com/username/)")
    
    logger.info("=" * 60)
    logger.info(f"Instagram Image Downloader v2")
    logger.info("=" * 60)
    logger.info(f"Profile: {args.profile_url}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Headless mode: {args.headless}")
    logger.info(f"Manual login: {args.manual_login}")
    if args.manual_login:
        logger.info(f"Login timeout: {args.login_timeout} seconds")
    logger.info(f"Max scrolls: {args.max_scrolls}")
    logger.info(f"Scroll pause: {args.scroll_pause} seconds")
    logger.info(f"Max workers: {args.max_workers}")
    
    driver = None
    try:
        # Setup driver
        logger.info("Setting up browser...")
        driver = setup_driver(headless=args.headless, user_data_dir=args.user_data_dir)
        logger.info("Browser started successfully")
        
        # Open the profile page
        logger.info(f"Opening profile page: {args.profile_url}")
        driver.get(args.profile_url)
        time.sleep(5)  # Wait for initial page load
        
        # Check if page loaded successfully
        current_url = driver.current_url
        logger.info(f"Current URL: {current_url}")
        
        if "instagram.com" not in current_url:
            logger.error("Failed to load Instagram.")
            logger.error("You might be blocked, need to solve a captcha, or network issues.")
            sys.exit(1)
        
        # Manual login if requested
        login_successful = True  # Assume success unless manual login fails
        if args.manual_login and not args.headless:
            login_successful = wait_for_login(driver, timeout=args.login_timeout)
            if not login_successful:
                logger.warning("Login verification failed. Proceeding anyway...")
        
        # Extract image URLs and post links
        logger.info("Starting image extraction...")
        image_urls, post_urls = extract_all_image_urls(
            driver,
            scroll_pause_time=args.scroll_pause,
            max_scrolls=args.max_scrolls
        )
        
        # Check if we found any images
        if not image_urls:
            logger.error("No image URLs found!")
            logger.error("Possible reasons:")
            logger.error("1. The profile might be private and you're not logged in")
            logger.error("2. The profile has no posts")
            logger.error("3. Instagram's page structure may have changed")
            logger.error("4. You might be blocked or rate-limited")
            sys.exit(1)
        
        # Save metadata if requested
        if args.save_metadata:
            save_metadata(image_urls, post_urls, args.output_dir)
        
        # Save URLs to file
        os.makedirs(args.output_dir, exist_ok=True)
        urls_file = os.path.join(args.output_dir, 'extracted_urls.json')
        with open(urls_file, 'w', encoding='utf-8') as f:
            json.dump({
                'image_urls': image_urls,
                'post_urls': post_urls,
                'extraction_date': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        logger.info(f"Extracted URLs saved to: {urls_file}")
        
        # Download images
        logger.info(f"Downloading {len(image_urls)} images...")
        results = download_images_parallel(image_urls, args.output_dir, args.max_workers)
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("DOWNLOAD SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Profile URL: {args.profile_url}")
        logger.info(f"Image URLs found: {results['total']}")
        logger.info(f"Successfully downloaded: {results['success']}")
        logger.info(f"Failed downloads: {results['failed']}")
        logger.info(f"Download directory: {os.path.abspath(args.output_dir)}")
        
        if results['failed'] > 0:
            logger.warning(f"\nFailed URLs ({results['failed']}):")
            for url, error in results['failed_urls'][:10]:  # Show first 10
                logger.warning(f"  {url[:100]}... - {error}")
            if results['failed'] > 10:
                logger.warning(f"  ... and {results['failed'] - 10} more")
        
        if args.save_metadata:
            logger.info(f"Metadata saved to: {os.path.join(args.output_dir, 'download_metadata.json')}")
        
        logger.info("\nDownload completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        logger.error("\nTroubleshooting tips:")
        logger.error("1. Ensure you have Chrome browser installed")
        logger.error("2. Try using --manual-login if profile is private")
        logger.error("3. Check your internet connection")
        logger.error("4. Instagram might be blocking automated access")
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")

if __name__ == '__main__':
    main()