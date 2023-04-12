import numpy as np
from sklearn.model_selection import learning_curve

def grad_desc(x,y):
    mi = bi = 0
    iterations = 10000
    n = len(x)
    learning_rate = 0.082

    for i in range(iterations):
        y_pred = mi * x + bi
        cost = (1/n) * sum(val**2 for val in (y-y_pred))
        md = -(2/n) * sum(x*(y - y_pred))
        bd = -(2/n) * sum(y - y_pred)
        mi = mi - learning_rate * md
        bi = bi - learning_rate * bd
        print(f"Iteration: {i}\t m: {mi}\t b: {bi}\t Cost: {cost}")


x = np.array([1,2,3,4,5])
y = np.array([5,7,9,11,13])

grad_desc(x,y)