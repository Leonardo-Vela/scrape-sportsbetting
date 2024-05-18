import numpy as np
# doc string

def calc_spread(odds_list):
    num_odds = len(odds_list)
    inverse_odds_list = [1/x for x in odds_list]
    spread = round((1/sum(inverse_odds_list))-1,5)
    return spread 

def calc_probs(odds_list):
    num_odds = len(odds_list)
    spread = calc_spread(odds_list)
    probs = [(spread + 1)/x for x in odds_list]
    return probs

def calc_break_even(odds_list):
    inverse_odds_list = [1/x for x in odds_list]
    break_even_odd = 1/(1-sum(inverse_odds_list))
    return break_even_odd
