#!/usr/bin/env python3
"""
ReviewEnhancer.py

This script adds a wordCount key to each review in all Reviews*.json files in the data directory.
It calculates the word count of the "text" field for each review and adds it as a new key.
"""

import json
import os
import glob
import sys
from typing import List, Dict, Any, Optional


def calculate_word_count(text: Optional[str]) -> int:
    """
    Calculate the word count of a text string.
    
    Args:
        text: The text to count words in. Can be None.
        
    Returns:
        The number of words in the text. Returns 0 if text is None or empty.
    """
    if not text:
        return 0
    
    # Split by whitespace and filter out empty strings
    words = [word for word in text.split() if word.strip()]
    return len(words)


def process_reviews_file(file_path: str) -> bool:
    """
    Process a single reviews file, adding wordCount to each review.
    
    Args:
        file_path: Path to the reviews JSON file.
        
    Returns:
        True if processing was successful, False otherwise.
    """
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            reviews_data = json.load(f)
        
        # Ensure we have a list of reviews
        if not isinstance(reviews_data, list):
            print(f"Warning: {file_path} does not contain a list of reviews. Skipping.")
            return False
        
        # Process each review
        updated_count = 0
        for review in reviews_data:
            if not isinstance(review, dict):
                print(f"Warning: Found non-dictionary review in {file_path}. Skipping.")
                continue
            
            # Get the text field and calculate word count
            text = review.get("text")
            word_count = calculate_word_count(text)
            
            # Add the wordCount key
            review["wordCount"] = word_count
            updated_count += 1
        
        # Write the updated data back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(reviews_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully processed {file_path}: Updated {updated_count} reviews.")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON in {file_path}: {e}")
        return False
    except IOError as e:
        print(f"Error processing file {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")
        return False


def find_reviews_files(directory: str = "data") -> List[str]:
    """
    Find all Reviews*.json files in the specified directory.
    
    Args:
        directory: Directory to search for Review files. Defaults to "data".
        
    Returns:
        List of file paths matching the pattern.
    """
    pattern = os.path.join(directory, "Reviews*.json")
    files = glob.glob(pattern)
    return sorted(files)


def main():
    """Main function to process all review files."""
    # Parse command line arguments
    directory = "data"
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    
    # Find all review files
    review_files = find_reviews_files(directory)
    
    if not review_files:
        print(f"No Review files found in directory '{directory}'")
        return
    
    print(f"Found {len(review_files)} Review files to process:")
    for file_path in review_files:
        print(f"  - {file_path}")
    print()
    
    # Process each file
    success_count = 0
    for file_path in review_files:
        if process_reviews_file(file_path):
            success_count += 1
    
    print(f"\nProcessing complete. Successfully updated {success_count}/{len(review_files)} files.")


if __name__ == "__main__":
    main()