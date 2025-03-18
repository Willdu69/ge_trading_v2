import random
from grammar import get_grammar, generate_rule
import numpy as np
from tqdm import tqdm
from config import POPULATION_SIZE, GENERATIONS, MUTATION_RATE, CROSSOVER_RATE, ELITISM, ELITISM_CRITERIA, TECHNICAL_INDICATORS

class Individual:
    def __init__(self, rule):
        self.rule = rule
        self.fitness = None  # To be set during evaluation

class GrammaticalEvolution:
    def __init__(self):
        self.population = []

    def initialize_population(self):
        grammar = get_grammar()
        self.population = [Individual(generate_rule(grammar)) for _ in range(POPULATION_SIZE)]

    def evaluate_fitness(self, individual):
        from backtester import run_backtest
        individual.fitness = run_backtest(individual.rule)

    def select_parents(self):
        return random.sample(self.population, 2)

    def label_rule_components(self, rule):
        """
        Label each component (indicator, operator, value) in the rule.
        Example: 
        "if EMA(50) <= closing_price" will become:
        [("indicator", "EMA(50)"), ("operator", "<="), ("value", "closing_price")]
        """
        components = []
        tokens = rule.split()
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if any(indicator in token for indicator in TECHNICAL_INDICATORS):
                components.append(("indicator", token))
            elif token in [">", "<", ">=", "<="]:
                components.append(("operator", token))
            elif token in ["closing_price", "open_price", "high_price", "low_price", "volume"]:
                components.append(("value", token))
            elif token in ["and", "or"]:
                components.append(("logic", token))
            elif token in ["buy", "sell"]:
                components.append(("action", token))
            i += 1
        
        return components

    def validate_rule_structure(self, components):
        """
        Validate that the rule follows the structure:
        <indicator> <operator> <value> [and/or <indicator> <operator> <value>] then <action>
        """
        if not components:
            return False
        
        valid_structure = [("indicator",), ("operator",), ("value",)]
        
        i = 0
        while i < len(components):
            for part in valid_structure:
                if i >= len(components) or components[i][0] != part[0]:
                    return False
                i += 1
            
            if i < len(components) and components[i][0] == "logic":
                i += 1  
        
        if i < len(components) and components[i][0] == "action":
            return True
        return False

    def crossover(self, parent1, parent2):
        """
        Improved crossover method that follows the grammar structure:
        <indicator> <operator> <value> and <indicator> <operator> <value> then <action>
        """
        if random.random() < CROSSOVER_RATE:
            components1 = self.label_rule_components(parent1.rule)
            components2 = self.label_rule_components(parent2.rule)

            if not self.validate_rule_structure(components1) or not self.validate_rule_structure(components2):
                return parent1.rule  # Return parent rule if structure is invalid

            crossover_point1 = random.randint(1, len(components1) - 1) 
            crossover_point2 = random.randint(1, len(components2) - 1)
            child_components = components1[:crossover_point1] + components2[crossover_point2:]

            if self.validate_rule_structure(child_components):
                return ' '.join([component[1] for component in child_components])
            else:
                return parent1.rule  # Fall back to parent rule if the new structure is invalid

        return parent1.rule



    def mutate(self, rule):
        if random.random() < MUTATION_RATE:
            grammar = get_grammar()
            rule = generate_rule(grammar)
        return rule

    def evolve(self):
        try:
            self.initialize_population()

            for generation in tqdm(range(GENERATIONS), desc="Generations"):
                with tqdm(total=POPULATION_SIZE, desc=f"Evaluating Gen {generation + 1}", leave=False) as progress_bar:
                    for individual in self.population:
                        # print(individual.rule)
                        try:
                            self.evaluate_fitness(individual)
                        except Exception as exc:
                            print(f"An error occurred while evaluating {individual.rule}: {exc}")
                        progress_bar.update(1) 

                self.population.sort(key=lambda ind: ind.fitness, reverse=True)

                new_population = []

                if ELITISM:
                    new_population.append(self.population[-1])  # Keep the best individual

                while len(new_population) < POPULATION_SIZE:
                    parent1, parent2 = self.select_parents()
                    child_rule = self.crossover(parent1, parent2)
                    child_rule = self.mutate(child_rule)
                    new_population.append(Individual(child_rule))

                self.population = new_population

                print(f"Generation {generation + 1}, Best Rule: {self.population[0].rule}, Fitness: {self.population[0].fitness}")

        except KeyboardInterrupt:
            print("\nProcess interrupted! Exiting gracefully...")
