import openai
import json

class LLMParsingAgent:
    def __init__(self, azure_api_key: str, azure_endpoint: str, deployment_name: str):
        openai.api_type = "azure"
        openai.api_key = azure_api_key
        openai.api_base = azure_endpoint
        openai.api_version = "2023-05-15"
        self.deployment_name = deployment_name

    def parse(self, text: str) -> dict:
        prompt = f"""
You are a general-purpose data extraction agent. Given the following text, extract all numerical data and structure it for use in data visualization.

For each data point, return:
- "value": the numeric value (as a float or string if needed)
- "unit": the unit or type (e.g., %, USD, date, count, kg, etc.)
- "label": a short label or category for the data (e.g., "Revenue", "Population", "Growth Rate")
- "context": the full sentence or phrase where the data appears
- "timestamp": if the data is time-related, extract the date or time reference (optional)

Respond in JSON format as:
{{
  "data_points": [
    {{
      "value": ...,
      "unit": "...",
      "label": "...",
      "context": "...",
      "timestamp": "..." (optional)
    }},
    ...
  ]
}}

Text:
\"\"\"{text}\"\"\"
"""

        response = openai.ChatCompletion.create(
            engine=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful data extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1200
        )

        content = response['choices'][0]['message']['content']
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM response", "raw_response": content}