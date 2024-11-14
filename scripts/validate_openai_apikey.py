from openai import OpenAI
import os  
from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv()
      
    # Set the OpenAI API key from the environment variable  
    OpenAI.api_key = os.environ["OPENAI_API_KEY"]  
    
    
    # Define client
    client = OpenAI()
      
    # Test the API key by retrieving the list of models  
    try:
        completion = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="Say this validation test was successful",
            max_tokens=7,
            temperature=0
        )
    
        print(completion.choices[0].text)
    except Exception as e:
        print(f'Failed with the following error messge: {e}')
