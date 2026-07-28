class MemoryAnalyzer:

    def analyze(self, message: str):

        score = 0.0
        category = "temporary_information"


        keywords = [
            "my project",
            "remember",
            "i prefer",
            "i use",
            "i am building",
            "my name"
        ]


        for word in keywords:
            if word.lower() in message.lower():
                score += 0.2


        if score >= 0.8:
            category = "important"

        elif score >= 0.4:
            category = "useful"


        return {
            "content": message,
            "importance": min(score,1),
            "category": category
        }