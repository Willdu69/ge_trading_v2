# grammar.py

import random

def get_grammar():
    grammar = {
        "<rule>": ["if <condition> then <action>"],
        "<condition>": [
            # "<indicator> <operator> <value>",
            "<indicator> <operator> <value> and <indicator> <operator> <value>",
            "<indicator> <operator> <value> and <indicator> <operator> <value> and <indicator> <operator> <value>",
            "<indicator> <operator> <value> and <indicator> <operator> <value> and <indicator> <operator> <value> and <indicator> <operator> <value>"
        ],
        "<operator>": [">", "<", ">=", "<="],
        "<indicator>": [
            "SMA({})".format(period) for period in [10, 20, 50]
        ] + [
            "EMA({})".format(period) for period in [10, 20, 50]
        ] + [
            "RSI({})".format(period) for period in [10, 20, 50]
        ] + [
            "BBANDS({})_upper".format(period) for period in [10, 20, 50]
        ] + [
            "BBANDS({})_lower".format(period) for period in [10, 20, 50]
        ] + [
            "ATR({})".format(period) for period in [10, 20, 50]
        ],
        "<value>": ["closing_price", "open_price", "high_price", "low_price", "volume"],
        "<action>": ["buy", "sell"]
    }
    return grammar

def generate_rule(grammar):
    def replace_non_terminal(symbol):
        rule = random.choice(grammar[symbol])
        while any(char in rule for char in grammar):
            for non_terminal in grammar:
                if non_terminal in rule:
                    rule = rule.replace(non_terminal, random.choice(grammar[non_terminal]), 1)
        return rule

    return replace_non_terminal("<rule>")
