from abc import ABC, abstractmethod

class UserInteraction(ABC):
    def __init__(self, user_id):
        self.user_id = user_id
        # Each interaction is tied to a specific user_id

    @abstractmethod
    def handle(self):
        pass
# Abstract class for all user interactions

class FeedbackComment(UserInteraction):
    def __init__(self, user_id, comment_text):
        super().__init__(user_id)
        self.comment_text = comment_text

    def handle(self):
        return f"User {self.user_id} commented: {self.comment_text}"
# Calls parent constructor, stores comment content

class Rating(UserInteraction):
    def __init__(self, user_id, rating_value):
        super().__init__(user_id)
        self.rating_value = rating_value

    def handle(self):
        return f"User {self.user_id} rated this recipe {self.rating_value}/5"

class AbuseReport(UserInteraction):
    def __init__(self, user_id, reason):
        super().__init__(user_id)
        self.reason = reason

    def handle(self):
        return f"User {self.user_id} reported recipe for: {self.reason}"
    
class InteractionHandler:
    def __init__(self, interactions: list[UserInteraction]):
        self.interactions = interactions

    def process_all(self):
        return [i.handle() for i in self.interactions]
# Aggregates multiple interactions and processes them
# Stores interactions in a unified list
# Calls handle() on each interaction