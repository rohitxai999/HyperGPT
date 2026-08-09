import re

from app.tools.registry import registry


class ToolSelector:
    """
    Explainable scored tool-selection engine.
    """

    def __init__(self):
        registry.auto_register()

    def _normalize(self, text: str):
        """
        Normalize user input for matching.
        """

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9+\-*/% ]",
            " ",
            text
        )

        return " ".join(text.split())

    def _score_tool(self, tool, query: str):
        """
        Calculate relevance score for a tool.
        """

        score = 0

        metadata = tool.metadata()

        keywords = metadata.get(
            "keywords",
            []
        )

        description = metadata.get(
            "description",
            ""
        ).lower()

        for keyword in keywords:

            keyword = keyword.lower().strip()

            if not keyword:
                continue

            if keyword in query:

                if " " in keyword:
                    score += 3
                else:
                    score += 1

        description_words = description.split()

        for word in description_words:

            if len(word) > 3 and word in query:
                score += 0.25

        if tool.name == "calculator":

            # Direct mathematical expression
            if re.search(
                r"\d+\s*[+\-*/%]\s*\d+",
                query
            ):
                score += 5

            # Natural-language arithmetic
            natural_math_patterns = [
                r"\d+\s+plus\s+\d+",
                r"\d+\s+minus\s+\d+",
                r"\d+\s+times\s+\d+",
                r"\d+\s+multiplied\s+by\s+\d+",
                r"\d+\s+divided\s+by\s+\d+",
                r"\d+\s+divide\s+by\s+\d+",
            ]

            for pattern in natural_math_patterns:

                if re.search(pattern, query):
                    score += 5
                    break

        return score

    def _build_reasons(self, tool, query: str):
        """
        Explain why a tool received its score.
        """

        reasons = []

        if tool is None:
            return reasons

        metadata = tool.metadata()

        keywords = metadata.get(
            "keywords",
            []
        )

        matched_keywords = []

        for keyword in keywords:

            keyword = keyword.lower().strip()

            if keyword and keyword in query:
                matched_keywords.append(keyword)

        if matched_keywords:
            reasons.append(
                "Matched keywords: "
                + ", ".join(matched_keywords)
            )

        if tool.name == "calculator":

            if re.search(
                r"\d+\s*[+\-*/%]\s*\d+",
                query
            ):
                reasons.append(
                    "Arithmetic expression detected"
                )

            natural_math_patterns = [
                r"\d+\s+plus\s+\d+",
                r"\d+\s+minus\s+\d+",
                r"\d+\s+times\s+\d+",
                r"\d+\s+multiplied\s+by\s+\d+",
                r"\d+\s+divided\s+by\s+\d+",
                r"\d+\s+divide\s+by\s+\d+",
            ]

            if any(
                re.search(pattern, query)
                for pattern in natural_math_patterns
            ):
                reasons.append(
                    "Natural-language arithmetic detected"
                )

        description = metadata.get(
            "description",
            ""
        ).lower()

        description_matches = []

        for word in description.split():

            if len(word) > 3 and word in query:
                description_matches.append(word)

        if description_matches:
            reasons.append(
                "Description terms matched: "
                + ", ".join(
                    sorted(set(description_matches))
                )
            )

        return reasons

    def _confidence(self, score: float):
        """
        Convert a numerical score into a confidence level.
        """

        if score >= 4:
            return "high"

        if score >= 2:
            return "medium"

        if score >= 1:
            return "low"

        return "none"

    def select_with_explanation(self, user_input: str):
        """
        Select the best tool and return an explainable result.
        """

        query = self._normalize(user_input)

        candidates = []

        for tool in registry.tools.values():

            score = self._score_tool(
                tool,
                query
            )

            candidates.append({
                "tool": tool,
                "score": score
            })

        candidates.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        best = candidates[0] if candidates else None

        if best is None or best["score"] < 1:

            return {
                "selected_tool": None,
                "score": 0,
                "confidence": "none",
                "reasons": [
                    "No registered tool matched the request."
                ],
                "alternatives": []
            }

        selected_tool = best["tool"]
        selected_score = best["score"]

        alternatives = []

        for candidate in candidates[1:]:

            # Only show meaningful alternatives.
            if candidate["score"] >= 2:

                alternatives.append({
                    "tool": candidate["tool"].name,
                    "score": candidate["score"]
                })

        return {
            "selected_tool": selected_tool.name,
            "score": selected_score,
            "confidence": self._confidence(
                selected_score
            ),
            "reasons": self._build_reasons(
                selected_tool,
                query
            ),
            "alternatives": alternatives
        }

    def select(self, user_input: str):
        """
        Backward-compatible tool selection.

        Returns the actual tool instance.
        """

        result = self.select_with_explanation(
            user_input
        )

        selected_name = result["selected_tool"]

        if selected_name is None:
            return None

        return registry.get(selected_name)