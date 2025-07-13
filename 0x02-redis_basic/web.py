#!/usr/bin/env python3
"""
A module for fetching web pages with caching and access tracking.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize a Redis client instance
# This assumes your Redis server is running on localhost:6379
redis_client = redis.Redis()


def cache_and_track(method: Callable) -> Callable:
    """
    Decorator that caches a function's return value and tracks call counts.

    It uses two Redis keys for each URL:
    - "count:{url}" to store the number of times it has been accessed.
    - "cache:{url}" to store the HTML content, with an expiration of 10 seconds.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        The wrapper function that adds caching and tracking functionality.
        """
        # Define the key for counting URL accesses
        count_key = f"count:{url}"
        redis_client.incr(count_key) # Increment the access count

        # Define the key for caching the page content
        cache_key = f"cache:{url}"
        cached_page = redis_client.get(cache_key)

        # If the page is already in the cache, return it
        if cached_page:
            return cached_page.decode('utf-8')

        # If not cached, call the original function to fetch the page
        html_content = method(url)

        # Cache the fetched content in Redis with an expiration of 10 seconds
        redis_client.setex(cache_key, 10, html_content)

        return html_content
    return wrapper

@cache_and_track
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    The @cache_and_track decorator handles the caching and access counting.
    """
    try:
        response = requests.get(url)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""


if __name__ == '__main__':
    # Example usage to test the functionality
    import time

    # We use a slow URL to easily observe the effect of caching
    slow_url = "http://slowwly.robertomurray.co.uk/ws/2/" # This URL takes ~2s

    print("--- 1. First request (slow, fetches from the web) ---")
    start = time.time()
    get_page(slow_url)
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")

    print("\n--- 2. Second request (fast, should come from cache) ---")
    start = time.time()
    get_page(slow_url)
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")

    print("\n--- Waiting for 11 seconds for the cache to expire... ---")
    time.sleep(11)

    print("\n--- 3. Third request (slow again, cache has expired) ---")
    start = time.time()
    get_page(slow_url)
    end = time.time()
    print(f"Time taken: {end - start:.2f} seconds")
