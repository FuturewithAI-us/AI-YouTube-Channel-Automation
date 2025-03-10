#!/usr/bin/env python3
import os
import json

def optimize_metadata():
    # For simplicity, generate metadata based on a fixed template.
    metadata = {
        "title": "Breaking News on Asap Rocky",
        "description": "This video discusses trending news about Asap Rocky with background, analysis, and conclusion.",
        "tags": ["Asap Rocky", "Breaking News", "Analysis", "Trending"]
    }
    
    output_file = os.path.join(
        os.path.expanduser("~"),
        "Documents/youtube/Agents/7_SEO_Metadata_Optimization_Agent/code/metadata.json"
    )
    
    with open(output_file, "w") as f:
        json.dump(metadata, f, indent=4)
    
    print("SEO metadata generated and saved to", output_file)

if __name__ == '__main__':
    optimize_metadata()

