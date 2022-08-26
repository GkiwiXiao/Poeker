from learner import Table
from learner.templates import simulate, BasicPlayer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor

fit1 = MLPRegressor(
        hidden_layer_sizes=(100, 50), activation='relu', solver='adam',
        alpha=0.01, max_iter=200)

if __name__ == '__main__':

    t = Table(smallBlind=1, bigBlind=2, maxBuyIn=200)

    players = []
    for i in range(6):
        
        r = fit1()
        name = 'Player ' + str(i+1)
        p = BasicPlayer(name=name, reg=r, bankroll=10**6, nRaises=10, rFactor=.7, memory=10**5)
        players.append(p)

    for p in players: t.addPlayer(p)

    simulate(t, nHands=10000, firstTrain=2000, nTrain=1000, nBuyIn=10)
    simulate(t, nHands=20, nBuyIn=10, vocal=True)
