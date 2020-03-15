from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from .SimpleContinuousModule import SimpleCanvas

from .individual import Individual
from .model import Transmission


def transmission_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if agent.sick:
        portrayal["Color"] = "brown"
    elif agent.recovered:
        portrayal["Color"] = "purple"
    elif agent.dead:
        portrayal["Color"] = "grey"
    else:  # uninfected.
        portrayal["Color"] = "green"



    if agent.moving:
        portrayal["Filled"] = "true"
        portrayal["Shape"] = "circle"
        portrayal["r"] = 4
    else:
        portrayal["Filled"] = "false"
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.015
        portrayal["h"] = 0.015
    portrayal["Layer"] = 0


    return portrayal


canvas_element = SimpleCanvas(transmission_portrayal, 500, 500)
chart_element = ChartModule(
    [
        {"Label": "uninfected", "Color": "green"},
        {"Label": "sick", "Color": "brown"},
        {"Label": "recovered", "Color": "purple"},
        {"Label": "dead", "Color": "gray"},
    ],
    data_collector_name="datacollector",
)

model_params = {
    "population": UserSettableParameter(
        "slider", "population", value=100, min_value=10, max_value=1000, step=10
    ),
    "initial_proportion_sick": UserSettableParameter(
        "slider",
        "initial_proportion_sick",
        value=0.1,
        min_value=0,
        max_value=1,
        step=0.01,
    ),
    "proportion_moving": UserSettableParameter(
        "slider", "proportion_moving", value=0.2, min_value=0, max_value=1, step=0.1
    ),
    "speed": UserSettableParameter(
        "slider", "speed", value=1, min_value=0, max_value=10, step=1
    ),
    "transmission_probability": UserSettableParameter(
        "slider",
        "transmission_probability",
        value=0.2,
        min_value=0,
        max_value=1,
        step=0.01,
    ),
    "transmission_distance": UserSettableParameter(
        "slider", "transmission_distance", value=2, min_value=0, max_value=10, step=0.5
    ),
    "recovery_probability": UserSettableParameter(
        "slider", "recovery_probability", value=0.9, min_value=0, max_value=1, step=0.01
    ),
}

server = ModularServer(
    Transmission, [canvas_element, chart_element], "Transmission", model_params
)
server.port = 8521
