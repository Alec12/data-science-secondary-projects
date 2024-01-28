# Project : Build  a Second-Price Auction (Modeling and Strategy)

## Context:

After being hired by a major retailer to develop algorithms for an online ad auction. Your client knows a little about the multi-armed bandit literature and recognizes that it can spend money to explore, learning how likely users are to click on ads, or to exploit, spending on the most promising users to maximize immediate payoffs. At the same time, there are other companies participating in the auction that may outbid your client, potentially interfering with these goals. Your task is to model the ad auction and develop an effective algorithm for bidding in a landscape of strategic competitors. Your client plans to test your bidding algorithm against other bidding algorithms contributed by other data scientists, in order to select the most promising algorithm.

## Goal:

Develop class architecture that models a typical second price auction, multiple bidder competitions, and Users with a probability to click on an ad. Build a model that maximizes immediate payoffs.

Assume that you are one of many bidders, there are millions of auctions, and various collections of users on a given ad space.