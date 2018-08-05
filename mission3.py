import math
import sys
# data8 -> 234435068 yen

INF = 10000
T = 320
LEN = 21
datafile = "data8.csv"
sys.stderr.write(datafile)
sys.stderr.write("\n")
data = open(datafile, "r")
stock = [[] for i in range(3)]
route = []
distance = [INF for i in range(T)]
prev = [-1 for i in range(T)]
distance[0] = 0

#--------------------------------------
balance = 10000
kabu = [0 for i in range(3)]
#--------------------------------------
# functions
def buy(a, b, num = -1):
    global balance
    global kabu
    price = stock[a][b]
    flag = 0

    if balance < price:
        # error flag
        flag = -1
    elif num == -1:
        num = balance // price
    
    if num > 10000:
        num = 10000
        flag = 1
    if flag >= 0:
        kabu[a] = num
        balance -= price * num
    return flag

def sell(a, b, num = -1):
    global balance
    global kabu
    price = stock[a][b]

    if num == -1:
        num = kabu[a]

    kabu[a] -= num
    balance += price * num


# from datafile
count = 0
for line in data:
    if count == 0:
        count = 1
        continue
    tmp = line.split(",")
    stock[0].append(int(tmp[1]))
    stock[1].append(int(tmp[2]))
    stock[2].append(int(tmp[3]))

# make route list
N = 200
for i in range(N):
    if i + LEN > T:
        for j in range(i, i + 10):
            route.append([i, j, 0])
        for j in range(i + 10, T):
            rate_0 = stock[0][j] / stock[0][i]
            rate_1 = stock[1][j] / stock[1][i]
            rate_2 = stock[2][j] / stock[2][i]
            rate_max = max([rate_0, rate_1, rate_2])
            rate_max = math.log(rate_max)
            rate_max *= -1
            route.append([i, j, rate_max])
    else:
        for j in range(i, i + 10):
            route.append([i, j, 0])
        for j in range(i + 10, i + LEN):
            rate_0 = stock[0][j] / stock[0][i]
            rate_1 = stock[1][j] / stock[1][i]
            rate_2 = stock[2][j] / stock[2][i]
            rate_max = max([rate_0, rate_1, rate_2])
            rate_max = math.log(rate_max)
            rate_max *= -1
            route.append([i, j, rate_max])

# bellman ford (first)
for i in range(N):
    for line in route:
        u = line[0]
        v = line[1]
        w = line[2]
        if distance[v] > distance[u] + w:
            distance[v] = distance[u] + w
            prev[v] = u

place = N
first = []
while(place != -1):
    first.append(place)
    place = prev[place]
first.reverse()
#print(first)

#stock check (first)
mystock = -1
turning = 0
for i in range(len(first) - 1):
    a = first[i]
    b = first[i + 1]
    if b >= a + 10:
        if mystock != -1:
            print("sell(",mystock,",",a,")")
            sell(mystock, a)
            mystock = -1

        rate_0 = stock[0][b] / stock[0][a]
        rate_1 = stock[1][b] / stock[1][a]
        rate_2 = stock[2][b] / stock[2][a]
        rate_max = max([rate_0, rate_1, rate_2])
        mystock = [rate_0, rate_1, rate_2].index(rate_max)
        
        turning = buy(mystock, a)
        if turning == 1:
            sell(mystock, a) # roll back
            turning = a
            break
        else:
            print("buy(",mystock,",",a,")")
    else:
        print("sell(",mystock,",",a,")")
        sell(mystock, a)
        mystock = -1

sys.stderr.write("turning ")
sys.stderr.write(str(turning))
sys.stderr.write("\n")
sys.stderr.write("balance ")
sys.stderr.write(str(balance))
sys.stderr.write("\n")

# first ends
#-------------------------------------------------------------------
# second starts

# buy = -1, sell = 1
lat = []

balance_tmp = balance
# make route list
for k in range(3):
    route = []
    distance = [INF for i in range(T)]
    prev = [-1 for i in range(T)]
    distance[turning] = 0

    N = T - 10
    for i in range(turning, N):
        if i + LEN > T:
            for j in range(i, i + 10):
                route.append([i, j, 0])
            for j in range(i + 10, T):
                rate = stock[k][j] / stock[k][i] #here
                rate = math.log(rate)
                rate *= -1
                route.append([i, j, rate])
        else:
            for j in range(i, i + 10):
                route.append([i, j, 0])
            for j in range(i + 10, i + LEN):
                rate = stock[k][j] / stock[k][i] #here
                rate = math.log(rate)
                rate *= -1
                route.append([i, j, rate])
    for i in range(N, T):
        route.append([i, T-1, 0])

    # bellman ford (second)
    for i in range(turning, T-1):
        for line in route:
            u = line[0]
            v = line[1]
            w = line[2]
            if distance[v] > distance[u] + w:
                distance[v] = distance[u] + w
                prev[v] = u

    place = T-1
    second = []
    while(place != -1):
        second.append(place)
        place = prev[place]
    second.reverse()
    #print(second)

    #stock check (second)
    mystock = -1 # -1 means that I have not any stocks.
    for i in range(len(second) - 1):
        a = second[i]
        b = second[i + 1]
        if b >= a + 10:
            if mystock != -1:
                #print("sell(",mystock,",",a,")")
                sell(mystock, a)
                lat.append([mystock, a, 1])
                mystock = -1
            # not else
            mystock = k
            buy(mystock, a)
            lat.append([mystock, a, -1])
            #print("buy(",mystock,",",a,")")
        elif mystock != -1:
            #print("sell(",mystock,",",a,")")
            sell(mystock, a)
            lat.append([mystock, a, 1])
            mystock = -1
    # i == len(second) - 1
    # b = last, a = last - 1
    if b >= a + 10:
        if mystock != -1:
            #print("sell(",mystock,",",b,")")
            sell(mystock, b)
            lat.append([mystock, b, 1])
            mystock = -1

#-------------------------------------------------
balance = balance_tmp
lat = sorted(lat, key = lambda x: x[1])

for line in lat:
    if line[2] == -1:
        flag = buy(line[0], line[1])
        if flag != -1:
            print("buy(",line[0],",",line[1],")")
    else:
        sell(line[0], line[1])
        print("sell(",line[0],",",line[1],")")

sys.stderr.write("balance ")
sys.stderr.write(str(balance))