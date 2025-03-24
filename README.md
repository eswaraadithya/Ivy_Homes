# Ivy_Homes

# Extracting Names from the Autocomplete API

## 1. Problem Statement
We have been given access to an autocomplete API at `http://35.200.185.69:8000`. However, there is no official documentation. The objective is to systematically explore the API, extract all possible names, and document the findings.

## 2. Approach
The program follows a structured approach to discover and extract names:

1. **API Exploration**
   - Sending requests to `/v1/autocomplete?query=<string>`.
   - Analyzing the API response format.
   - Identifying rate limits and constraints.

2. **Data Extraction Strategy**
   - Querying the API using all lowercase letters (`a-z`) as prefixes.
   - Collecting unique names from the response.
   
3. **Handling API Constraints**
   - Implementing error handling for failed requests.
   - Detecting and handling rate limiting (HTTP 429) by respecting the `Retry-After` header.
   - Setting a request timeout to prevent indefinite waiting.

4. **Efficiency Considerations**
   - Using a set to store unique names and avoid duplicates.
   - Logging query execution time for performance evaluation.

## 3. Implementation
The script is written in Python and uses the `requests` library to interact with the API.

### **Code Breakdown**

1. **Making API Requests**
   - A function `make_request(query)` sends GET requests and handles errors gracefully.
   - It detects rate limits and waits before retrying.
   
2. **Extracting Names**
   - `extract_names()` loops through each letter (`a-z`), collects names, and measures execution time.

3. **Summary Report**
   - The script prints total names extracted, total requests made, and execution time.

## 4. Running the Script
### **Prerequisites**
Ensure you have Python installed with the following dependencies:
```sh
pip install requests
```

### **Executing the Script**
Run the script using:
```sh
python script.py
```

## 5. Observations and Findings
1. The API accepts simple queries and returns a JSON response.
2. It enforces rate limits (`HTTP 429`), which are handled using retries.
3. The response contains a `results` field with names.
4. The API does not seem to return all names in a single query, requiring multiple queries with different prefixes.

## 6. Results
- **Total unique names found:** 286
- **Total API requests made:** 370
- **Total execution time:** 132.81 seconds

## 7. Additional Considerations
- Further optimization can be done by dynamically expanding prefixes based on partial results.
- Multithreading could speed up the extraction process but must consider rate limits.

## 8. Files in the Repository
- `script.py`: Main Python script for extracting names.
- `README.md`: Documentation of the approach and findings.

---
