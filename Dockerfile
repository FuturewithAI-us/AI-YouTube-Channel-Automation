FROM python:3.8

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "Agents/1_Content_Research_Agent/code/content_research_agent.py"]
