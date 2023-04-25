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
'''Data processing'''
#clip_to_skin
frame0 = [1,2,3,4,5,6,7,8,9,10,11,12]
stringer0 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
total0 = iterate_points(type = 0, frames = frame0[::], stringers = stringer0[::])
X0 = Data(total0)
#clip_to_frame
frame1 = [1,2,3,4,5,6,7,8,9,10,11,12]
stringer1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
total1 = iterate_points(type = 1, frames = frame0[::], stringers = stringer0[::])
X1 = Data(total1)
#print(X)

'''Data Normalization'''
scaler_0 = StandardScaler()
normalized_features_0 = scaler_0.fit_transform(X0)
normalized_features_1 = scaler_0.fit_transform(X1)
scaler = Normalizer()
normalized_features0 = scaler.fit_transform(normalized_features_0)
normalized_data0 = pd.DataFrame(normalized_features0, columns = X0.columns)
normalized_features1 = scaler.fit_transform(normalized_features_1)
normalized_data1 = pd.DataFrame(normalized_features1, columns = X1.columns)
#print(normalized_data)

'''Training the data'''
original_dim = X0.shape[1]
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
     x = normalized_data0,
     y = normalized_data0,
     verbose = 0
)
print('Base line model: loss', results[0])

#training model
model_history = encoder_decoder_model.fit(
     x = normalized_data0,
     y = normalized_data0,
     epochs = 30,
     batch_size = 32,
     verbose = 1,
     validation_split= 0.3
)

post_results = encoder_decoder_model.evaluate(
     x = normalized_data0,
     y = normalized_data0,
     verbose = 0
)
print('Base line model: loss', post_results[0])

encodings = encoder(normalized_data0.values)
X_0 = encodings.numpy()
cosine_dist_matrix = cosine_distances(X_0)

#clustering
np.random.seed(42)
clf = LocalOutlierFactor(n_neighbors = 20, contamination = 'auto', metric = 'precomputed')
y_0 = clf.fit(cosine_dist_matrix)
X_scores_0 = clf.negative_outlier_factor_

#report the outlier
threshold = -1.6
outlier_indice_0 = np.where(X_scores_0 < threshold)[0]
#print(total0[outlier_indice_0[0]].main_label)



original_dim = X1.shape[1]
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
     x = normalized_data1,
     y = normalized_data1,
     verbose = 0
)
print('Base line model: loss', results[0])

#training model
model_history = encoder_decoder_model.fit(
     x = normalized_data1,
     y = normalized_data1,
     epochs = 30,
     batch_size = 32,
     verbose = 1,
     validation_split= 0.3
)

post_results = encoder_decoder_model.evaluate(
     x = normalized_data1,
     y = normalized_data1,
     verbose = 0
)
print('Base line model: loss', post_results[0])

encodings = encoder(normalized_data1.values)
X_1 = encodings.numpy()
cosine_dist_matrix = cosine_distances(X_1)

#clustering
np.random.seed(42)
clf = LocalOutlierFactor(n_neighbors = 20, contamination = 'auto', metric = 'precomputed')
y_1 = clf.fit(cosine_dist_matrix)
X_scores_1 = clf.negative_outlier_factor_

#report the outlier
threshold = -1.5
outlier_indice_1 = np.where(X_scores_1 < threshold)[0]
#print(total1[outlier_indice_1[0]].main_label)




'''Visualization'''
'''
fig, (ax0, ax1) = plt.subplots(1, 2)

ax0.scatter(X_0[:, 0], X_0[:, 1], color="m", s=3.0, label="Data points")
# plot circles with radius proportional to the outlier scores
radius_0 = (X_scores_0.max() - X_scores_0) / (X_scores_0.max() - X_scores_0.min())
ax0.scatter(
    X_0[:, 0],
    X_0[:, 1],
    s=1000 * radius_0,
    edgecolors="g",
    facecolors="none",
    label="Outlier scores",
)
ax0.legend(loc="upper left")
ax0.title.set_text("Local Outlier Factor (LOF) for clip-to-skin")
ax1.scatter(X_1[:, 0], X_1[:, 1], color="b", s=3.0, label="Data points")
# plot circles with radius proportional to the outlier scores
radius_1 = (X_scores_1.max() - X_scores_1) / (X_scores_1.max() - X_scores_1.min())
ax1.scatter(
    X_1[:, 0],
    X_1[:, 1],
    s=1000 * radius_1,
    edgecolors="c",
    facecolors="none",
    label="Outlier scores",
)
ax1.legend(loc="upper left")
ax1.title.set_text("Local Outlier Factor (LOF) for clip-to-frame")
#plt.axis("tight")
#plt.xlim((-0.1, 1.5))
#plt.ylim((-0.1, 1.5))
plt.show()
'''




