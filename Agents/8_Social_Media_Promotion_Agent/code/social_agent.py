#!/usr/bin/env python3
import os

def promote_video():
    # Create a simple simulated social media post
    post = (
        "Check out our latest video: Breaking News on Asap Rocky! "
        "Watch now for in-depth analysis and insights. #BreakingNews #AsapRocky"
    )
    
    output_file = os.path.join(
        os.path.expanduser("~"),
        "Documents/youtube/Agents/8_Social_Media_Promotion_Agent/code/social_post.txt"
    )
    
    with open(output_file, "w") as f:
        f.write(post)
    
    print("Social media post generated and saved to", output_file)

if __name__ == '__main__':
    promote_video()

