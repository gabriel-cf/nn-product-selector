from nn import NN
import numpy as np

x1 = np.array([[0.,0.,20.,7.,0.1]]) # 0;0;20;7;0
y1 = np.array([[0.199415754]])
x2 = np.array([[0.,0.,69.,7.,4.9]]) # 0;0;69;7;4.9;0.988423931
y2 = np.array([[0.988423931]])

print("#1")
NN.getInstance()
print("#2")
network = NN.getInstance()
print("#3")
network.evaluate(x1, y1) # 0;1;0;1
print("#4")
print(network.predict(x1))

print("#3")
network.evaluate(x2, y2) # 0;1;0;1
print("#4")
print(network.predict(x2))