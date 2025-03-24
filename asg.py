import requests
import time
import json
from datetime import datetime

BASE_URL = "http://35.200.185.69:8000/v1/autocomplete"
REQUEST_COUNT = 0
TIMEOUT = 10  # Request timeout in seconds
HEADERS = {"User-Agent": "Mozilla/5.0"}

def make_request(query: str):
    """Make a request and handle errors properly."""
    global REQUEST_COUNT
    REQUEST_COUNT += 1

    try:
        start_time = time.time()
        response = requests.get(BASE_URL, params={"query": query}, headers=HEADERS, timeout=TIMEOUT)
        elapsed_time = time.time() - start_time

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limited. Waiting {retry_after}s before retrying '{query}'...")
            time.sleep(retry_after)
            return make_request(query)

        # Print full response for debugging
        print(f"\nQuery: '{query}' | Status: {response.status_code} | Time: {elapsed_time:.3f}s")
        print(f"Response: {response.text}")

        return response.json() if response.status_code == 200 else None

    except requests.exceptions.RequestException as e:
        print(f"Request error for '{query}': {e}")
        return None

def extract_names():
    """
    Extract all possible names from the API using recursive exploration.
    For each name found, the function will query that name to find additional connected names
    until no new names are discovered.
    """
    
    to_process = set()  # Queue of names to process
    names_found = []
    # Start with a-z prefixes
    from datetime import datetime

    # Initialize with single-letter prefixes (a to z)
    prefixes = {chr(i) for i in range(ord('a'), ord('z') + 1)}
    to_process = set(prefixes)  # Separate queue to track elements to process

    print("\nStarting recursive name extraction from API...")
    start_time = datetime.now()

    # Process names dynamically
    while to_process:
        current_prefix = to_process.pop()  # Remove and process one element at a time
        names_found.append(current_prefix)

        result = make_request(current_prefix)
        if result and isinstance(result, dict) and "results" in result:
            names = set(result["results"])  # Extract names
            new_names = names - prefixes  # Filter out already seen names

            if new_names:
                prefixes.update(new_names)  # Add to master set
                to_process.update(new_names)  # Queue new names for processing
                print(f"Prefix '{current_prefix}': Found {len(names)} names, {len(new_names)} are new")
            else:
                print(f"Prefix '{current_prefix}': No new names added")
        else:
            print(f"Prefix '{current_prefix}': No result returned")

    
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    print(f"\nExtraction complete!")
    print(f"Total unique names found: {len(names_found)}")
    print(f"Total API requests made: {REQUEST_COUNT}")
    print(f"Total time elapsed: {elapsed:.2f} seconds")
    
    return {
        "names": sorted(names_found),
        "total_time": elapsed,
        "request_count": REQUEST_COUNT
    }

if __name__ == "__main__":
    # Test a basic query
    test_query = "a"
    test_result = make_request(test_query)

    if test_result:
        print("\nInitial Test Query Result:")
        print(json.dumps(test_result, indent=2))

    # Extract all names
    results = extract_names()

    # Print summary
    print("\nSummary:")
    print(f"Total unique names found: {len(results['names'])}")
    print(f"Total requests made: {results['request_count']}")
    print(f"Total time taken: {results['total_time']:.2f}s")