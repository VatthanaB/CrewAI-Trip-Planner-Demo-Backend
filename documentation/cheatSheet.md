Sure! Below are cheat sheets for each step in the process, along with best practices and reusable instructions for creating future AI workers (agents, tasks, and tools) in CREWAI projects.

---

## **Step 1: Environment Setup Cheat Sheet**

### **Best Practices for Environment Setup**:

1. **Use Poetry**: For dependency management, Poetry simplifies packaging and dependency installation.
2. **Organize Your Project**: Ensure your project structure is clean and modular.
3. **Use `.env` Files for Sensitive Data**: Store API keys and credentials in environment variables.

### **Reusable Instructions**:

1. **Create the Project**:
   - Run: `poetry new project-name` to initialize the project.
   - Update `pyproject.toml` with your project metadata, dependencies, and tools.
2. **Set Up Dependencies**:
   - Add dependencies using `poetry add <package-name>`. For example:
     - `poetry add crewai`
     - `poetry add langchain-openai`
3. **Organize Project Structure**:

   - Follow a structure like:
     ```
     project-name/
     ├── pyproject.toml
     ├── main.py
     ├── agents.py
     ├── tasks.py
     ├── tools/
     ├── .env
     └── README.md
     ```

4. **Load Environment Variables**:
   - Install `python-dotenv` using `poetry add python-dotenv`.
   - Add sensitive keys in `.env` (e.g., `SERPER_API_KEY=<your-api-key>`).
   - Use `load_dotenv()` to load environment variables in your scripts.

---

## **Step 2: Creating Tools Cheat Sheet**

### **Best Practices for Tool Creation**:

1. **Reusability**: Design tools that can be reused across multiple agents and tasks.
2. **Simplicity**: Keep tools focused on one task (e.g., web search, calculations).
3. **Error Handling**: Ensure tools handle errors gracefully, such as invalid inputs or failed API requests.

### **Reusable Instructions**:

1. **Create a New Tool**:

   - Tools should be placed inside a dedicated `tools/` folder.
   - Use the `@tool` decorator from CREWAI to define reusable functions.

2. **Structure Example**: For a **search tool**:

   ```python
   from langchain.tools import tool
   import requests
   import os

   class SearchTools:
       @tool("Search the internet")
       def search_internet(query: str) -> str:
           # Add your search logic here, including API calls
           try:
               response = requests.post(
                   "https://google.serper.dev/search",
                   headers={"X-API-KEY": os.getenv('SERPER_API_KEY')},
                   json={"q": query}
               )
               return response.json()['organic']
           except Exception as e:
               return f"Error: {e}"
   ```

3. **Follow These Steps**:
   - **Define the Purpose**: What action is this tool performing (e.g., web search)?
   - **Create Parameters**: Input arguments should be clear and easy to use.
   - **Return Results**: Return results in a consistent format.
   - **Handle Errors**: Provide user-friendly error messages when things go wrong.

---

## **Step 3: Creating Agents Cheat Sheet**

### **Best Practices for Agent Creation**:

1. **Think Like a Manager**: Agents should be experts in a specific domain with clear roles and goals.
2. **Goal-Oriented**: Each agent must have a clearly defined goal.
3. **Tool Integration**: Agents should be assigned the appropriate tools to achieve their goals.

### **Reusable Instructions**:

1. **Define the Agent’s Role and Backstory**:

   - Agents should have distinct roles (e.g., "Expert Travel Planner", "City Selection Expert").
   - Each agent should have a relevant backstory to help guide its actions.

2. **Use LLMs (Large Language Models)**:

   - Agents rely on LLMs like `gpt-3.5-turbo` or `gpt-4`. Configure these in the agent definition.
   - Example:

     ```python
     from crewai import Agent
     from langchain_openai import ChatOpenAI

     class TravelAgents:
         def expert_travel_agent(self):
             return Agent(
                 role="Expert Travel Agent",
                 backstory="Decades of experience in travel planning.",
                 goal="Create a 7-day travel itinerary including budget, packing, and safety tips.",
                 tools=[SearchTools.search_internet, CalculatorTools.calculate],
                 llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
                 verbose=True
             )
     ```

3. **Assign Tools**:

   - Make sure each agent has the necessary tools to complete its tasks. For example:
     ```python
     tools=[SearchTools.search_internet, CalculatorTools.calculate]
     ```

