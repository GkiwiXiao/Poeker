import time
from .player import Player


def simulate(table, nHands, firstTrain=0, nTrain=0, nBuyIn=0, tPrint=5, vocal=False):  

    """
    This function simulates several hands of Holdem according to these parameters:

    Parameters:
    table - table used in simulation (Table)
    nHands - total number of hands to simulate (int)
    firstTrain - number of hands before first training, when players take random actions (int)
    nTrain - number of hands between training players (int)
    nBuyIn - number of hands between cashing out/buying in players (int)
    tPrint - number of seconds between printing hand number (int)
    vocal - hands are narrated by table when vocal is True (bool)
    """

    print('Beginning simulation of', nHands, 'hands.')

    players = table.getPlayers()
    bankroll = [[] for p in players]    #holds bankroll history of all players
    maxBuyIn = table.getParams()[-1]

    #set Player stack sizes to max buy-in or less
    for p in players: 
        p.cashOut()
        if p.getStack() < maxBuyIn: p.buyChips(maxBuyIn)

    nextTrain = firstTrain    #next hand players will train
    if firstTrain == 0: nextTrain = nTrain
    nextBuyIn = nBuyIn        #next hand players will cash out and buy in
    hand = 1                  #hands started
    lastTime = time.time()    #last time printed hands completed
    while hand <= nHands:

        if time.time() - lastTime > tPrint:
            lastTime = time.time()
            print(hand - 1, 'hands simulated.')
        
        if hand == nextTrain:
            print('Players are training...')
            for p in players: p.train()
            nextTrain = hand + nTrain
            print('Complete.')

        if hand == nextBuyIn:
            if vocal: print('Players are cashing out and buying in.')
            for p in players:
                p.cashOut()
                if p.getStack() < maxBuyIn: p.buyChips(maxBuyIn)
            nextBuyIn = hand + nBuyIn

        if vocal: print('Hand', hand)
        played = table.playHand(vocal=vocal)
        
        #Hand failure
        if not played:    
            if nextBuyIn == hand + nBuyIn:    #if players just bought in
                print('All or all but one players are bankrupt.')
                break

            #buy in and redo hand
            if vocal: print('Not enough eligible players.')
            nextBuyIn = hand    
        
        else:
            hand += 1
            for i in range(len(players)): bankroll[i].append(players[i].getBankroll())

    print('Simulation complete.\n')
    return bankroll


class BasicPlayer(Player):

    # 生成当前游戏的特征，该特征独立于玩家的行动
    def _genGameFeatures(self, gameState):

        gameFeatures = 43 * [0]

        holeCards = sorted(self._cards)
        tableCards = sorted(gameState.cards)

        cards = holeCards + tableCards
        for i in range(len(cards)):
            gameFeatures[6 * i + 0] = 1
            gameFeatures[6 * i + 1] = cards[i].getNumber()
            suit = cards[i].getSuit()
            
            gameFeatures[6 * i + 2] = suit == 'c'
            gameFeatures[6 * i + 3] = suit == 'd'
            gameFeatures[6 * i + 4] = suit == 's'
            gameFeatures[6 * i + 5] = suit == 'h'

        gameFeatures[42] = self._stack

        return gameFeatures

    # 生成玩家行动的特征
    def _genActionFeatures(self, action, gameState):
        actionFeatures = 7 * [0]

        if action[0] == 'check': actionFeatures[0] = 1
        elif action[0] == 'fold': actionFeatures[1] = 1
        elif action[0] == 'call': actionFeatures[2] = 1
        elif action[0] == 'raise' or action[0] == 'bet':
            actionFeatures[3] = 1
            actionFeatures[4] = action[1]
            actionFeatures[5] = action[1] - max(gameState.currBets)
            actionFeatures[6] = actionFeatures[5] / sum(gameState.bets + gameState.currBets)
        else: raise Exception('Invalid action.')

        return actionFeatures
