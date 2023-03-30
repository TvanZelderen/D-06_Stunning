from load import *
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
from typing import Callable
from scipy import stats
from scipy.integrate import simpson
#from total_energy import total_energy
import pandas as pd
'''
class filter():

    def __energy(self):

    def'''




'''Data systhesis'''   

def Data(total, num: int):
    y = pd.DataFrame()
    energy = []
    for i in range(0, len(total)):
        y['Power' + str(i)] = total[i].frame['Power'].dropna().to_numpy()[0:num]
        p = total[i].frame['Power'].dropna().to_numpy()
        t = total[i].frame['Time'].drop(total[i].frame['Power'].isna()*range(len(total[i].frame['Power']))).to_numpy()
        energy.append(simpson(p, t))    
    X = pd.Series(energy).values
    return X, y.T

'''Training sets'''
def train_test_set(X, y, test_size, cv_size):
    X_train1, X_test, y_train1, y_test = train_test_split(X, y, test_size = test_size)

    refine_size = cv_size / (1-test_size)

    X_train, X_cv, y_train, y_cv = train_test_split(X_train1, y_train1, test_size = refine_size)

    return[X_train, X_test, X_cv, y_train, y_test, y_cv]

'''Standardization'''
def scale(X):
    
    X_1 = (X.sub(X.mean(axis = 0).to_numpy(), axis = 1)).div(X.std(axis = 0), axis = 1)
    X_1.fillna(0, inplace = True)

    return X_1


'''Training'''
def model(dim_hidden: int, dim_input: int, dim_output: int):
    model = nn.Sequential(
        nn.Transformer(dim_input, dim_hidden),
        nn.ReLU(),
        nn.Transformer(dim_hidden, dim_hidden),
        nn.ReLU(),
        nn.Transformer(dim_hidden, dim_output)
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

'''Weightinitiation'''
def weights_init(layer: nn.Module) -> None:
    if isinstance(layer, nn.Linear):
        nn.init.xavier_uniform_(layer.weight)
        nn.init.zeros_(layer.bias)

'''Bestlearningrate'''
def lrate(model, X_train, y_train, X_val, y_val, reps: int):
    lr_best = 0
    loss_min = 1
    rvs = stats.loguniform.rvs(1e-3, 1, size=reps)

    for i in range(reps):
        model.apply(weights_init)
        train_loss, val_loss = train_model_early_stop(model, X_train, y_train, X_val, y_val, 
                                                      loss_function = nn.MSELoss(), optimizer=torch.optim.Adam(params = model.parameters(), lr = rvs[i]))
        if val_loss[-1] < loss_min:
            loss_min = val_loss[-1]
            lr_best = rvs[i]
        else:
            continue
    
    return lr_best
    
if __name__ == '__main__':
    #energy_matrix = total_energy(1, [2, 3], [1], 1)
    #print(energy_matrix)

    

    total = iterate_points(type=0, frames=[1], stringers=[1, 2, 4])

    number_data = 20

    X, y = Data(total, num = number_data)
    print(X.shape, y.size)
'''
    #y = scale(y)
    X = torch.Tensor(X)
    y = torch.Tensor(y.values)
    #print(X.size(), y.size())

    X_train, X_test, X_cv, y_train, y_test, y_cv = train_test_set(X, y, test_size=0.15, cv_size=0.1)
    #print(X_train, X_test, X_cv)

    #model_ = model(dim_hidden=10, dim_input=X_train.size()[1], dim_output=1)
    model_1 = model(dim_hidden=10, dim_input=1, dim_output = number_data)

    lr_best = lrate(model_1, X_train, y_train, X_cv, y_cv, reps = 20)
    print(lr_best)

    train_loss_history, validation_loss_history = train_model_early_stop(model_, X_train, y_train, X_cv, y_cv, 
                                                                        loss_function = nn.MSELoss(), optimizer = torch.optim.Adam(model_.parameters(), lr = lr_best))
    #plt.plot(train_loss_history)
    #plt.show()

    #print(y_test)
    #plt.scatter(X_test.detach().numpy(), y.detach().numpy())
    #plt.show()

    #plt.scatter(np.linspace(0, 100, 20), total[3].frame['Power'].dropna().to_numpy()[0:20])
    #plt.scatter()
    #plt.show()
'''


    #atotal = iterate_points(type=1, frames=[1], stringers=[1,2,4,5,6,7])
    #ax = plot_ini('test')
    #for i in atotal:
    #    i.plot(ax, power=True)  
    #pred.plot(ax, power=True)
    #plot_legends()
