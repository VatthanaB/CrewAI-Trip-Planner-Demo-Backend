from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __tip_section(self):
        return "Deliver detailed, complete responses to qualify for a quality bonus!"

    def plan_itinerary(self, agent, cities, travel_dates, interests):
        return Task(
            description=dedent(f"""
                **Task**: Develop a 7-Day Travel Itinerary
                **Description**: Create a full 7-day itinerary for {', '.join(cities)}, including specific recommendations 
                for restaurants, accommodations, and attractions that match the traveler's interests ({interests}). 
                Detail per-day activities with times and costs.
                
                **Parameters**: 
                - Cities: {cities}
                - Dates: {travel_dates}
                - Interests: {interests}
                
                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )

    def identify_city(self, agent, origin, cities, interests, travel_dates):
        return Task(
            description=dedent(f"""
                **Task**: Identify the Best City for the Trip
                **Description**: Evaluate each city in {cities} for weather, seasonal events, and travel expenses 
                during {travel_dates}. Recommend the top city with details on weather, flight costs, and highlights.

                **Parameters**: 
                - Origin: {origin}
                - Cities: {cities}
                - Interests: {interests}
                - Dates: {travel_dates}

                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )

    def gather_city_info(self, agent, cities, travel_dates, interests):
        return Task(
            description=dedent(f"""
                **Task**: Gather In-depth City Guide Information
                **Description**: Compile an in-depth city guide with key attractions, local customs, 
                hidden gems, and high-level cost estimates in {cities} for travel dates {travel_dates}. 
                
                **Parameters**: 
                - Cities: {cities}
                - Dates: {travel_dates}
                - Interests: {interests}

                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )

    def structure_info(self, agent, itinerary, city_info, identified_city):
        return Task(
            description=dedent(f"""
                **Task**: Structure All Trip Information into a Comprehensive Report
                **Description**: Organize all travel information into a single report covering itinerary, 
                city guides, logistics, and travel tips. Ensure no placeholders are present, and all data is 
                cohesive and complete for easy reading.
                
                **Parameters**: 
                - Itinerary: {itinerary}
                - City Info: {city_info}
                - Identified City: {identified_city}

                **Note**: {self.__tip_section()}
            """),
            agent=agent,
        )
