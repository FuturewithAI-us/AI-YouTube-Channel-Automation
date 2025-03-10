#!/usr/bin/env python3
import subprocess
import os
import sys

def run_agent(path):
    print(f"Running agent: {path}")
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"Error running agent: {path}", file=sys.stderr)
        sys.exit(result.returncode)

def main():
    base = os.path.expanduser("~")
    agents = [
        os.path.join(base, "Documents/youtube/Agents/1_Content_Research_Agent/code/content_research_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/2_Scriptwriting_Outline_Agent/code/scriptwriting_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/4_Voiceover_Audio_Agent/code/voiceover_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/5_Video_Creation_Editing_Agent/code/video_creation_agent_alternative.py"),
        os.path.join(base, "Documents/youtube/Agents/3_Content_Planning_Calendar_Agent/code/planning_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/6_Thumbnail_Graphic_Design_Agent/code/thumbnail_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/7_SEO_Metadata_Optimization_Agent/code/seo_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/8_Social_Media_Promotion_Agent/code/social_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/9_Analytics_Performance_Agent/code/analytics_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/10_Quality_Assurance_Agent/code/qa_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/11_High_Level_Manager_Agent/code/manager_agent.py"),
        os.path.join(base, "Documents/youtube/Agents/12_Video_Publishing_Agent/code/video_publishing_agent.py"),
    ]
    
    for agent in agents:
        if os.path.exists(agent):
            run_agent(agent)
        else:
            print(f"Agent not found: {agent}")
            # Optionally exit if a critical agent is missing:
            # sys.exit(1)
    print("Workflow complete.")

if __name__ == '__main__':
    main()

