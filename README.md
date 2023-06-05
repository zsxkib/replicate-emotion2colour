# **Unveiling Cog's Emotion Visualization: Paint Your Mood with Color!** 🌈

Imagine transforming a sentence into emotions depicted by colors. This is what our tool achieves. Allow us to walk you through this journey from textual emotions to a radiant world of color gradients. 🎨

## The Mechanics of It All 🤔

Our system utilizes a Python-based Cog Predictor, designed to transform your textual input into a vibrant display of color gradients. The process is simple:
- Your text is received, no matter its content.
- Our model, [`distilroberta-base` by `j-hartmann`](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base), adeptly uncovers the emotional sentiments within your text.
- These detected emotions are then converted into colors, forming a visual representation as intricate as your feelings.

## Translating Emotions into Radiant Gradients 🎨

The model is capable of recognizing a range of emotions: anger 🤬, disgust 🤢, fear 😨, joy 😀, neutral 😐, sadness 😭, and surprise 😲. Each emotion translates to a unique color, creating a comprehensive palette to paint your emotional landscape. The intensity of the detected emotions influences the transition points within the radiant gradient. The more pronounced the emotion, the more it shapes the color scheme.

Interestingly, the location of the transition within the gradient depends on the strength of the top two emotions identified. This means that if one emotion is significantly stronger than the other, the color representing the stronger emotion will dominate a larger portion of the gradient.

## Your Journey from Installation to Visualization 🚀

### Building with Cog 🛠️

Before you start, ensure you have [Cog](https://github.com/replicate/cog) installed. Once that's done, building with Cog is a breeze. 

Just run the following command in your terminal:
```zsh
cog build
```

### Executing a Prediction 🏃‍♀️

For illustration, let's explore how a prediction is executed. With an input like `"I'm so mad, I don't know why"`, we create this eye-catching gradient:
```
cog predict -i text="I'm so mad, i don't know why"
```

The script provides a detailed output:
```zsh
Running prediction...
================================================================================
sorted_emotions=[{'label': 'anger', 'score': 0.6365653872489929}, {'label': 'surprise', 'score': 0.22874169051647186}]
(#FF0000) top_emotion='anger'
(#FFA500) bottom_emotion='surprise'
================================================================================
Written output to output.png
```

<center>
    <img src="https://cdn.discordapp.com/attachments/847959427424452639/1115395222696906862/output.png" alt="Prediction Output" width="600px" />
</center>

As you can see, your part is easy: provide the text and watch the machine learning magic happen!

Once the prediction is complete, you'll find an image titled `output.png` in your directory, reflecting the emotional sentiment of your input text as a radiant gradient.

With this Replicate cog-example, we aim to bridge the gap between machine learning and user-friendly application, providing you with a fun and captivating way to visualize textual emotions as color gradients.
