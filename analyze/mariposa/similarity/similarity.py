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
                    print(f"Warning : Invalid data for benchmark {row['benchmark']}. Skipping.")
                    pass
    
    # Calculate and output average for each project
    print(f"{'Project':<15} {'Average':<10}")
    print("-" * 25)
    
    for project in sorted(project_scores.keys()):
        scores = project_scores[project]
        if scores:
            avg = sum(scores) / len(scores)
            print(f"{project:<15} {avg:<10.2f}")
        else:
            print(f"{project:<15} No data available")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    analyze_benchmarks(csv_file)