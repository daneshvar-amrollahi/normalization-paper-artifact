#!/usr/bin/env python3
import sys
import csv
from collections import defaultdict

def analyze_benchmarks(csv_file):
    # Dictionary to store similarity scores for each project
    project_scores = defaultdict(list)
    
    # Read CSV file
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract project name from benchmark field (everything before first '/')
            if '/' in row['benchmark']:
                project = row['benchmark'].split('/')[0]
                
                # Convert similarity score to float and add to appropriate project list
                try:
                    sim_score = float(row['avg_sim'])
                    project_scores[project].append(sim_score)
                except (ValueError, KeyError):
                    print(f"Warning: Could not parse similarity score for {row['benchmark']}")
    
    # Calculate and output statistics for each project
    print(f"{'Project':<15} {'Average':<10} {'Min':<10} {'Max':<10} {'Count':<10}")
    print("-" * 55)
    
    for project in sorted(project_scores.keys()):
        scores = project_scores[project]
        if scores:
            avg = sum(scores) / len(scores)
            min_score = min(scores)
            max_score = max(scores)
            count = len(scores)
            print(f"{project:<15} {avg:<10.2f} {min_score:<10.2f} {max_score:<10.2f} {count:<10}")
        else:
            print(f"{project:<15} No data available")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    analyze_benchmarks(csv_file)