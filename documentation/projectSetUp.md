# **Detailed Documentation for Creating a CREWAI Work Team with AI Travel Planner Project**

This document provides a step-by-step guide on creating a **CREWAI work team** for your project, using a travel itinerary planner as an example. The example demonstrates the workflow of using CREWAI, setting up agents, defining tasks, and creating custom tools. By the end of this document, you'll understand how to structure your AI project to create an efficient, task-oriented team using AI agents.

We will also cover every detail of project setup, including dependency management via Poetry, tools for searching the internet and performing calculations, and the interaction between agents and tasks.

---

## **1. Project Setup with Poetry**

Poetry is a dependency management and packaging tool for Python. We will begin by creating the environment and configuring dependencies using Poetry.

### **Step 1.1: Poetry Configuration**

Below is the `pyproject.toml` file configuration for your project. This file declares the project metadata, dependencies, and tools used.

```toml
[tool.poetry]
name = "trip-planner-vatthana"
version = "0.1.0"
description = "Simple AI trip planner"
authors = ["Vatthana Boulom"]

[tool.poetry.dependencies]
python = ">=3.10.0,<3.12"
crewai = "0.1.24"
unstructured = "==0.10.25"   # Unstructured data handling
pyowm = "3.3.0"               # OpenWeatherMap API for weather forecasting
python-dotenv = "1.0.0"       # Load environment variables
langchain-openai = "^0.0.5"   # AI interaction via OpenAI models

[tool.pyright]
useLibraryCodeForTypes = true
exclude = [".cache"]

[tool.ruff]
select = ['E', 'W', 'F', 'I', 'B', 'C4', 'ARG', 'SIM']
ignore = ['W291', 'W292', 'W293']

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### **Step 1.2: Installing Dependencies**

After creating the `pyproject.toml` file, run the following command to install the dependencies:

```bash
poetry install
```

This will create a virtual environment and install the required libraries for your project.

---

## **2. Understanding the Project Structure**

For the AI Trip Planner, we will create three main components:

1. **Agents**: These are the virtual "employees" that execute tasks.
2. **Tasks**: Actions that the agents must complete.
3. **Tools**: External utilities that help the agents perform certain actions, like searching the web or performing calculations.

### **Project File Structure**

Here’s how your project structure might look:

```
trip-planner-vatthana/
│
├── pyproject.toml                # Poetry configuration file
├── main.py                       # Main script to run the CREWAI work team
├── agents.py                     # Defines agents (AI assistants)
├── tasks.py                      # Defines tasks (work to be done by agents)
├── tools/
│   ├── search_tools.py           # Search tool to gather information from the internet
│   └── calculator_tools.py       # Calculation tool for mathematical operations
├── .env                          # Stores environment variables (e.g., API keys)
└── README.md                     # Project documentation
```

---

## **3. Creating the Tools**

### **Step 3.1: Internet Search Tool**

The `search_tools.py` will contain a tool that allows agents to search the web for relevant information. This tool interacts with a search API (e.g., Serper) to retrieve search results.

```python
import json
import os
import requests
from langchain.tools import tool  # CREWAI's tool decorator for defining tools

class SearchTools:
    @tool("Search the internet")
    def search_internet(query: str) -> str:
        """
        This tool searches the internet for a given query and returns relevant results.
        It uses the Serper API for performing the search.
        """
        top_result_to_return = 4  # Limit to 4 top search results
        url = "https://google.serper.dev/search"  # API endpoint for search

        # Create a payload with the query
        payload = json.dumps({"q": query})

        # Define headers, including the API key fetched from environment variables
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],  # Ensure to set your API key in .env
            'content-type': 'application/json'
        }

        # Send request to Serper API
        response = requests.post(url, headers=headers, data=payload)

        # Handle response and extract search results
        if 'organic' not in response.json():
            return "No results found or API key error."
        else:
            results = response.json()['organic']
            formatted_results = []

            for result in results[:top_result_to_return]:
                formatted_results.append(
                    f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n-------------------"
                )

            return "\n\n".join(formatted_results)
```

**Explanation**:

- This tool searches the web using a search API.
- It formats and returns the top results in a readable way.
- Ensure your `.env` file contains the `SERPER_API_KEY`.

---

### **Step 3.2: Calculator Tool**

The `calculator_tools.py` will contain a tool to perform mathematical calculations.

```python
from langchain.tools import tool

class CalculatorTools:
    @tool("Make a calculation")
    def calculate(operation: str) -> str:
        """
        This tool performs basic mathematical operations.
        Example inputs: '200*7', '5000/2', '45+20'
        """
        try:
            return str(eval(operation))  # Using eval to execute the calculation
        except (SyntaxError, ZeroDivisionError):
            return "Error: Invalid mathematical expression or division by zero."
```

**Explanation**:

- This tool evaluates mathematical expressions provided as strings.
- The `eval` function is used for dynamic execution of the operation, and we handle common errors such as invalid syntax or division by zero.

---

## **4. Defining Agents**

Agents are the key actors in the project. They are responsible for handling specific roles like city selection, itinerary planning, and gathering city information.

### **Step 4.1: Creating Agents in `agents.py`**

```python
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools

