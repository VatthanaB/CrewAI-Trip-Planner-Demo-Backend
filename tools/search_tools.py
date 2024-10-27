# Importing necessary modules
import json  # For working with JSON data
import os  # For interacting with the operating system (e.g., accessing environment variables)

import requests  # For making HTTP requests to external APIs
from langchain.tools import tool  # Importing the 'tool' decorator from LangChain library to define tools for interaction

# Defining a class 'SearchTools' to handle internet search functionality
class SearchTools():

    # Using the 'tool' decorator to define a function for searching the internet
    # The function is labeled as "Search the internet"
    @tool("Search the internet")
    def search_internet(query):
        """This function searches the internet for a given topic
        and returns relevant results."""
        
        top_result_to_return = 4  # Number of top results to return
        url = "https://google.serper.dev/search"  # URL endpoint for the Serper API (search API)
        
        # Creating a payload to send with the POST request, converting the query into JSON format
        payload = json.dumps({"q": query})
        
        # Defining the headers for the request, including the Serper API key and content type
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],  # Fetching API key from environment variables
            'content-type': 'application/json'  # Specifying the content type as JSON
        }
        
        # Sending the HTTP POST request to the search API with headers and payload
        response = requests.request("POST", url, headers=headers, data=payload)
        
        # Checking if the response contains the 'organic' key (this key holds search results)
        if 'organic' not in response.json():
            # If the key is missing, returning an error message
            return "Sorry, I couldn't find anything about that, there could be an error with your Serper API key."
        else:
            # If 'organic' results are found, process them
            results = response.json()['organic']  # Extracting the 'organic' search results
            string = []  # Initializing an empty list to store formatted result strings
            
            # Looping through the top results (up to the defined number)
            for result in results[:top_result_to_return]:
                try:
                    # Appending the formatted result (title, link, and snippet) to the list
                    string.append('\n'.join([
                        f"Title: {result['title']}",  # The title of the search result
                        f"Link: {result['link']}",  # The link to the search result
                        f"Snippet: {result['snippet']}",  # A brief snippet of the content
                        "\n-----------------"  # Separator for readability
                    ]))
                except KeyError:
                    # If any expected key (like 'title', 'link', or 'snippet') is missing, skip to the next result
                    next
            
            # Joining the formatted result strings with newline characters and returning the final output
            return '\n'.join(string)
