# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:24:07 2024

@author: niran
"""


import random
from PokerHand import ThreeCardPokerDeck, ThreeCardPokerHand
from Card import Card

def make_dist(n):
    
    count_of_hand = {label: 0 for label in ThreeCardPokerHand.all_labels}


    for _ in range(n):
        deck = ThreeCardPokerDeck()
        deck.shuffle()

        hand = ThreeCardPokerHand(deck.pop_cards(3))

        label = hand.get_label()
        count_of_hand[label] += 1

    probs = {label: round(count / n * 100,2) for label, count in count_of_hand.items()}

    return probs



min_dealer_hand = ThreeCardPokerHand([Card(10, 0), Card(1, 1), Card(0, 2)])


def play_round(dealer_hand, player_hand, cash, get_ante, is_playing):

    ante = get_ante(cash)


    if not is_playing(player_hand):
        return ante, -1 


    min_dealer_hand = ThreeCardPokerHand([Card("Queen", "Hearts"), Card("5", "Clubs"), Card("2", "Spades")])  


    dealer_qualifies = dealer_hand._compare(min_dealer_hand) >= 0

    if not dealer_qualifies:
        return ante, 1  

   
    comparison_result = player_hand._compare(dealer_hand)

    if comparison_result > 0:
        return ante, 2  
    elif comparison_result < 0:
        return ante, -2  
    else:
        return ante, 0  
    

    
def get_ante(cash):

    return int(input('Enter your ante bet (Cash=' + str(cash) + '): '))
    
def is_playing(player_hand):

    print(player_hand)
    return True if input("Play or fold  (p/f): ") == 'p' else False

def proc_outcome(outcome, ante, dealer_hand):

    out = ['Tie', 'Dealer does not qualify', 'You won', 'You lost', 'You folded']
    payoff = outcome * ante
    print(dealer_hand)
    print(out[outcome] + ': ' + ('+' if payoff > 0 else '') + str(payoff))
    return payoff

def play(trials, stake, goal):

    wins, gain, rounds, win_rounds, tie_rounds, lose_rounds = 0, 0, 0, 0, 0, 0
    for _ in range(trials):
        cash = stake
        while cash > 0 and cash < goal:
            deck = ThreeCardPokerDeck()
            deck.shuffle()
            player_hand = deck.deal_hand("Player")
            dealer_hand = deck.deal_hand("Dealer")

            (ante, outcome) = \
                play_round(dealer_hand, player_hand, cash, get_ante, is_playing)
            cash += proc_outcome(outcome, ante, dealer_hand)
            rounds += 1
            win_rounds += 1 if outcome > 0 else 0
            tie_rounds += 1 if outcome == 0 else 0
            lose_rounds += 1 if outcome < 0 else 0
        wins += 1 if cash >= goal else 0
        gain += cash - stake
    print('Finished', trials, 'trial games')
    print('Winning games (%)', 100 * wins / trials)
    print('Average gain per game', gain / trials)
    print('Average number of rounds per game:', rounds / trials)
    print('Average number of winning rounds per game:', win_rounds / trials)
    print('Average number of tied rounds per game:', tie_rounds / trials)
    print('Average number of losing rounds per game:', lose_rounds / trials)

if __name__ == '__main__':

    print(make_dist(10000))
    

    play(1, 100, 200)
 