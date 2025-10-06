"""
AI-powered analysis for fake news detection
"""


import json
from typing import List, Dict
from openai import OpenAI


class NewsAnalyzer:
    """Analyze news claims using OpenAI's API"""

    def __init__(self, api_key: str, model: str = "gpt-5-nano"):

        self.client = OpenAI(api_key=api_key)
        # If using openrouter api
        # self.client = OpenAI(
        # base_url="https://openrouter.ai/api/v1",
        # api_key=api_key,
        # )

        self.model = model

    def analyze_claim(self, claim: str, search_results: List[Dict[str, str]]) -> Dict:
        """
        Analyze a claim based on search results

        Args:
            claim: The claim to analyze
            search_results: List of search results

        Returns:
            Analysis results including credibility score and explanation
        """
        try:
            # Prepare context from search results
            context = self._prepare_context(search_results)

            # Create analysis prompt
            prompt = self._create_analysis_prompt(claim, context)

            # Get AI analysis

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.8,
            )

            # If using openrouter api
            # response = self.client.chat.completions.create(
            # extra_headers={},
            # extra_body={},
            # model=self.model,
            # messages=[
            #         {"role": "system", "content": self._get_system_prompt()},
            #         {"role": "user", "content": prompt}
            #     ],
            #     max_tokens=1000,
            #     temperature=0.8
            # )

            # Parse response
            analysis_text = response.choices[0].message.content
            return self._parse_analysis(analysis_text)

        except Exception as e:
            print(f"Error during analysis: {e}")
            return {
                'credibility_score': 0,
                'verdict': 'Analysis Failed',
                'explanation': f'Could not complete analysis: {str(e)}',
                'confidence': 'Low'
            }

    def _prepare_context(self, search_results: List[Dict[str, str]]) -> str:
        """Prepare context from search results"""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(
                f"Source {i}: {result['title']}\n"
                f"URL: {result['link']}\n"
                f"Summary: {result['snippet']}\n"
            )
        return "\n".join(context_parts)

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI"""
        return """You are a fact-checking assistant that analyzes news claims for credibility.
        Your task is to evaluate claims based on available evidence and provide a structured analysis.
        Be objective, thorough, and base your assessment on the information provided.
        Always respond with a JSON object containing the analysis."""

    def _create_analysis_prompt(self, claim: str, context: str) -> str:
        """Create the analysis prompt"""
        return f"""Analyze the following claim for credibility based on the search results provided.

CLAIM: {claim}

SEARCH RESULTS:
{context}

Please provide your analysis as a JSON object with the following structure:
{{
    "credibility_score": <integer from 0-10>,
    "verdict": "<Likely True/Likely False/Uncertain/Mixed Evidence>",
    "confidence": "<High/Medium/Low>",
    "explanation": "<detailed explanation of your analysis>",
    "key_findings": ["<finding 1>", "<finding 2>", ...],
    "red_flags": ["<red flag 1>", "<red flag 2>", ...],
    "supporting_evidence": ["<evidence 1>", "<evidence 2>", ...]
}}

Consider:
- Consistency across sources
- Source credibility
- Presence of factual information vs opinion
- Any obvious signs of misinformation
- Date and relevance of information"""

    def _parse_analysis(self, analysis_text: str) -> Dict:
        """Parse the AI's analysis response"""
        try:
            # Try to extract JSON from the response
            if "```json" in analysis_text:
                json_start = analysis_text.find("```json") + 7
                json_end = analysis_text.find("```", json_start)
                json_str = analysis_text[json_start:json_end].strip()
            elif "{" in analysis_text and "}" in analysis_text:
                json_start = analysis_text.find("{")
                json_end = analysis_text.rfind("}") + 1
                json_str = analysis_text[json_start:json_end]
            else:
                json_str = analysis_text

            # Parse JSON
            analysis = json.loads(json_str)

            # Validate and set defaults
            return self._validate_analysis(analysis)

        except json.JSONDecodeError:
            # Fallback for non-JSON responses
            return {
                'credibility_score': 5,
                'verdict': 'Uncertain',
                'explanation': analysis_text,
                'confidence': 'Medium',
                'key_findings': [],
                'red_flags': [],
                'supporting_evidence': []
            }

    def _validate_analysis(self, analysis: Dict) -> Dict:
        """Validate and ensure all required fields are present"""
        defaults = {
            'credibility_score': 5,
            'verdict': 'Uncertain',
            'confidence': 'Medium',
            'explanation': 'Analysis could not be completed',
            'key_findings': [],
            'red_flags': [],
            'supporting_evidence': []
        }

        # Merge with defaults
        for key, default_value in defaults.items():
            if key not in analysis:
                analysis[key] = default_value

        # Ensure credibility score is within range
        score = analysis.get('credibility_score', 5)
        if isinstance(score, str):
            try:
                score = int(score)
            except ValueError:
                score = 5
        analysis['credibility_score'] = max(0, min(10, score))

        return analysis
