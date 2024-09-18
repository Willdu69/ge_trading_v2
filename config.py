# config.py

# File path for the input data
DATA_FILE_PATH = './data/BTC-6h-1000wks-data.csv'

# GE configuration
POPULATION_SIZE = 100
GENERATIONS = 50
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.85
ELITISM = True  # Keep the best individuals
ELITISM_CRITERIA = 10  # percentage of the population to keep

# Grammar parameters
TECHNICAL_INDICATORS = ['SMA', 'EMA', 'RSI', 'BBANDS', 'ATR']
INDICATOR_PERIODS = [10, 20, 50]  # Periods to be used with indicators

# Backtesting parameters
INITIAL_CASH = 100000
COMMISSION = 0.002  # Commission rate for trades

NUM_THREADS = 60
