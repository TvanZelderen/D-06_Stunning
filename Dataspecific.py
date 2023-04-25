import numpy as np
from keras import Sequential
from keras.layers import Input, Dense
from keras.models import Model
import matplotlib.pyplot as plt
from load import *
from sklearn.preprocessing import Normalizer, StandardScaler
import seaborn as sns
#from scipy.interpolate import interp1d
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics.pairwise import cosine_distances

def Data(total):
    X = pd.DataFrame()
    max_row = 0
    
    for i in range(0, len(total)):
        tmp_col = total[i].frame['Power'].dropna().to_numpy()
        #print(tmp_col, tmp_col.shape[0])
        if tmp_col.shape[0] > max_row:
                max_row = tmp_col.shape[0]

    for i in range(0, len(total)):
        #count = 0
        tmp_col_1 = pd.DataFrame(total[i].frame['Power'].dropna().to_numpy())
        #num_row = tmp_col_1.shape[0]
        """if num_row < max_row:
            n = max_row - num_row
            m = int(max/n)
            f1 = interp1d(tmp_col_1.columns.to_numpy(), tmp_col_1.values.to_numpy(), kind = 'cubic')
            for j in range(0, tmp_col_1.shape[0]):
                
                
                tmp_col_1.insert(f1())
            print(tmp_col_2)"""
        #tmp_col_2 = np.pad(tmp_col_1, (0, (max_row-num_row)))
        X = pd.concat([X, tmp_col_1], axis=1)
        X.fillna(0, inplace=True)
    return X.T
#clip_to_skin
frame0 = [1,2,3,4,5,6,7,8,9,10,11,12]
stringer0 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]

#clip_to_frame
frame1 = [1,2,3,4,5,6,7,8,9,10,11,12]
stringer1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]


total = iterate_points(type = 1, frames = frame1[::], stringers = stringer1[::])
X = Data(total)
#print(X)

scaler_1 = StandardScaler()
normalized_features_1 = scaler_1.fit_transform(X)
scaler = Normalizer()
normalized_features = scaler.fit_transform(normalized_features_1)
normalized_data = pd.DataFrame(normalized_features, columns = X.columns)

#print(normalized_data)

original_dim = X.shape[1]
encoding_dim = 4

encoder = Sequential(
    [
    Dense(80, name = '1st_hidden_layer', input_shape = (original_dim,), activation='relu'),
    Dense(32, name = '2nd_hidden_layer', input_shape = (80, ), activation='relu'),
    Dense(encoding_dim, name = 'encoding_Layer', activation='relu')
    ]
)

decoder = Sequential(
     [
     Dense(32, name = '4th_hidden_layer', input_shape = (encoding_dim,), activation='relu'),
     Dense(80, name = '5th_hidden_layer', input_shape = (32, ), activation='relu'),
     Dense(original_dim, name = 'output_layer')
     ]
)
# Autoencoder
encoder_decoder_model = Model(
     inputs = encoder.inputs,
     outputs = decoder(encoder.outputs)
)

encoder_decoder_model.compile(loss = 'mse', optimizer = 'adam', metrics = 'mse')
results = encoder_decoder_model.evaluate(
     x = normalized_data,
     y = normalized_data,
     verbose = 0
)
print('Base line model: loss', results[0])

#training model
model_history = encoder_decoder_model.fit(
     x = normalized_data,
     y = normalized_data,
     epochs = 30,
     batch_size = 32,
     verbose = 1,
     validation_split= 0.3
)

post_results = encoder_decoder_model.evaluate(
     x = normalized_data,
     y = normalized_data,
     verbose = 0
)
print('Base line model: loss', post_results[0])

encodings = encoder(normalized_data.values)
X1 = encodings.numpy()
#print(X1)
cosine_dist_matrix = cosine_distances(X1)

#clustering
np.random.seed(42)
clf = LocalOutlierFactor(n_neighbors = 20, contamination = 'auto', metric = 'precomputed')

y_1 = clf.fit(cosine_dist_matrix)
X_scores_1 = clf.negative_outlier_factor_

#report the outlier
threshold = -1.5
outlier_indice = np.where(X_scores_3 < threshold)[0]
print(total[outlier_indice[0]].main_label)
#print(X_scores_3)

plt.title("Local Outlier Factor (LOF)")

plt.scatter(X1[:,0], X1[:, 1], color="m", s=3.0, label="Data points")
# plot circles with radius proportional to the outlier scores
radius_1 = (X_scores_1.max() - X_scores_1) / (X_scores_1.max() - X_scores_1.min())
plt.scatter(
    X1[:, 0],
    X1[:, 1],
    s=1000 * radius_1,
    edgecolors="g",
    facecolors="none",
    label="Outlier scores",
)

plt.axis("tight")
plt.xlim((-0.1, 1.5))
plt.ylim((-0.1, 1.5))
legend = plt.legend(loc="upper left")
plt.show()