4. **Agent Reusability**:
   - Create agents that can be reused in different projects by assigning them specific, domain-agnostic goals (e.g., general research, planning, etc.).

---

## **Step 4: Creating Tasks Cheat Sheet**

### **Best Practices for Task Creation**:

1. **Start with the Goal**: Each task should move toward achieving a well-defined outcome.
2. **Break Down Big Goals**: Divide large tasks into smaller, manageable tasks that agents can handle.
3. **Descriptive and Clear**: Provide a clear, actionable description for each task. This should outline exactly what the agent is expected to do.

### **Reusable Instructions**:

1. **Define the Task Structure**:

   - Use a class structure to define tasks and methods for each specific task. Example:

     ```python
     from crewai import Task
     from textwrap import dedent

     class TravelTasks:
         def plan_itinerary(self, agent, city, travel_dates, interests):
             return Task(
                 description=dedent(f"""
                     **Task**: Develop a 7-Day Travel Itinerary
                     **Description**: Create a detailed itinerary with daily plans including weather forecasts, packing suggestions, and a budget breakdown.

                     **Parameters**:
                     - City: {city}
                     - Trip Date: {travel_dates}
                     - Traveler Interests: {interests}
                 """),
                 agent=agent
             )
     ```

2. **Task Breakdown**:

   - For each task, define:
     - **Task Summary**: What is the task aiming to achieve?
     - **Detailed Instructions**: What are the exact steps the agent should follow?
     - **Parameters**: What inputs (e.g., city, travel dates) are needed?

3. **Assign Tasks to Agents**:
   - Match each task to the correct agent, ensuring the agent has the necessary tools and expertise.
     ```python
     travel_tasks = TravelTasks()
     plan_itinerary = travel_tasks.plan_itinerary(agent=expert_travel_agent, city="Paris", travel_dates="2024-06-01 to 2024-06-07", interests="history, food")
     ```

---

## **Step 5: Crew Execution Cheat Sheet**

### **Best Practices for Crew Execution**:

1. **Define Roles Clearly**: Each agent must have a specific role and should not overlap with others.
2. **Sequential Task Execution**: Tasks should flow logically from one agent to another, ensuring that each agent’s output feeds into the next.
3. **Verbose Mode for Debugging**: Use the verbose flag to get detailed information about task execution for debugging purposes.

### **Reusable Instructions**:

1. **Define the Crew in `main.py`**:

   - Organize the agents and tasks into a `Crew` and use the `kickoff()` method to run the crew.

     ```python
     from crewai import Crew
     from agents import TravelAgents
     from tasks import TravelTasks

     # Initialize agents and tasks
     agents = TravelAgents()
     tasks = TravelTasks()

     # Define the agents
     expert_travel_agent = agents.expert_travel_agent()
     city_selection_expert = agents.city_selection_expert()
     local_tour_guide = agents.local_tour_guide()

     # Define the tasks
     plan_itinerary_task = tasks.plan_itinerary(expert_travel_agent, city="Paris", travel_dates="2024-06-01 to 2024-06-07", interests="history, food")
     identify_city_task = tasks.identify_city(city_selection_expert, origin="London", cities=["Paris", "Rome"], interests="history", travel_dates="2024-06-01 to 2024-06-07")

     # Create and execute the crew
     crew = Crew(
         agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
         tasks=[plan_itinerary_task, identify_city_task],
         verbose=True
     )

     result = crew.kickoff()
     print(result)
     ```

2. **Crew Reusability**:
   - You can reuse the same crew setup for other projects by swapping agents and tasks.

---

## **Final Summary: Best Practices for Future CREWAI Projects**

1. **Environment Setup**: Use Poetry and `.env` files to manage dependencies and sensitive data.
2. **Tool Creation**: Create simple, reusable tools (e.g., search tools, calculator tools) that can be shared across multiple agents.
3. **Agent Definition**: Define agents with clear roles and backstories. Assign each agent specific tools and goals.
4. **Task Creation**: Break down the project’s goal into manageable tasks. Ensure each task has clear instructions and is

assigned to the right agent. 5. **Crew Execution**: Use CREWAI to organize agents and tasks into a work team, executing tasks in sequence. Leverage verbose mode for easier debugging.

By following these cheat sheets, you'll have a solid foundation for building CREWAI-based AI workers that are highly modular, reusable, and efficient for future projects.
