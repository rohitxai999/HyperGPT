from app.memory.memory_analyzer import MemoryAnalyzer


class MemoryService:

    def __init__(self, store):
        self.analyzer = MemoryAnalyzer()
        self.store = store


    def process_memory(self,message):

        result = self.analyzer.analyze(message)


        if result["importance"] >= 0.5:

            self.store.save(
                result["content"],
                result["category"]
            )

            return "Memory saved"


        return "Memory ignored"