import numpy as np

from mesa import Agent

_UNINFECTED = 0
_SICK = 1
_RECOVERED = 2
_DEAD = 3


class Individual(Agent):
    """
    Individual.
    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
        speed,
        velocity,
        moving=False,
        status=0,
        recovered=False,
        dead=False,
        transmission_probability=0.2,
        recovery_probability=0.6,
        transmission_distance=1.0,
    ):

        """
        Create a new Individual agent.

        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            speed: Distance to move per step.

            status

        uninfected = 0
        sick = 1
        recovered = 2
        dead = 3

        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.moving = moving
        self.status = status
        self.transmission_probability = transmission_probability
        self.recovery_probability = recovery_probability
        self.transmission_distance = transmission_distance

    @property
    def sick(self):
        return self.status == _SICK

    @property
    def recovered(self):
        return self.status == _RECOVERED

    @property
    def dead(self):
        return self.status == _DEAD

    @property
    def uninfected(self):
        return self.status == _UNINFECTED

    def step(self):
        """
        """

        # if you are not dead or recovered.
        if (not self.recovered) and (not self.dead):

            # find and transmit with neighbors

            neighbors = self.model.space.get_neighbors(
                self.pos, self.transmission_distance, False
            )
            for neighbor in neighbors:
                # if you or neighbor is sick, infect.

                if (self.sick) or (neighbor.sick):
                    transmit = np.random.random_sample() < self.transmission_probability
                    if transmit:
                        self.status = _SICK
                        neighbor.status = _SICK

        # if you are sick, potentially recover or die.
        if self.sick:
            recover = np.random.random_sample() < self.recovery_probability
            if recover:
                self.status = _RECOVERED
            else:
                self.status = _DEAD
                self.moving = False

        # move if you are moving (move randomly)
        if self.moving:
            velocity = np.random.random(2) * 2 - 1
            self.velocity /= np.linalg.norm(velocity)
            new_pos = self.pos + self.velocity * self.speed
            self.model.space.move_agent(self, new_pos)
