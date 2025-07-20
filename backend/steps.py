from abc import ABC, abstractmethod

class StepBase(ABC):
    def __init__(self, step_number, instruction, img_path=None):
        self.step_number = step_number
        self.instruction = instruction
        self.img_path = img_path

    @abstractmethod
    def render(self) -> str:
        pass
# Base class for steps.
# Each class must implement a render() method which will return a HTML string.
# This is the polymorphic parent class of the other step classes below.

class TextStep(StepBase):
    def render(self) -> str:
        return f"<p>{self.step_number}. {self.instruction}</p>"
# For steps that only include text instructions and no images.

class ImageStep(StepBase):
    def render(self) -> str:
        return (
            f"<div>"
            f"<p>{self.step_number}. {self.instruction}</p>"
            f"<img src='{self.img_path}' alt='Step image' style='width:100%; border-radius:6px;' />"
            f"</div>"
        )
# For steps that include images.
# Renders the instruction followed by an embedded image.
# The image will stretch to fit the container's width.