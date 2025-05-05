#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# Create a temporary file
temp_file=$(mktemp)

# Use awk to remove duplicates while preserving order
awk '!seen[$0]++' "$filename" > "$temp_file"

# Replace the original file with the deduplicated content
mv "$temp_file" "$filename"