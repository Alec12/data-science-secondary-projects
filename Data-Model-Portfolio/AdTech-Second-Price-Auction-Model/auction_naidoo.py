import random
import numpy as np

class User:
    """User Class for the Auction"""
    _instance_count = 0
    def __init__(self):
        self.__probability = random.uniform(0,1)
        self.user_id = User._instance_count
        User._instance_count += 1

    def __repr__(self):
        return f"u{self.user_id}"

    def __str__(self):
        return f"u{self.user_id}"
    
    def show_ad(self):
        """This method should return True to represent the user clicking on and ad and
            otherwise."""
        return True if np.random.rand() <= self.__probability else False

class Auction:
    
    def __init__(self, users, bidders):
        self.users = users
        self.bidders = bidders
        self.balances = {bidder: 0 for bidder in self.bidders}
        self.balances_history = []
        self.round_count = 1

    def __repr__(self):
        return f"Auction(users={self.users}, bidders={self.bidders})"

    def __str__(self):
        return f"Auction with {len(self.users)} users and {len(self.bidders)} bidders"

    def execute_round(self):
        """Execute all steps within a single round of the game."""
        user_id = random.choice(self.users)
        bids = {}

        for bidder in self.bidders:
            final_bid = bidder.bid(user_id)
            bids[bidder] = max(0, final_bid)

        highest_bid = max((bid for bid in bids.values() if bid is not None), default=None)
        tie_bidders = [bidder for bidder, bid in bids.items() if bid == highest_bid]

        if len(tie_bidders) >= 2:
            winner = random.choice(tie_bidders)
            tie_bidders.remove(winner)
            second_highest_bid = bids[random.choice(tie_bidders)]
        else:
            winner = tie_bidders[0]
            second_highest_bid = float('-inf')

        for bidder, bid in bids.items():
            if bid is not None and bid > second_highest_bid and bidder != winner:
                second_highest_bid = bid

        clicked = user_id.show_ad()

        for bidder in self.bidders:
            if bidder == winner:
                bidder.notify(auction_winner=True, price=second_highest_bid, clicked=clicked)
                if clicked==True:
                    self.balances[winner] += (1 - second_highest_bid)
                else:
                    self.balances[winner] -= second_highest_bid
            else:
                bidder.notify(auction_winner=False, price=second_highest_bid, clicked=None)
                self.balances[bidder] = 0

        for bidder in self.bidders:
            self.balances_history.append((bidder, self.round_count, bids[bidder], user_id, clicked, self.balances[bidder]))
        self.round_count += 1