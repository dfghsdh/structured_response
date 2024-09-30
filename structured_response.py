import json
import requests
import yaml
import csv
import io
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: BeautifulSoup4 is not installed. Please run 'pip install beautifulsoup4'")
    exit(1)
import xml.etree.ElementTree as ET

def query_ollama(prompt, model="llama3.2:3b"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return response.json()["response"]

def is_valid_json(structure):
    try:
        json.loads(structure)
        return True
    except json.JSONDecodeError:
        return False

def is_valid_html(structure):
    soup = BeautifulSoup(structure, 'html.parser')
    return soup.find() is not None

def is_valid_xml(structure):
    try:
        ET.fromstring(structure)
        return True
    except ET.ParseError:
        return False

def is_valid_yaml(structure):
    try:
        yaml.safe_load(structure)
        return True
    except yaml.YAMLError:
        return False

def is_valid_csv(structure):
    try:
        csv.reader(io.StringIO(structure))
        return True
    except csv.Error:
        return False

def extract_structure(text, structure_type):
    if structure_type == 'json':
        start = text.find('{')
        end = text.rfind('}') + 1
    elif structure_type in ['html', 'xml']:
        start = text.find('<')
        end = text.rfind('>') + 1
    elif structure_type in ['yaml', 'csv']:
        return text  # YAML and CSV don't have clear delimiters, so we return the whole text
    else:
        return None

    if start != -1 and end != -1:
        return text[start:end]
    return None

def process_structured_output(data, structure, structure_type, verbose=False):
    prompt = f"Given the following data:\n{data}\n\nPlease fill out this {structure_type.upper()} structure. DO NOT DEVIATE FROM THE STRUCTURE EVEN TO IMPROVE IT, DO NOT LEAVE COMMENTS INSIDE THE {structure_type.upper()}:\n{structure}\n\nProvide only the filled {structure_type.upper()} structure in your response."
    output = None
    max_attempts = 5
    attempts_log = []

    validity_functions = {
        'json': is_valid_json,
        'html': is_valid_html,
        'xml': is_valid_xml,
        'yaml': is_valid_yaml,
        'csv': is_valid_csv
    }

    for attempt in range(max_attempts):
        if verbose:
            print(f"\nAttempt {attempt + 1}:")
        response = query_ollama(prompt)
        output = extract_structure(response, structure_type)
        
        attempts_log.append({
            "attempt": attempt + 1,
            "response": response,
            "extracted_structure": output
        })
        
        if verbose:
            print(f"Extracted {structure_type.upper()}:\n{output}")
        
        if output and validity_functions[structure_type](output):
            return output, attempt + 1, attempts_log

        if verbose:
            print(f"Invalid {structure_type.upper()}. Retrying...")
        prompt = f"The previous response was not valid {structure_type.upper()}. Please correctly fit the data into the {structure_type.upper()} structure. DO NOT DEVIATE FROM THE STRUCTURE EVEN TO IMPROVE IT, DO NOT LEAVE COMMENTS INSIDE THE {structure_type.upper()}:\n{structure}\n\nFilled with the data:\n{data}"
    
    if verbose:
        print(f"Failed to generate valid {structure_type.upper()} after maximum attempts.")
    return None, max_attempts, attempts_log

def main(verbose=False):
    test_cases = [
        {
            "name": "JSON test",
            "data": "The capital of France is Paris",
            "structure": '{"country": "", "capital": ""}',
            "type": "json"
        },
        {
            "name": "HTML test",
            "data": "Welcome to my website. This is the main content.",
            "structure": "<html><head><title></title></head><body><h1></h1><p></p></body></html>",
            "type": "html"
        },
        {
            "name": "XML test",
            "data": "John Doe is 30 years old and works as a developer",
            "structure": "<person><name></name><age></age><occupation></occupation></person>",
            "type": "xml"
        },
        {
            "name": "YAML test",
            "data": "The book 'To Kill a Mockingbird' was written by Harper Lee in 1960",
            "structure": "book:\n  title:\n  author:\n  year:",
            "type": "yaml"
        },
        {
            "name": "CSV test",
            "data": "John is 30 years old, Mary is 25 years old, and Bob is 35 years old",
            "structure": "Name,Age\n,,\n,,\n,,",
            "type": "csv"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"Data: {test['data']}")
        print(f"Structure: {test['structure']}")
        print(f"Type: {test['type']}")
        
        result, attempts, log = process_structured_output(test['data'], test['structure'], test['type'], verbose)
        
        print(f"Result (after {attempts} attempts):")
        print(result)
        if verbose:
            print("Attempts log:")
            for entry in log:
                print(f"  Attempt {entry['attempt']}:")
                print(f"    Response: {entry['response'][:100]}...")
                print(f"    Extracted structure: {entry['extracted_structure'][:100]}...")
        
        if result:
            print("Test passed!")
        else:
            print("Test failed.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate structured responses using Ollama API")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    main(verbose=args.verbose)
