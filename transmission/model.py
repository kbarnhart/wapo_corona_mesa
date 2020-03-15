"""
"""

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from .individual import Individual, _SICK, _RECOVERED, _UNINFECTED, _DEAD


def analyze_dead(model):
    agent_status = [agent.dead for agent in model.schedule.agents]
    dead = np.mean(agent_status)
    return dead


def analyze_sick(model):
    agent_status = [agent.sick for agent in model.schedule.agents]
    sick = np.mean(agent_status)
    return sick


def analyze_uninfected(model):
    agent_status = [agent.uninfected for agent in model.schedule.agents]
    uninf = np.mean(agent_status)
    return uninf


def analyze_recovered(model):
    agent_status = [agent.recovered for agent in model.schedule.agents]
    recovered = np.mean(agent_status)
    return recovered


class Transmission(Model):
    """
    """

    def __init__(
        self,
        population=100,
        width=500,
        height=500,
        initial_proportion_sick=0.1,
        proportion_moving=0.5,
        speed=1.0,
        transmission_probability=0.2,
        transmission_distance=1.0,
        recovery_probability=0.6,
    ):
        """
        Create a new Transmission model.



Potential things to add
# age as an attribute.
# differential mobility as a function of age.
# time dependence of recovery
# non random walking

                     """
        self.population = population
        self.proportion_moving = proportion_moving
        self.initial_proportion_sick = initial_proportion_sick
        self.speed = speed

        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(
            transmission_probability=transmission_probability,
            recovery_probability=recovery_probability,
            transmission_distance=transmission_distance,
        )

        self.make_agents()
        self.running = True

        self.datacollector = DataCollector(
            model_reporters={
                "uninfected": analyze_uninfected,
                "sick": analyze_sick,
                "recovered": analyze_recovered,
                "dead": analyze_dead,
            }
        )

    def make_agents(self):
        """
        """
        for i in range(self.population):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max

            sick = np.random.random_sample() < self.initial_proportion_sick
            if sick:
                status = _SICK
            else:
                status = _UNINFECTED

            moving = np.random.random_sample() < self.proportion_moving

            pos = np.array((x, y))
            if moving:
                velocity = np.random.random(2) * 2 - 1
            else:
                velocity = 0.0

            indiv = Individual(
                i, self, pos, self.speed, velocity, moving, status, **self.factors
            )

            self.space.place_agent(indiv, pos)
            self.schedule.add(indiv)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()