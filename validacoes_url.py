import requests
import random
import time
from urllib.parse import urlparse

# List of blocked domains (case insensitive)
BLOCKED_DOMAINS = [
    'github.com',
    'facebook.com',
    'instagram.com',
    'google.com',
    'youtube.com',
    'twitter.com',
    'linkedin.com'
]


def is_url_valid(url):
    """Validate URL format and check against blocked domains"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False

        # Check if domain is blocked
        domain = result.netloc.lower()
        if any(blocked_domain in domain for blocked_domain in BLOCKED_DOMAINS):
            return False

        return True
    except:
        return False


def is_domain_blocked(url):
    """Check if URL belongs to a blocked domain"""
    try:
        domain = urlparse(url).netloc.lower()
        return any(blocked_domain in domain for blocked_domain in BLOCKED_DOMAINS)
    except:
        return True  # Block if we can't parse


def get_session_with_proxy():
    """Create a requests session with random proxy and user-agent"""
    session = requests.Session()

    # Random proxy selection
    if PROXY_LIST:
        proxy = random.choice(PROXY_LIST)
        session.proxies.update(proxy)

    return session


def fetch_url_with_retry(url, max_retries=3):
    """Fetch URL with retry mechanism and proxy rotation"""
    # First check if URL is blocked
    if is_domain_blocked(url):
        raise Exception(f"Access to this domain is blocked by policy")

    for attempt in range(max_retries):
        try:
            session = get_session_with_proxy()
            response = session.get(url, timeout=10)

            # If we get blocked, try with different proxy
            if response.status_code == 403:
                raise Exception(f"Blocked by server (403)")

            response.raise_for_status()
            return response

        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 * (attempt + 1))  # Exponential backoff
            continue
    return None

