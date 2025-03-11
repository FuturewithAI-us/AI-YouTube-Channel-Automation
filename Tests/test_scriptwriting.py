import pytest  
from Agents.Scriptwriting_Agent.code.scriptwriting_agent import generate_script  

def test_script_generation():  
    script = generate_script({"topic": "AI"})  
    assert "AI" in script, "Topic missing in script"  
