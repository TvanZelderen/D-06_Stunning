from load import *
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import torch
import torch.nn as nn
from typing import Callable

#class filter()



'''Data systhesis'''   

def Data(total, num: int):
    X = pd.DataFrame()
    for i in range(0, len(total)):
        X['Power' + str(i)] = total[i].frame['Power'].dropna().to_numpy()[0:num]
    y = X.index
    return X, torch.Tensor(y).reshape(-1, 1)

'''Training sets'''
def train_test_set(X, y, test_size, cv_size):
    X_train1, X_test, y_train1, y_test = train_test_split(X, y, test_size = test_size)

    refine_size = cv_size / (1-test_size)

    X_train, X_cv, y_train, y_cv = train_test_split(X_train1, y_train1, test_size = refine_size)

    return[X_train, X_test, X_cv, y_train, y_test, y_cv]

'''Standardization'''
def scale(X):
    
    X_1 = (X.sub(X.mean(axis = 1).to_numpy(), axis = 0)).div(X.std(axis = 1), axis = 0)
    X_1.fillna(0, inplace = True)

    return X_1


'''Bestlearningrate'''
def lrate(X, y, ):

    
    return lr_best


'''Training'''
def model(dim_hidden: int, dim_input: int, dim_output: int):
    model = nn.Sequential(
        nn.Linear(dim_input, dim_hidden),
        nn.Sigmoid(),
        nn.Linear(dim_hidden, dim_hidden),
        nn.Sigmoid(),
        nn.Linear(dim_hidden, dim_output)
    )
    
    return model

'''Learning'''
def train_model_early_stop(model: nn.modules, X_train: torch.tensor, y_train: torch.tensor, X_cv: torch.tensor,
                            y_cv: torch.tensor, loss_function: Callable, optimizer: torch.optim.Optimizer, tot_tol: float = 1e-5, n_epochs: int = 200):
    train_loss_history = []
    val_loss_history = []

    for i in range(n_epochs):
        
        y_pred = model(X_train)
        y_pred_cv = model(X_cv)

        loss = loss_function(y_pred, y_train)
        val_loss = loss_function(y_pred_cv, y_cv)
        train_loss_history.append(loss.detach().numpy())
        val_loss_history.append(val_loss.detach().numpy())

        if loss < tot_tol:
            break

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return train_loss_history, val_loss_history

    
if __name__ == '__main__':

    total = iterate_points(type=0, frames=[1], stringers=[1, 2])

    X, y = Data(total, num = 30)

    X = scale(X)
    X = torch.Tensor(X.values)

    X_train, X_test, X_cv, y_train, y_test, y_cv = train_test_set(X, y, test_size=0.15, cv_size=0.1)

    model_ = model(dim_hidden=10, dim_input=X_train.size()[1], dim_output=1)

    train_loss_history, validation_loss_history = train_model_early_stop(model_, X_train, y_train, X_cv, y_cv, 
                                                                        loss_function = nn.MSELoss(), optimizer = torch.optim.Adam(model_.parameters(), lr = 0.1))
    print(train_loss_history)

 #plt.plot(train_loss_history)
    #plt.show()
    X_test0 = iterate_points(type=0, frames=[2], stringers=[1, 2])
    X_test0, y = Data(total, num = 30)
    X = scale(X_test0)
    X = torch.Tensor(X.values)
    X_pred = model_(X)
    fig, ax = plt.subplot()
    for i in range(X_pred.size()[1]):
        ax.plot(X_pred.detach().numpy()[:,i], lable = f'stringers{i + 1}')
    plt.show()
'''  '''


'''
#plt.scatter(np.linspace(0, 100, 20), total[3].frame['Power'].dropna().to_numpy()[0:20])
#plt.scatter()
#plt.show()


for i in atotal:
     i.plot(ax, power=True)  
pred.plot(ax, power=True)
plot_legends()'''