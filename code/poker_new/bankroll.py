from learner import Table
import matplotlib.pyplot as plt
from learner.templates import simulate, BasicPlayer
import warnings
warnings.filterwarnings("ignore")
from sklearn.neural_network import MLPRegressor

fit1 = MLPRegressor(
        hidden_layer_sizes=(100, 50), activation='relu', solver='adam',
        alpha=0.01, max_iter=200)

if __name__ == '__main__':

    # 建立Table，小盲注为1，大盲注为2，最大下注为200
    # Create a table with a small blind of 1, a big blind of 2 and a maximum bet of 200
    t = Table(smallBlind=1, bigBlind=2, maxBuyIn=200)

    # 建立gambler
    # Create gambler
    gamblers = []

    # 建立4个玩家
    # Create 4 players
    for i in range(4):
        # r = SVR()
        r = fit1
        name = 'Player ' + str(i+1)
        p = BasicPlayer(name=name, reg=r, bankroll=10**6, nRaises=10, rFactor=.7, memory=10**5)
        p.stopTraining()
        gamblers.append(p)

    for p in gamblers:
        t.addPlayer(p)

    # 训练第一个玩家1000手
    # Train the first player 1000 hands
    gamblers[0].startTraining()
    simulate(t, nHands=1000, nTrain=10, nBuyIn=10)
    gamblers[0].stopTraining()
    
    # 训练第二个玩家10000手
    # Train a second player 10,000 hands
    gamblers[1].startTraining()
    simulate(t, nHands=1000, nTrain=1000, nBuyIn=10)
    gamblers[1].stopTraining()

    for p in gamblers:
        p.setBankroll(10**6)

    # 模拟20000手并保存每个玩家的bankroll
    # Simulate 20,000 hands and save each player's bankroll
    bankrolls = simulate(t, nHands=20000, nTrain=0, nBuyIn=10)

    # 可视化
    # Visualization
    for i in range(4):
        bankroll = bankrolls[i]
        plt.plot(range(len(bankroll)), bankroll, label=gamblers[i].getName())
    plt.title('Player bankroll vs Hands played')        
    plt.xlabel('Hands played')
    plt.ylabel('Player bankroll/wealth')
    plt.legend(loc='upper left')
    plt.show()
