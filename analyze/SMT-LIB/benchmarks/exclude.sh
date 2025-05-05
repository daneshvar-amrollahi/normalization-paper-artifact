#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <file1> <file2>" >&2
    exit 1
fi

file1=$1
file2=$2

# Check if files exist
if [ ! -f "$file1" ]; then
    echo "Error: File '$file1' not found." >&2
    exit 1
fi

if [ ! -f "$file2" ]; then
    echo "Error: File '$file2' not found." >&2
    exit 1
fi

# Create a temporary file with patterns from file2
# Prefix each line with .* and suffix with .* to allow for partial matching
temp_patterns=$(mktemp)
sed 's/^/.*/' "$file2" | sed 's/$/.*/' > "$temp_patterns"

# Use grep to filter file1, excluding lines that match patterns from file2
grep -v -f "$temp_patterns" "$file1"

# Clean up
rm "$temp_patterns"