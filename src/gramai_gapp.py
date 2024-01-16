# Import the libraries
import os
import sys
from urllib.parse import quote

import requests
from dash import Dash, Input, Output, State, dcc, html

# Define the carousel text and colors
carouselText = [
    {"text": "Grammer", "color": "red"},
    {"text": "Gramar", "color": "orange"},
    {"text": "Grammar", "color": "green"},
    {"text": "with GramAI", "color": "violet"},
]

length = 0
dp = 0

# Create the app
app = Dash(__name__, update_title=None)

# Define the layout
app.layout = html.Div(
    [
        html.H1("GramAI", style={"font-size": "40px", "text-align": "center"}),
        dcc.Textarea(
            id="query-box",
            value="",
            placeholder="He have a car",
            style={"font-size": "20px", "width": "55%", "margin-top": "60px", "resize": "none"},
            maxLength=200,
        ),
        # dcc.Textarea(id="output", style={"font-size": "20px", "width": "55%", "margin-top": "20px", "resize":"none"}, readOnly=True),
        dcc.Loading(
            id="loading-2",
            type="circle",
            style={"margin-left": "-40%"},
            children=html.Div(
                id="output", style={"font-size": "20px", "width": "55%", "margin-top": "20px", "whiteSpace": "pre-line"}
            ),
        ),
        html.Button(
            "Correct", id="update-button", style={"font-size": "20px", "width": "10%", "margin-top": "20px"}
        ),  # Add the button element
        html.Div(id="logo", style={"background-image": f"url({app.get_asset_url('dtu.png')})"}),
        # html.Div(id="background", style={"background-image": f"url({app.get_asset_url('parrot.jpeg')})"}),
        html.Div(
            [
                html.Span(
                    children="I want to learn",
                    style={"font-size": "42px", "font-family": "'Darker Grotesque', sans-serif"},
                ),
                html.Span(id="index", style={"display": "none"}, children=0),
                html.Span(
                    id="feature-text",
                    style={"font-size": "42px", "font-family": "'Darker Grotesque', sans-serif"},
                    children="",
                ),
                # A timer to trigger the carousel callback every 200 miliseconds
                dcc.Interval(id="timer", interval=200, n_intervals=0),
                html.Span(id="input-cursor"),
            ],
            id="typing-container",
        ),
    ]
)


# Define the callback function
@app.callback(
    Output("output", "children"),
    Input("update-button", "n_clicks"),
    # Input("query-bar", "value")
    State("query-box", "value"),  # Use the input element as a state
)
def display_output(n_clicks, value):
    if value is None:
        return "No input"
    else:
        response = requests.post("https://gramai-app-h2yv3342wq-ew.a.run.app/text/?input_sentence=" + quote(value))
        return response.json()["corrected"]


@app.callback(
    # The output is the feature text div and the index div
    [Output("feature-text", "children"), Output("index", "children")],
    # The input is the timer component
    Input("timer", "n_intervals"),
    State("index", "children"),
)
def carousel(n, i):
    global length
    global dp
    text = carouselText[i]["text"]
    color = carouselText[i]["color"]
    if dp == 0:
        # Get the current text and color from the carousel list
        partial = text[0 : abs(length)]
        length += 1
        # Create a span element with the text and color
        span = html.Span(partial, style={"color": color})
        if length == len(text):
            # Reverse the order of indexing letters
            length *= -1
            dp = 1
        if length == 0:
            # Increment i to go to the next word
            i = (i + 1) % len(carouselText)
    elif dp < 4:
        span = html.Span(text, style={"color": color})
        # Add a delay point
        dp += 1
        if dp == 4:
            dp = 0
    # Return the span element and the updated index
    return span, i


# Run the app
if __name__ == "__main__":
    if len(sys.argv) > 1:
        app.run(debug=True, host=os.getenv("HOST", sys.argv[1]), port=os.getenv("PORT", sys.argv[2]))
    else:
        app.run(debug=True)
