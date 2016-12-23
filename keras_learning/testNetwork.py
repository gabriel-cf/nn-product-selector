from nn import NN
import numpy as np

x = np.array([[0.,1.,0.]])
y = np.array([[1.]])
print("#1")
NN.getInstance()
print("#2")
network = NN.getInstance()
print("#3")
network.evaluate(x, y) # 0;1;0;1
print("#4")
print(network.predict(x))