from typing import List, Dict, Any


class ResponseSynthesizer:
    """
    Combines outputs from multiple agents into one final response.
    """

    def synthesize(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "status": "success",
            "agents_used": [
                response.get("agent", "Unknown")
                for response in responses
            ],
            "responses": responses
        }