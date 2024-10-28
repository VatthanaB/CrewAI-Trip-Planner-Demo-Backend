from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def plan_itinerary(self, agent, city, travel_dates, interests):
        return Task(
            description=dedent(
                f"""
                **Task**: Develop a 7-Day Travel Itinerary
                **Description**: Create a detailed 7-day itinerary for {city} without any placeholders. 
                Each day must include specific restaurant names, hotel names, and dive shop names if relevant. 
                Find actual spots that align with traveler interests ({interests}) and the location, 
                ensuring every entry is a real place accessible during the specified travel dates ({travel_dates}).

                **Parameters**: 
                - City: {city}
                - Trip Date: {travel_dates}
                - Traveler Interests: {interests}

                **Note**: Do your BEST to provide detailed, real-world information to replace any generic terms.
            """
            ),
            agent=agent,
        )

    def identify_city(self, agent, origin, cities, interests, travel_dates):
        return Task(
            description=dedent(
                f"""
                    **Task**: Identify the Best City for the Trip
                    **Description**: Analyze and select the best city for the trip based on specific 
                        criteria such as weather patterns, seasonal events, and travel costs. 
                        This task involves comparing multiple cities, considering factors like current weather 
                        conditions, upcoming cultural or seasonal events, and overall travel expenses. 
                        Your final answer must be a detailed report on the chosen city, 
                        including actual flight costs, weather forecast, and attractions.

                    **Parameters**: 
                    - Origin: {origin}
                    - Cities: {cities}
                    - Interests: {interests}
                    - Travel Date: {travel_dates}

                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
        )

    def gather_city_info(self, agent, city, travel_dates, interests):
        return Task(
            description=dedent(
                f"""
                    **Task**: Gather In-depth City Guide Information
                    **Description**: Compile an in-depth guide for the selected city, gathering information about 
                        key attractions, local customs, special events, and daily activity recommendations. 
                        This guide should provide a thorough overview of what the city has to offer, including 
                        hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level costs.

                    **Parameters**: 
                    - Cities: {city}
                    - Interests: {interests}
                    - Travel Date: {travel_dates}

                    **Note**: {self.__tip_section()}
        """
            ),
            agent=agent,
        )

    def structure_info(self, agent, itinerary, city_info, identified_city):
        return Task(
            description=dedent(
                f"""
                    **Task**: Structure All Trip Information into a Comprehensive Report
                    **Description**: Compile and structure the outputs from the previous tasks into a single, complete trip report.
                        The report should include all sections—Introduction, City Overview, 7-Day Itinerary, Detailed City Information, 
                        Travel Logistics, and Travel Tips. Each section should have real names, locations, and other details, and 
                        there should be no placeholders such as `[no value]`, `[Hotel Name]`, or `[Attraction]`. Every section must
                        include actual names, with missing data handled intelligently, using tools or default suggestions.

                    **Parameters**: 
                    - Itinerary Details: {itinerary}
                    - City Information: {city_info}
                    - Identified City: {identified_city}

                    **Note**: {self.__tip_section()} Ensure that no placeholders are present in the final report. Verify that each
                    entry has specific names and values based on the gathered data.
            """
            ),
            agent=agent,
        )

