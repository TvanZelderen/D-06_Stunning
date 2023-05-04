import numpy as np
from keras import Sequential
from keras.layers import Input, Dense
from keras.models import Model
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics.pairwise import cosine_distances

def trainning(a, X0, X1, total0, total1, normalized_data0, normalized_data1, threshold0 = -1.6, threshold1 = -1.5):

    abnomal_skin = []
    abnomal_frame = []

    for k in range(a):

        abnomal_skin_tem = []
        abnomal_frame_tem = []

        '''Training the data'''
        original_dim = X0.shape[1]
        encoding_dim = 5

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
        '''
        plt.plot(model_history.history['loss'], label='train')
        plt.plot(model_history.history['val_loss'], label='test')
        plt.legend()
        plt.xlabel("Epochs")
        plt.ylabel("MSE")
        plt.show()
        '''

        encodings = encoder(normalized_data0.values)
        X_0 = encodings.numpy()
        cosine_dist_matrix = cosine_distances(X_0)

        #clustering
        np.random.seed(42)
        clf = LocalOutlierFactor(n_neighbors = 20, contamination = 'auto', metric = 'precomputed')
        y_0 = clf.fit(cosine_dist_matrix)
        X_scores_0 = clf.negative_outlier_factor_

        #report the outliers
        outlier_indice_0 = np.where(X_scores_0 < threshold0)[0]
        for i in range(len(outlier_indice_0)):
            abnomal_skin_tem.append(total0[outlier_indice_0[i]].main_label)

        abnomal_skin.append(abnomal_skin_tem)

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

        #report the outliers
        outlier_indice_1 = np.where(X_scores_1 < threshold1)[0]
        for j in range(len(outlier_indice_1)):
            abnomal_frame_tem.append(total1[outlier_indice_1[j]].main_label)

        abnomal_frame.append(abnomal_frame_tem)

    return abnomal_skin, abnomal_frame