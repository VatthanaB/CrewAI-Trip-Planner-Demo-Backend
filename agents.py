from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools

class TravelAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory="Experienced in planning detailed travel itineraries with real-world insights and cost-efficiency.",
            goal="Develop a 7-day itinerary with real recommendations for restaurants, hotels, and activities tailored to the travel dates and interests.",
            tools=[SearchTools.search_internet, CalculatorTools.calculate],
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory="Analyst focused on optimizing city choices based on weather, season, and budget.",
            goal="Compare and select the ideal city based on origin, travel dates, and interests with a weather, event, and cost breakdown.",
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory="Local expert with insights into hidden gems, local customs, and must-see spots.",
            goal="Provide a detailed city guide with specific attractions, local tips, and daily activity recommendations.",
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def result_structuring_expert(self):
        return Agent(
            role="Result Structuring Expert",
            backstory="Specialist in organizing travel data into a comprehensive, readable report.",
            goal="Structure gathered information into a cohesive report covering itinerary, logistics, and tips without placeholders.",
            tools=[CalculatorTools.calculate],
            verbose=True,
            llm=self.OpenAIGPT35,
        )
