from learner import Table
from learner.templates import simulate, BasicPlayer
import numpy as np

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor

if __name__ == '__main__':

    t = Table(smallBlind=1, bigBlind=2, maxBuyIn=200)

    players = []
    for i in range(6):
        
        name = 'Player ' + str(i+1)
        p = BasicPlayer(name=name, bankroll=10**6, nRaises=10, rFactor=.7, memory=10**5)
        players.append(p)

    for p in players: t.addPlayer(p)

    simulate(t, nHands=1000, nBuyIn=10, nTrain=0, vocal=False)

    features = []
    labels = []

    for p in players:
        features.extend(p.getFeatures())
        labels.extend(p.getLabels())

    features = np.array(features)
    labels = np.array(labels)

    #shuffle features/labels
    index = np.arange(len(labels))
    np.random.shuffle(index)
    features = features[index]
    labels = labels[index]

    #initialize regressors with default parameters
    regressors = {LinearRegression(): 'LinearRegression',
                  Lasso(): 'Lasso',
                  RandomForestRegressor(): 'RandomForestRegressor',
                  GradientBoostingRegressor(): 'GradientBoostingRegressor',
                  MLPRegressor(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', alpha=0.001, max_iter=1000): 'MlpRegressor'
    }
    
    for r in regressors:
        print('Cross-validating ' + regressors[r] + '...')
        print('Rsquared:', np.mean(cross_val_score(r, features, labels)))
        print()
