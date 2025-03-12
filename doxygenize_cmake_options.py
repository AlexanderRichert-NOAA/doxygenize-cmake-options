#!/usr/bin/env python3
"""
Script to parse CMakeLists.txt files and generate Doxygen documentation for CMake options.
"""
import re
import sys
import os
from pathlib import Path

def parse_cmake_options(cmake_file_path):
    """
    Parse a CMakeLists.txt file and extract all option() function calls.
    
    Args:
        cmake_file_path: Path to the CMakeLists.txt file
        
    Returns:
        List of dictionaries containing option name, description, and default value
    """
    options = []
    
    # Read the CMakeLists.txt file
    try:
        with open(cmake_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {cmake_file_path}: {e}", file=sys.stderr)
        return options
    
    # Regular expression to match option() calls
    # Format: option(<variable> "<help_text>" [value])
    option_pattern = r'option\s*\(\s*([A-Za-z0-9_-]+)\s+"([^"]*)"\s*(?:(ON|OFF|TRUE|FALSE))?\s*\)'
    
    # Find all matches
    for match in re.finditer(option_pattern, content, re.IGNORECASE):
        option_name = match.group(1)
        description = match.group(2)
        default_value = match.group(3) if match.group(3) else "OFF"  # Default is OFF if not specified
        
        options.append({
            'name': option_name,
            'description': description,
            'default': default_value
        })
    
    return options

def generate_doxygen_table(options):
    """
    Generate Doxygen-formatted table for the options.
    
    Args:
        options: List of dictionaries containing option details
        
    Returns:
        String containing Doxygen formatted table
    """
    if not options:
        return "No CMake options found."
    
    # Doxygen table header
    doxygen_output = [
        "The following CMake build options can be used to configure the build by setting them with `-D<OPTION>=<VALUE>`.",
        "",
        "| Option | Description | Default |",
        "|--------|-------------|---------|",
        "| CMAKE_INSTALL_PREFIX | Installation path | /usr/local |",
    ]
    
    # Add table rows
    for option in options:
        doxygen_output.append(f"| {option['name']} | {option['description']} | {option['default']} |")
    
    return "\n".join(doxygen_output)

def main():
    """
    Main function to parse command line arguments and process CMakeLists.txt files.
    """
    # Check if a file path was provided
    if len(sys.argv) > 1:
        cmake_path = sys.argv[1]
    else:
        # Default to looking for CMakeLists.txt in the current directory
        cmake_path = "CMakeLists.txt"
    
    # Validate path
    if not os.path.isfile(cmake_path):
        print(f"Error: File '{cmake_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Parse options and generate documentation
    options = parse_cmake_options(cmake_path)
    doxygen_doc = generate_doxygen_table(options)
    
    # Print to stdout
    print(doxygen_doc)

if __name__ == "__main__":
    main()
