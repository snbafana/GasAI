from instructor import OpenAISchema
from pydantic import Field, field_validator
import subprocess
from typing import List
import os
from bs4 import BeautifulSoup
import requests
import re
import asyncio


class LinkedINSearch(OpenAISchema):
    linkedinurl: str = Field(..., description="Linkedin URL of the person")
    
    @field_validator("linkedinurl")
    @classmethod
    def validate_url(cls, v):
        if "https://www.linkedin.com/in/" not in v:
            raise ValueError("LinkedIN Profile Link is not correct")
        return v
    
    
    async def run(self):

        import json

        headers = {'Authorization': 'Bearer ' + os.environ['PROXYCURL_API_KEY']}

        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

        params = {

            'linkedin_profile_url': self.linkedinurl,
            
            'use_cache': 'if-recent',

            'fallback_to_cache': 'on-error',

        }

        response = requests.get(api_endpoint,

                                params=params,

                                headers=headers)

        # Check if the request was successful

        if response.status_code == 200:

            # Parse and print the content of the response in a formatted manner

            data = response.json()

            return json.dumps(data, indent=4)

        else:

            print(f"Error: {response.status_code}")