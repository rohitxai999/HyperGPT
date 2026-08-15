from typing import List, Dict, Any


class ResponseSynthesizer:
    """
    Combines outputs from multiple HyperGPT agents
    into one unified response.
    """

    def synthesize(
        self,
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        agents_used = [
            response.get(
                "agent",
                "Unknown Agent",
            )
            for response in responses
        ]

        final_parts = []

        for response in responses:

            agent = response.get(
                "agent",
                "Unknown Agent",
            )

            # Coding agent
            if response.get("generated_code"):

                code = response["generated_code"]

                explanation = response.get(
                    "explanation",
                    "",
                )

                text = (
                    f"[{agent}]\n\n"
                    f"```python\n"
                    f"{code.strip()}\n"
                    f"```"
                )

                if explanation:
                    text += (
                        f"\n\nExplanation:\n"
                        f"{explanation}"
                    )

                final_parts.append(text)

                continue

            # Normal response
            if response.get("response"):

                final_parts.append(
                    f"[{agent}]\n\n"
                    f"{response['response']}"
                )

                continue

            # Facts
            if response.get("facts"):

                facts = response["facts"]

                final_parts.append(
                    f"[{agent}]\n\n"
                    + "\n".join(
                        f"- {fact}"
                        for fact in facts
                    )
                )

                continue

            # Document
            if response.get("document"):

                final_parts.append(
                    f"[{agent}]\n\n"
                    f"{response['document']}"
                )

                continue

            # Generic fallback
            final_parts.append(
                f"[{agent}]\n\n"
                f"{response}"
            )

        final_response = "\n\n".join(
            final_parts
        )

        return {
            "status": "success",
            "agents_used": agents_used,
            "responses": responses,
            "final_response": final_response,
        }
