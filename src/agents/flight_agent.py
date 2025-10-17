import os
import requests
import json
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
# from agno.models.openai import OpenAIChat
from src.tools.base_tools import search_sabre_flights
from agno.models.google import Gemini
from dotenv import load_dotenv
load_dotenv(override=True)

# Create Knowledge Instance with ChromaDB
knowledge = Knowledge(
    name="Basic SDK Knowledge Base",
    description="Agno 2.0 Knowledge Implementation with ChromaDB",
    vector_db=ChromaDb(
        collection="vectors", path="tmp/chromadb", persistent_client=True
    ),
)
knowledge.add_content_async(
        name="Recipes",
        path="src/utils/airports.json",
        metadata={"doc_type": "recipe_book"},
    )


# Create your Sabre flight agent
sabre_agent = Agent(
    name="Sabre Flight Search Agent",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[search_sabre_flights],
    knowledge=knowledge,
    instructions=[
        "You are a flight search specialist using Sabre APIs",
        "Help users find flights with clear pricing and schedules",
        "Always ask for required parameters: PCC, origin, destination, dates"
    ],
    markdown=True
)

# Test the agent
sabre_agent.print_response(
    "Search for flights from MIA to MCO departing 2025-10-10 and returning 2025-10-20, use PCC 7C18"
)