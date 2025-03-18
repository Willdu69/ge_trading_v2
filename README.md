# Algorithmic Trading with Genetic Evolution

This project implements a trading strategy optimization using a genetic algorithm. It leverages financial technical indicators and a grammatical evolution approach to generate trading rules.

## Scientific Concepts

### 1. Technical Indicators

The core of this project relies on technical indicators. These are calculations based on historical price and volume data used to predict future market movements. The following indicators are used:

* **Simple Moving Average (SMA)**: A basic indicator that smooths price data by calculating the average price over a specified period. It helps to identify trends.
* **Exponential Moving Average (EMA)**: Similar to SMA, but gives more weight to recent prices, making it more responsive to new information.
* **Relative Strength Index (RSI)**: A momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions.
* **Average True Range (ATR)**: A volatility indicator that measures price volatility.
* **Bollinger Bands (BBANDS)**: A volatility indicator defined by a set of trendlines typically plotted two standard deviations (positively and negatively) away from a simple moving average (SMA)[cite: 8].

### 2. Grammatical Evolution

Grammatical evolution (GE) is an evolutionary algorithm that can generate computer programs. It uses a grammar to define the search space, allowing the algorithm to explore only syntactically correct programs[cite: 1, 5, 6].

* **Grammar**: In this project, a specific grammar is defined to generate trading rules. The grammar specifies the structure of a rule, including conditions, actions, and logical operators. This ensures that only valid trading rules are created[cite: 5, 6].
* **Genetic Algorithm**: GE employs a genetic algorithm to evolve populations of trading rules. The key steps include:
    * **Initialization**: A population of random trading rules is created[cite: 1].
    * **Fitness Evaluation**: Each rule's performance is evaluated using backtesting, and a fitness score (e.g., return) is assigned[cite: 1, 8, 9, 10].
    * **Selection**: The better-performing rules are more likely to be selected as parents for the next generation[cite: 1].
    * **Crossover**: Genetic material from two parent rules is combined to create new offspring rules[cite: 1].
    * **Mutation**: Random changes are introduced into the rules to maintain diversity in the population[cite: 1].
    * **Evolution**: The process repeats over generations, with the population of rules gradually improving[cite: 1].

### 3. Backtesting

Backtesting is the process of evaluating a trading strategy on historical data. This project uses the `backtesting.py` library to simulate trading with generated rules on historical price data[cite: 1, 8, 9, 10].

* **Strategy Implementation**: The `CustomStrategy` class in `backtester.py` implements the trading logic. It uses the generated rules to determine when to buy or sell[cite: 1, 8].
* **Performance Metrics**: The backtesting process calculates performance metrics such as return, Sharpe ratio, and drawdown to assess the effectiveness of the trading strategies[cite: 10].

## Code Explanation

### `grammar.py`

This file defines the grammar used by the grammatical evolution algorithm. The grammar specifies the valid structure of trading rules. It includes components such as conditions, actions, logical operators, and technical indicators[cite: 5, 6].

### `ge_engine.py`

This file implements the grammatical evolution algorithm. It includes the logic for:

* Initializing the population of trading rules[cite: 1].
* Evaluating the fitness of individual rules using backtesting[cite: 1, 8, 9, 10].
* Selecting parents for crossover[cite: 1].
* Performing crossover and mutation operations to create new rules[cite: 1].

### `backtester.py`

This file sets up the backtesting environment. It reads historical data, defines the custom trading strategy, and uses the `backtesting.py` library to evaluate the performance of trading rules[cite: 1, 8, 9, 10].

### `config.py`

This file contains configuration parameters for the project, such as data file paths, genetic algorithm settings (e.g., population size, mutation rate), and backtesting parameters[cite: 4, 11].

### `main.py`

This is the main entry point of the program, which initializes and runs the grammatical evolution process[cite: 3, 7].

## How Scientific Concepts Are Used

* Technical indicators are used to provide input features for the trading rules. The code calculates these indicators and makes them available to the strategy logic[cite: 8].
* Grammatical evolution uses a predefined grammar to generate trading rules, ensuring that the rules are syntactically correct and follow a logical structure[cite: 5, 6].
* The genetic algorithm optimizes the trading strategies by evolving a population of rules over generations, using fitness evaluation, selection, crossover, and mutation[cite: 1].
* Backtesting is used to evaluate the performance of the generated trading rules on historical data, providing a quantitative measure of their effectiveness[cite: 1, 8, 9, 10].
