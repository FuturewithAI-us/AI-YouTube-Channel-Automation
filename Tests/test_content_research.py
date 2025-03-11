import pytest
from Agents.Content_Research_Agent.code.content_research_agent import ContentResearchAgent

def test_fetch_trends_success():
    """Test successful trend fetching."""
    agent = ContentResearchAgent()
    trends = agent.fetch_trends("AI")
    assert isinstance(trends, list), "Trends should be a list"
    assert len(trends) > 0, "No trends found"

def test_fetch_trends_failure():
    """Test API failure handling."""
    agent = ContentResearchAgent()
    with pytest.raises(Exception):
        agent.fetch_trends("InvalidTopic@123")
