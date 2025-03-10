#!/usr/bin/env python3
import os
import pandas as pd

def generate_script_outline():
    # Define the path to the trending topics file from the Content Research Agent
    trending_file = os.path.join(
        os.path.expanduser("~"),
        "Documents/youtube/Agents/1_Content_Research_Agent/code/trending_topics.txt"
    )
    
    # Check if the file exists
    if not os.path.exists(trending_file):
        print("Trending topics file not found. Please run the Content Research Agent first.")
        return
    
    # Read the trending topics file (assuming it's in CSV format)
    try:
        trending_df = pd.read_csv(trending_file)
    except Exception as e:
        print("Error reading trending topics file:", e)
        return
    
    if trending_df.empty:
        print("Trending topics file is empty.")
        return
    
    # For simplicity, select the first trending topic from the file
    trending_topic = trending_df.iloc[0, 0]
    print("Selected trending topic:", trending_topic)
    
    # Generate a simple script outline with pause markers
    outline = f"""Video Title: Breaking News on {trending_topic}

Script Outline:
1. Introduction: Briefly introduce the trending topic. [PAUSE]
2. Background: Provide context and background on {trending_topic}. [PAUSE]
3. Analysis: Discuss the implications and various viewpoints. [PAUSE]
4. Conclusion: Summarize the key points and invite viewers to comment. [PAUSE]
"""
    print(outline)
    
    # Save the outline to a file
    output_dir = os.path.join(os.path.expanduser("~"), 
                              "Documents/youtube/Agents/2_Scriptwriting_Outline_Agent/code")
    output_file = os.path.join(output_dir, "script_outline.txt")
    with open(output_file, "w") as f:
        f.write(outline)
    print("Script outline saved to", output_file)

if __name__ == '__main__':
    generate_script_outline()
