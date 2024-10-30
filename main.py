from flask import Flask, request, jsonify
from flask_cors import CORS
from crewai import Crew  # assuming Crew is a valid import path
from agents import TravelAgents
from tasks import TravelTasks
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        # Set up agents and tasks
        agents = TravelAgents()
        tasks = TravelTasks()
        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()
        result_structuring_expert = agents.result_structuring_expert()

        # Define tasks
        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent, self.cities, self.date_range, self.interests
        )
        identify_city = tasks.identify_city(
            city_selection_expert, self.origin, self.cities, self.interests, self.date_range
        )
        gather_city_info = tasks.gather_city_info(
            local_tour_guide, self.cities, self.date_range, self.interests
        )
        # # New task to structure all gathered information
        # structure_info = tasks.structure_info(
        #     agent=result_structuring_expert,
        #     itinerary=plan_itinerary,
        #     city_info=gather_city_info,
        #     identified_city=identify_city
        # )

        # Crew setup
        crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide, result_structuring_expert],
            tasks=[plan_itinerary, identify_city, gather_city_info],
            verbose=True,
        )

        # Execute the crew and ensure result length
        result = crew.kickoff()
        attempt_count = 1  # Track the number of attempts
        max_attempts = 5  # Limit the number of retries to prevent infinite loop

        while len(result) < 1500 and attempt_count < max_attempts:
            print(f"Result is under 1200 characters. Retrying... Attempt {attempt_count}")
            result = crew.kickoff()  # Restart the crew
            attempt_count += 1

        if len(result) < 1500:
            print("Unable to generate a result over 1200 characters after multiple attempts.")
            result += "\n\nAdditional insights and data are currently being gathered. Please check back later or contact support for more details."

        return result

# Route to check if the server is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Trip Planner Crew API is running'})

@app.route('/api/trip-plan', methods=['POST'])
def trip_plan():
    data = request.json
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400

    origin = data.get('origin') 
    cities = data.get('cities')
    date_range = data.get('date_range')
    interests = data.get('interests')

    # Run TripCrew
    trip_crew = TripCrew(origin, cities, date_range, interests)
    result = trip_crew.run()

    # Return the result
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
