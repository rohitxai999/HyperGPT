class PersonalizationEngine:
    """
    Stores user preferences used during response generation.
    """

    DEFAULTS = {
        "response_length": "medium",
        "coding_style": "clean",
        "ui_style": "modern",
        "framework": "FastAPI",
    }

    def __init__(self):
        self.preferences = self.DEFAULTS.copy()

    def update(self, key, value):
        self.preferences[key] = value

    def get(self, key, default=None):
        return self.preferences.get(key, default)

    def all_preferences(self):
        return self.preferences