class TravelAgents:
    def __init__(self):
        # Initialize OpenAI models for agents to use
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    def expert_travel_agent(self):
        # The primary agent responsible for overall travel planning
        return Agent(
            role="Expert Travel Agent",
            backstory="Expert in travel planning and logistics. I have decades of experience making travel itineraries.",
            goal="Create a detailed 7-day travel itinerary, including budget, packing suggestions, and safety tips.",
            tools=[SearchTools.search_internet, CalculatorTools.calculate],
            llm=self.OpenAIGPT35,  # Using GPT-3.5 model for conversations
            verbose=True,
        )

    def city_selection_expert(self):
        # Agent responsible for analyzing travel data to select the best cities
        return Agent(
            role="City Selection Expert",
            backstory="Expert at analyzing travel data to pick ideal destinations.",
            goal="Select the best cities based on weather, season, prices, and traveler interests.",
            tools=[SearchTools.search_internet],  # This agent only needs the search tool
            llm=self.OpenAIGPT35,
            verbose=True,
        )

    def local_tour_guide(self):
        # Agent with knowledge about local attractions and recommendations
        return Agent(
            role="Local Tour Guide",
            backstory="Knowledgeable local guide with extensive information about the city, its attractions, and customs.",
            goal="Provide the best insights about the selected city, including hidden gems, local customs, and activities.",
            tools=[SearchTools.search_internet],
            llm=self.OpenAIGPT35,
            verbose=True,
        )
```

**Explanation**:

- **Expert Travel Agent**: This agent is responsible for creating a full itinerary using internet search and basic calculations.
- **City Selection Expert**: This agent analyzes data to select the best cities for travel, using the internet search tool.
- **Local Tour Guide**: This agent focuses on local knowledge, gathering insights about the selected city.

---

## **5. Defining Tasks**

Tasks are the specific actions agents perform. In this case, agents will be assigned tasks like itinerary planning, city selection, and gathering local information.

### **Step 5.1: Defining Tasks in `tasks.py`**

```python
from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def plan_itinerary(self, agent, city, travel_dates, interests):
        return Task(
            description=dedent(f"""
                **Task**: Develop a 7-Day Travel It

inerary
                **Description**: Create a detailed 7-day travel itinerary for the selected city, including
                daily activities, weather forecasts, budget, and packing suggestions.
                This must include recommendations for restaurants, hotels, and places to visit.

                **Parameters**:
                - City: {city}
                - Trip Date: {travel_dates}
                - Traveler Interests: {interests}

                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )

    def identify_city(self, agent, origin, cities, interests, travel_dates):
        return Task(
            description=dedent(f"""
                **Task**: Identify the Best City for the Trip
                **Description**: Analyze weather patterns, cultural events, and costs to determine the best city
                for this trip. The final output should include detailed information about the chosen city,
                including weather forecasts, events, and flight costs.

                **Parameters**:
                - Origin: {origin}
                - Cities: {cities}
                - Traveler Interests: {interests}
                - Travel Date: {travel_dates}

                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )

    def gather_city_info(self, agent, cities, travel_dates, interests):
        return Task(
            description=dedent(f"""
                **Task**: Gather In-depth City Guide Information
                **Description**: Create a guide for the chosen city, detailing key attractions, local customs,
                recommended activities, and hidden gems. Include high-level costs and a weather forecast.

                **Parameters**:
                - City: {cities}
                - Traveler Interests: {interests}
                - Travel Date: {travel_dates}

                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )
```

**Explanation**:

- **plan_itinerary**: This task requires the agent to build a full 7-day itinerary with suggestions for restaurants, hotels, and activities.
- **identify_city**: This task asks the agent to analyze various cities and choose the best one for the trip.
- **gather_city_info**: This task asks the agent to gather detailed information about the city, including local attractions and recommendations.

---

## **6. Running the CREWAI Work Team**

### **Step 6.1: Putting It All Together in `main.py`**

```python
from crewai import Crew
from agents import TravelAgents
from tasks import TravelTasks
from dotenv import load_dotenv

# Load environment variables from .env file (e.g., Serper API key)
load_dotenv()

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        # Initialize agents and tasks
        agents = TravelAgents()
        tasks = TravelTasks()

        # Create agents
        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        # Define tasks and assign agents
        plan_itinerary = tasks.plan_itinerary(expert_travel_agent, self.cities, self.date_range, self.interests)
        identify_city = tasks.identify_city(city_selection_expert, self.origin, self.cities, self.interests, self.date_range)
        gather_city_info = tasks.gather_city_info(local_tour_guide, self.cities, self.date_range, self.interests)

        # Create and run the CREWAI work team
        crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
            tasks=[plan_itinerary, identify_city, gather_city_info],
            verbose=True,
        )

        result = crew.kickoff()  # Run the crew
        return result

# Main entry point for the application
if __name__ == "__main__":
    print("## Welcome to the Trip Planner Crew")
    origin = input("From where will you be traveling from? ")
    cities = input("Which cities are you interested in visiting? ")
    date_range = input("What is the date range for your trip? ")
    interests = input("What are your main interests and hobbies? ")

    trip_crew = TripCrew(origin, cities, date_range, interests)
    result = trip_crew.run()

    print("\n\n########################")
    print("## Here is your Trip Plan")
    print("########################\n")
    print(result)
```

---

## **7. Key Steps Summary**

### **Step 1: Set Up the Environment**

- Use `Poetry` to manage dependencies.
- Install `CREWAI`, `unstructured`, `pyowm`, `python-dotenv`, and `langchain-openai` for your project.

### **Step 2: Create the Tools**

- **SearchTools** for web searches using Serper API.
- **CalculatorTools** for performing simple calculations.

### **Step 3: Define the Agents**

- Define different agents for city selection, itinerary planning, and local tour guiding.

### **Step 4: Assign Tasks**

- Break the project into smaller tasks such as planning an itinerary, selecting cities, and gathering detailed city information.

### **Step 5: Run the Work Team**

- Create a `Crew` that brings together agents and tasks to execute your project.

---

## **Conclusion**

By following this detailed guide, you can create a dynamic CREWAI work team for your own project. This process provides a clear and structured way to handle AI-powered tasks using agents, each responsible for specific jobs. With the custom tools, agents, and tasks in place, your AI-powered trip planner can efficiently build detailed travel itineraries and provide users with insightful recommendations.
