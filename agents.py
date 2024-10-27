from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools

class TravelAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(
                f"""Expert in travel planning and logistics. 
                I have decades of experience making travel itineraries."""),
            goal=dedent(f"""
                        Create a 7-day travel itinerary with detailed per-day plans,
                        including budget, packing suggestions, and safety tips.
                        """),
            tools=[
                SearchTools.search_internet,
                CalculatorTools.calculate
            ],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory=dedent(
                f"""Expert at analyzing travel data to pick ideal destinations"""),
            goal=dedent(
                f"""Select the best cities based on weather, season, prices, and traveler interests"""),
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(f"""Knowledgeable local guide with extensive information
        about the city, its attractions, and customs"""),
            goal=dedent(
                f"""Provide the BEST insights about the selected city"""),
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def result_structuring_expert(self):
        return Agent(
            role="Result Structuring Expert",
            backstory=dedent(
                f"""Experienced report writer and travel document organizer. 
                I have expertise in structuring and presenting information in an easy-to-read, 
                cohesive format that covers all details and ensures clarity."""),
            goal=dedent(
                f"""Structure the gathered travel information into a comprehensive report, 
                including a 7-day itinerary, city details, and recommendations. Ensure the report 
                is organized, easy to read, and covers all relevant aspects of the trip."""),
            tools=[CalculatorTools.calculate],
            verbose=True,
            llm=self.OpenAIGPT35,
        )
