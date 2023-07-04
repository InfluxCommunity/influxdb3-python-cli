import json
import os
import openai

class OpenAIHelper:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key

    def nl_to_sql(self, natural_language_query):
        try:
            # Construct the prompt to ask GPT to convert the natural language query to SQL
            prompt = f"""
            I have a natural language query and I need you to convert it into an INFLUXQL query. 
            Please ensure that the output is a valid INFLUXQL query.

            Natural Language Query: '{natural_language_query}'

            INFLUXQL Query:"""

            messages = [{"role": "user", "content": prompt }]
            
            # Send the prompt to GPT-3
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613", 
                messages=messages,
            )
            
            # Extract the SQL query from the response
            sql_query = response["choices"][0]["message"]
            sql_query = sql_query["content"]
 
            return sql_query
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

