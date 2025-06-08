from typing import Dict, Any, List
import ollama
from datetime import datetime

class OllamaAgent:
    def __init__(self, model_name: str = "gemma:3b"):
        self.model = model_name
        self.system_prompt = """You are an intelligent email assistant. Your tasks are:
1. Analyze email content for intent and urgency
2. Categorize emails into: urgent, meeting, inquiry, follow_up, or general
3. Determine if the email requires immediate attention
4. Generate appropriate responses
5. Assign priority levels (0-3) based on content analysis

Be concise and accurate in your analysis."""
    
    def analyze_email(self, subject: str, snippet: str) -> Dict[str, Any]:
        """Analyze email content using Ollama."""
        prompt = f"""Analyze this email:
Subject: {subject}
Content: {snippet}

Provide analysis in JSON format with these fields:
- category: one of [urgent, meeting, inquiry, follow_up, general]
- priority: number 0-3
- requires_attention: boolean
- intent: brief description of email's purpose
- suggested_response: brief template for response"""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                system=self.system_prompt
            )
            
            # Extract JSON from response
            analysis = self._parse_ollama_response(response['response'])
            return analysis
        except Exception as e:
            print(f"Error in Ollama analysis: {e}")
            return self._get_default_analysis()
    
    def generate_response(self, email_data: Dict[str, Any]) -> str:
        """Generate a response using Ollama."""
        prompt = f"""Generate a response for this email:
Category: {email_data['category']}
Priority: {email_data['priority']}
Subject: {email_data['subject']}
Content: {email_data['snippet']}

Generate a professional, concise response that:
1. Acknowledges the email's purpose
2. Provides appropriate level of urgency
3. Maintains professional tone
4. Is specific to the email's category"""

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                system=self.system_prompt
            )
            return response['response'].strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_default_response(email_data['category'])
    
    def _parse_ollama_response(self, response: str) -> Dict[str, Any]:
        """Parse Ollama's response into structured data."""
        try:
            # Extract JSON from response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # If no JSON found, parse the response manually
            lines = response.split('\n')
            analysis = {
                'category': 'general',
                'priority': 0,
                'requires_attention': False,
                'intent': 'unknown',
                'suggested_response': 'Thank you for your email.'
            }
            
            for line in lines:
                if 'category:' in line.lower():
                    analysis['category'] = line.split(':')[1].strip().lower()
                elif 'priority:' in line.lower():
                    try:
                        analysis['priority'] = int(line.split(':')[1].strip())
                    except:
                        pass
                elif 'requires_attention:' in line.lower():
                    analysis['requires_attention'] = 'true' in line.lower()
                elif 'intent:' in line.lower():
                    analysis['intent'] = line.split(':')[1].strip()
                elif 'suggested_response:' in line.lower():
                    analysis['suggested_response'] = line.split(':')[1].strip()
            
            return analysis
        except Exception as e:
            print(f"Error parsing Ollama response: {e}")
            return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when Ollama fails."""
        return {
            'category': 'general',
            'priority': 0,
            'requires_attention': False,
            'intent': 'unknown',
            'suggested_response': 'Thank you for your email.'
        }
    
    def _get_default_response(self, category: str) -> str:
        """Return default response when Ollama fails."""
        responses = {
            'urgent': "I understand this is urgent. I will prioritize your request and respond as soon as possible.",
            'meeting': "Thank you for the meeting invitation. I will review the details and respond accordingly.",
            'inquiry': "Thank you for your inquiry. I will look into this matter and provide you with a detailed response.",
            'follow_up': "Thank you for your follow-up. I will address this matter promptly.",
            'general': "Thank you for your email. I will get back to you soon."
        }
        return responses.get(category, responses['general']) 