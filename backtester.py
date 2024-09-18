# backtester.py

import pandas as pd
import talib
import re
from backtesting import Backtest, Strategy
from config import DATA_FILE_PATH, INITIAL_CASH, COMMISSION, TECHNICAL_INDICATORS, INDICATOR_PERIODS

# Load data
data = pd.read_csv(DATA_FILE_PATH, parse_dates=['datetime'], index_col='datetime')
VALID_VARIABLES = ['closing_price', 'open_price', 'high_price', 'low_price', 'volume']

class CustomStrategy(Strategy):
    rule = None  # This will be set externally for each strategy

    def init(self):
        # Dynamically calculate all indicators based on the defined periods
        self.indicators = {}
        
        for period in INDICATOR_PERIODS:
            self.indicators[f'SMA_{period}'] = self.I(talib.SMA, self.data.Close, period)
            self.indicators[f'EMA_{period}'] = self.I(talib.EMA, self.data.Close, period)
            self.indicators[f'RSI_{period}'] = self.I(talib.RSI, self.data.Close, period)
            self.indicators[f'ATR_{period}'] = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=period)
            
        # Bollinger Bands (BBANDS) calculation: upper, middle, lower
        for period in INDICATOR_PERIODS:
            self.indicators[f'BBANDS_{period}_upper'], \
            self.indicators[f'BBANDS_{period}_middle'], \
            self.indicators[f'BBANDS_{period}_lower'] = self.I(talib.BBANDS, self.data.Close, period)

    def preprocess_rule(self, rule):
        # Split the rule into condition and action
        condition_part, action_part = rule.split(" then ")

        # Remove 'if ' from the condition part
        condition_part = condition_part.strip().replace("if ", "")

        # Replace indicators in the condition part with their values
        def replace_indicator(match):
            indicator = match.group(0)
            period = re.search(r'\d+', indicator).group()  # Extract the period number (e.g., 10, 20, 50)

            # Identify the indicator type and return the corresponding value
            if f'SMA({period})' in indicator:
                return str(self.indicators[f'SMA_{period}'][-1])
            elif f'EMA({period})' in indicator:
                return str(self.indicators[f'EMA_{period}'][-1])
            elif f'RSI({period})' in indicator:
                return str(self.indicators[f'RSI_{period}'][-1])
            elif f'ATR({period})' in indicator:
                return str(self.indicators[f'ATR_{period}'][-1])
            elif f'BBANDS({period})_upper' in indicator:
                return str(self.indicators[f'BBANDS_{period}_upper'][-1])
            elif f'BBANDS({period})_lower' in indicator:
                return str(self.indicators[f'BBANDS_{period}_lower'][-1])
            else:
                raise ValueError(f"Unknown indicator in rule: {indicator}")

        # Create a regular expression to capture all the indicator patterns (SMA, EMA, RSI, ATR, BBANDS)
        indicator_pattern = r'(SMA\(\d+\)|EMA\(\d+\)|RSI\(\d+\)|ATR\(\d+\)|BBANDS\(\d+\)_(upper|lower))'

        # Replace indicators in the condition part with their actual values using regex
        processed_condition = re.sub(indicator_pattern, replace_indicator, condition_part)

        return processed_condition, action_part

    def next(self):
        # Prepare local variables for eval
        closing_price = self.data.Close[-1]
        open_price = self.data.Open[-1]
        high_price = self.data.High[-1]
        low_price = self.data.Low[-1]
        volume = self.data.Volume[-1]

        # Preprocess the rule to replace indicators with their values and split action
        condition, action = self.preprocess_rule(self.rule)

        # Use eval to execute the condition
        if eval(condition):  # Ensure only the logical condition is passed to eval
            if action == 'buy':
                self.buy()  # Execute buy action
            elif action == 'sell':
                self.sell()  # Execute sell action

def run_backtest(rule):
    CustomStrategy.rule = rule  # Set the strategy rule for this individual
    bt = Backtest(data, CustomStrategy, cash=INITIAL_CASH, commission=COMMISSION)
    stats = bt.run()
    print(stats)
    return stats['Return [%]']  # Fitness based on final equity
