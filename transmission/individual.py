import numpy as np

from mesa import Agent

_UNINFECTED = 0
_SICK = 1
_QUARANTINED = 2
_RECOVERED = 3
_DEAD = 4


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
        time_until_symptomatic=3,
        transmission_probability=0.2,
        recovery_probability=0.6,
        transmission_distance=1.0,
        death_probability=0.02,
        quarantine_probability = 0.5
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
        self.death_probability = death_probability
        self.transmission_distance = transmission_distance
        self.time_sick = 0
        self.time_until_symptomatic = time_until_symptomatic
        self.quarantine_probability = quarantine_probability
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

    @property
    def quarantined(self):
        return self.status == _QUARANTINED


    def step(self):
        """
        """

        # if you are sick or uninfected, then see who your friends are.
        if self.sick:

            # find and transmit with neighbors
            neighbors = self.model.space.get_neighbors(
                self.pos, self.transmission_distance, False
            )
            for neighbor in neighbors:
                # if you or neighbor is uninfected.
                if neighbor.uninfected:
                    transmit = np.random.random_sample() < self.transmission_probability
                    if transmit:
                        neighbor.status = _SICK

        # if you are sick, potentially recover or die. If you do neither, then
        # quarantine yourself after you become symptomatic.
        if self.sick or self.quarantined:

            recover = np.random.random_sample() < self.recovery_probability
            death = np.random.random_sample() < self.death_probability

            if recover and death: # if both, none.
                death = False
                recover = False

            if recover:
                self.status = _RECOVERED


            if death:
                self.status = _DEAD
                self.moving = False

            if (not self.recovered) and (self.time_sick>self.time_until_symptomatic):
                quarantined = np.random.random_sample() < self.quarantine_probability
                if quarantined:
                    self.status = _QUARANTINED

            self.time_sick += 1

        # move if you were assigned to move and are not quarantined (move randomly)
        if self.moving and (not self.quarantined):
            velocity = np.random.random(2) * 2 - 1
            self.velocity /= np.linalg.norm(velocity)
            new_pos = self.pos + self.velocity * self.speed
            self.model.space.move_agent(self, new_pos)
