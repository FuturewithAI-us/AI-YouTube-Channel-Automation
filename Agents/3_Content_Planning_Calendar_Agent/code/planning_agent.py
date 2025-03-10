#!/usr/bin/env python3
import os
from datetime import datetime, timedelta

def plan_content():
    # For simplicity, schedule the video 1 day from now
    scheduled_date = datetime.now() + timedelta(days=1)
    scheduled_date_str = scheduled_date.strftime("%Y-%m-%d %H:%M:%S")
    
    plan_file = os.path.join(
        os.path.expanduser("~"),
        
"Documents/youtube/Agents/3_Content_Planning_Calendar_Agent/code/content_calendar.txt"
    )
    
    with open(plan_file, "w") as f: f.write(f"Video scheduled for publication on: {scheduled_date_str}\n")
    
    print("Content scheduled for publication on:", scheduled_date_str)
    print("Calendar saved to", plan_file)

if __name__ == '__main__':
    plan_content()

