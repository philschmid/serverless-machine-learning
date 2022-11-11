import gradio as gr
from transformers import pipeline

clf = pipeline("sentiment-analysis", model="model/")


def sentiment(payload):
    prediction = clf(payload, return_all_scores=True)

    # convert list to dict
    result = {}
    for pred in prediction[0]:
        result[pred["label"]] = pred["score"]
    return result


demo = gr.Interface(
    fn=sentiment,
    inputs=gr.Textbox(placeholder="Enter a positive or negative sentence here..."),
    outputs="label",
    interpretation="default",
    examples=[["I Love Serverless Machine Learning"],["Running Gradio on AWS Lambda is amazing"]],
    allow_flagging="never",
    analytics_enabled=False
)

demo.launch(
    server_port=8080,
    # server_name="0.0.0.0",
    enable_queue=False,
)
