from load import *
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score


'''Data systhesis'''   

def Data(total, num: int):
    X = pd.DataFrame()
    for i in range(0, len(total)):
        X['Power' + str(i)] = total[i].frame['Power'].dropna().to_numpy()[0:20]
    y = np.linspace(0, 100, num)
    return X, y


'''Training sets'''
def train_test_set(X, y, test_size, cv_size):
    X_train1, X_test, y_train1, y_test = train_test_split(X, y, test_size = test_size)

    refine_size = cv_size / (1-test_size)

    X_train, X_cv, y_train, y_cv = train_test_split(X_train1, y_train1, test_size = refine_size)

    return[X_train, X_test, X_cv, y_train, y_test, y_cv]

'''Standardization'''
def scale(X_train, X_test, X_cv):
    scaler = StandardScaler().fit(X_train.T)

    X_train1 = scaler.fit_transform(X_train.T)
    X_test1 = scaler.transform(X_test.T)
    X_cv1 = scaler.transform(X_cv.T)

    return[X_train1, X_test1, X_cv1]


'''Bestlearningrate'''
def lrate():
    
    return lr_best


'''Training'''
def model(X, y, n_epochs, learning_rate = 1e-3, tot_tol = 1e-5):

    


    return
    

total = iterate_points(type=0, frames=[1], stringers=[1,2])

X, y = Data(total, num = 20)
X_train, X_test, X_cv, y_train, y_test, y_cv = train_test_set(X, y, test_size=0.15, cv_size=0.1)

print(X_train.index)


#plt.scatter(np.linspace(0, 100, 20), total[3].frame['Power'].dropna().to_numpy()[0:20])
#plt.scatter()
#plt.show()


#for i in atotal:
#     i.plot(ax, power=True)
#plot_legends()