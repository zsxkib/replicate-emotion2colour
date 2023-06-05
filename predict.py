# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
from pathlib import Path as PathlibPath
from typing import Dict, List, Union
from transformers import pipeline
from PIL import Image, ImageDraw
import numpy as np


class Predictor(BasePredictor):
    def setup(self):
        """Initialize the model and other necessary variables.

        The method sets up a transformer pipeline and a dictionary mapping emotions
        to specific color codes. It also creates an output directory.

        No parameters are required.

        Returns
        -------
        None
        """

        self.text_to_emotions_model = pipeline(
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=2,
        )
        self.emotions_colors = {
            "joy": "#FFFF00",  # yellow
            "surprise": "#FFA500",  # orange
            "neutral": "#FFF0DB",  # beige
            "anger": "#FF0000",  # red
            "sadness": "#0000FF",  # blue
            "disgust": "#008000",  # green
            "fear": "#800080",  # purple
        }
        self.output_path_str = "./outputs"
        PathlibPath(self.output_path_str).mkdir(parents=True, exist_ok=True)

    def _create_gradient(
        self,
        top_color: str,
        bottom_color: str,
        percentage_transition_point: float,
        steepness: float,
        width: int = 256,
        height: int = 256,
    ) -> Image:
        """Creates a gradient image based on top and bottom colors.

        Parameters
        ----------
        top_color : str
            The color at the top of the gradient (RGB hex code).
        bottom_color : str
            The color at the bottom of the gradient (RGB hex code).
        percentage_transition_point : float
            The point at which the transition should start.
        steepness : float
            Controls the abruptness of the color transition.
        width : int, optional
            The width of the gradient image.
        height : int, optional
            The height of the gradient image.

        Returns
        -------
        Image
            An image object with the desired gradient.
        """

        transition_height = round(percentage_transition_point * height)
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)
        for i in range(height):
            ratio = 1 / (1 + np.exp(-steepness * (i - transition_height) / height))
            r = round((1 - ratio) * int(top_color[1:3], 16) + ratio * int(bottom_color[1:3], 16))
            g = round((1 - ratio) * int(top_color[3:5], 16) + ratio * int(bottom_color[3:5], 16))
            b = round((1 - ratio) * int(top_color[5:7], 16) + ratio * int(bottom_color[5:7], 16))
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        return image

    def emotions_to_colorgrad(
        self,
        emotions: List[Dict[str, Union[str, float]]],
        steepness: float = 10,
        width: int = 256,
        height: int = 256,
    ) -> Image:
        """Generates a gradient image based on input emotions.

        Parameters
        ----------
        emotions : List[Dict[str, Union[str, float]]]
            The emotions to be used for creating the gradient.
        steepness : float, optional
            Controls the abruptness of the color transition.
        width : int, optional
            The width of the gradient image.
        height : int, optional
            The height of the gradient image.

        Returns
        -------
        Image
            An image object with the desired gradient.
        """

        sorted_emotions = sorted(emotions, key=lambda x: x["score"], reverse=True)
        top_emotion = sorted_emotions[0]["label"]
        bottom_emotion = sorted_emotions[1]["label"]
        score_top_emotion = sorted_emotions[0]["score"]
        color_top_emotion = self.emotions_colors.get(top_emotion)
        color_bottom_emotion = self.emotions_colors.get(bottom_emotion)
        if not color_top_emotion or not color_bottom_emotion:
            raise ValueError("One or more emotion colors not found in emotions_colors dictionary")
        image = self._create_gradient(
            color_top_emotion,
            color_bottom_emotion,
            score_top_emotion,
            steepness,
            width,
            height,
        )
        print(f"{'='*80}")
        print(f"{sorted_emotions=}")
        print(f"({color_top_emotion}) {top_emotion=}")
        print(f"({color_bottom_emotion}) {bottom_emotion=}")
        print(f"{'='*80}")
        return image

    def predict(
        self,
        text: str = Input(
            description="A sentence which we'd like to classify the emotion for to generate a colour (two-tone gradient)"
        ),
    ) -> Path:
        """Predicts the emotions in a given text and returns an image path.

        Parameters
        ----------
        text : str
            The text from which emotions are to be predicted.

        Returns
        -------
        Path
            Path to the generated image representing emotions.
        """

        emotions = self.text_to_emotions_model(text)[0]
        image = self.emotions_to_colorgrad(emotions)
        image_file_path = PathlibPath(self.output_path_str + "/emotion_gradient.png")
        image.save(image_file_path)
        return Path(image_file_path)
