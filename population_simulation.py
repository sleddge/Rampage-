"""Population Simulation
-----------------------

Ce script simule l'evolution d'une petite population humaine en fonction de la
nourriture disponible. Les survivants tirent des leçons des annees precedentes
et tentent d'adapter leur comportement (mise en reserve de nourriture) lorsque
des famines surviennent. A la fin de la simulation, une interface graphique
simple affiche l'historique de la population et des "echecs" (famine ou morts
de vieillesse).
"""

import argparse
import random
from dataclasses import dataclass, field

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib may be absent during tests
    plt = None

@dataclass
class Human:
    age: int = 0

    def age_one_year(self):
        self.age += 1


@dataclass
class GenerationFailure:
    """Stocke les echecs d'une annee."""
    year: int
    starvations: int
    deaths_old_age: int

@dataclass
class Simulation:
    food_per_year: int = 400
    consumption_per_human: int = 100
    birth_food_threshold: int = 200
    max_age: int = 80
    years: int = 100
    population: list = field(default_factory=lambda: [Human(age=20), Human(age=20)])
    memory: list = field(default_factory=list)
    reserved_food: int = 0
    population_history: list = field(default_factory=list)
    show_gui: bool = True

    def run(self):
        for year in range(1, self.years + 1):
            food_available = self.food_per_year + self.reserved_food
            starvations = 0
            survivors = []
            for human in self.population:
                if food_available >= self.consumption_per_human:
                    food_available -= self.consumption_per_human
                    survivors.append(human)
                else:
                    starvations += 1

            self.population = survivors

            adults = [h for h in self.population if h.age >= 18]
            if len(adults) >= 2 and food_available >= self.birth_food_threshold:
                self.population.append(Human(age=0))
                food_available -= self.birth_food_threshold

            deaths_old_age = 0
            next_generation = []
            for human in self.population:
                human.age_one_year()
                death_probability = 0.0
                if human.age > self.max_age:
                    death_probability = min(1.0, 0.05 * (human.age - self.max_age))
                if random.random() >= death_probability:
                    next_generation.append(human)
                else:
                    deaths_old_age += 1
            self.population = next_generation

            self.memory.append(
                GenerationFailure(year=year, starvations=starvations, deaths_old_age=deaths_old_age)
            )
            self.population_history.append(len(self.population))

            if starvations > 0:
                self.reserved_food += 50
            else:
                self.reserved_food = max(0, self.reserved_food - 10)

            print(
                f"Year {year}: population {len(self.population)} "
                f"(starvations: {starvations}, age deaths: {deaths_old_age})"
            )
            if not self.population:
                print("All humans have died.")
                break

        if self.show_gui:
            self.display_results()

    def display_results(self):
        """Affiche l'evolution de la population et les echecs."""
        if plt is None:
            print("Matplotlib n'est pas disponible, impossible d'afficher la fenetre graphique.")
            return

        years = [f.year for f in self.memory]
        populations = self.population_history
        starvations = [f.starvations for f in self.memory]
        old_deaths = [f.deaths_old_age for f in self.memory]

        fig, ax1 = plt.subplots()
        ax1.plot(years, populations, label="Population", color="blue")
        ax1.set_xlabel("Annee")
        ax1.set_ylabel("Population")
        ax1.legend(loc="upper left")

        ax2 = ax1.twinx()
        ax2.bar(years, starvations, alpha=0.4, color="red", label="Famine")
        ax2.bar(years, old_deaths, alpha=0.4, color="gray", bottom=starvations, label="Vieux")
        ax2.set_ylabel("Echecs")
        ax2.legend(loc="upper right")

        plt.title("Evolution de la population")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulation de population")
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Execute la simulation sans interface graphique",
    )
    args = parser.parse_args()

    sim = Simulation(show_gui=not args.no_gui)
    sim.run()
