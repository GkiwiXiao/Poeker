from learner import Table
import matplotlib.pyplot as plt
from learner.templates import simulate, BasicPlayer
from sklearn.ensemble import GradientBoostingRegressor

if __name__ == '__main__':

    # 建立Table，小盲注为1，大盲注为2，最大下注为200
    # Create a table with a small blind of 1, a big blind of 2 and a maximum bet of 200
    t = Table(smallBlind=1, bigBlind=2, maxBuyIn=200)

    # 建立player
    # Create player
    players = []

    # 建立4个玩家
    # Create 4 players
    for i in range(4):
        r = GradientBoostingRegressor()
        name = 'Player ' + str(i+1)
        p = BasicPlayer(name=name, reg=r, bankroll=10**6, nRaises=10, rFactor=.7, memory=10**5)
        players.append(p)

    for p in players:
        t.addPlayer(p)

    # 模拟20000手并保存每个玩家的bankroll
    # Simulate 20,000 hands and save bankroll for each player

    bankrolls = simulate(t, nHands=20000, nTrain=0, nBuyIn=10)

    # 可视化
    # Visualization
    for i in range(4):
        bankroll = bankrolls[i]
        plt.plot(range(len(bankroll)), bankroll, label=players[i].getName())
    plt.title('Player bankroll vs Hands played')        
    plt.xlabel('Hands played')
    plt.ylabel('Player bankroll/wealth')
    plt.legend(loc='upper left')
    plt.show()
