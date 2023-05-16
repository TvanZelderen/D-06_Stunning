import numpy as np
from keras import Sequential
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import Adam
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics.pairwise import cosine_distances
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def Model_r(X, nor_data, dim:int, learning_rate: 0.001):
    original_dim = X.shape[1]
    encoding_dim = dim

    encoder = Sequential(
    [
    Dense(80, name = '1st_hidden_layer', input_shape = (original_dim,), activation='relu'),
    Dense(32, name = '2nd_hidden_layer', input_shape = (80, ), activation='relu'),
    Dense(encoding_dim, name = 'encoding_Layer', activation='linear')
    ]
    )

    decoder = Sequential(
        [
        Dense(32, name = '4th_hidden_layer', input_shape = (encoding_dim,), activation='relu'),
        Dense(80, name = '5th_hidden_layer', input_shape = (32, ), activation='relu'),
        Dense(original_dim, name = 'output_layer', activation='sigmoid')
        ]
    )
    # Autoencoder
    encoder_decoder_model = Model(
        inputs = encoder.inputs,
        outputs = decoder(encoder.outputs)
    )

    encoder_decoder_model.compile(loss = 'mse', optimizer = Adam(lr=learning_rate))
    
    train_data, test_data = train_test_split(nor_data, test_size=0.3, random_state=42)

    #training model
    model_train_history = encoder_decoder_model.fit(
        x = train_data,
        y = train_data,
        epochs = 40,
        batch_size = 32,
        validation_data = (test_data, test_data)
    )
    # Use your model to encode the test data
    '''
    plt.plot(model_train_history.history['loss'], label='train')
    plt.plot(model_train_history.history['val_loss'], label='test')
    plt.legend()
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.show()'''
    
    return encoder_decoder_model



def LOF(a, X0, X1, total0, total1, normalized_data0, normalized_data1, threshold0 = -1.6, threshold1 = -1.5):

    abnomal_skin = []
    abnomal_frame = []
    scores_0 = 0
    scores_1 = 0
    
    for k in range(a):

        '''Training the data'''
        model0 = Model_r(X0, normalized_data0, dim = 5, learning_rate=0.0005)
        

        X_0 = model0.predict(normalized_data0.values)
        cosine_dist_matrix = cosine_distances(X_0)

        #clustering
        np.random.seed(42)
        clf = LocalOutlierFactor(n_neighbors = 20, contamination = 'auto', metric = 'precomputed')
        y_0 = clf.fit(cosine_dist_matrix)
        X_scores_0 = clf.negative_outlier_factor_

        #report the outliers
        outlier_indice_0 = np.where(X_scores_0 < threshold0)[0]
        for i in range(len(outlier_indice_0)):
            abnomal_skin.append(total0[outlier_indice_0[i]].main_label)

        model1 = Model_r(X1, normalized_data1, dim = 4, learning_rate=0.0009)

        X_1 = model1.predict(normalized_data1.values)
        cosine_dist_matrix = cosine_distances(X_1)

        #clustering
        np.random.seed(42)
        clf = LocalOutlierFactor(n_neighbors = 20, contamination = 'auto', metric = 'precomputed')
        y_1 = clf.fit(cosine_dist_matrix)
        X_scores_1 = clf.negative_outlier_factor_

        #report the outliers
        outlier_indice_1 = np.where(X_scores_1 < threshold1)[0]
        for j in range(len(outlier_indice_1)):
            abnomal_frame.append(total1[outlier_indice_1[j]].main_label)

        scores_0 += X_scores_0
        scores_1 += X_scores_1
    
    scores_0 = scores_0/a
    scores_1 = scores_1/a
    
    return abnomal_skin, abnomal_frame, X_0, scores_0, X_1, scores_1, outlier_indice_0, outlier_indice_1