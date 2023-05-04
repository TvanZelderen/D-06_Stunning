from Autoencoder import LOF
from Dataspecific import Data, standard
from load import *
import matplotlib.pyplot as plt

#clip_to_skin
total0 = iterate_points(type = 0)
X0 = Data(total0)
normalized_data0 = standard(X0)

#clip_to_frame
total1 = iterate_points(type = 1)
X1 = Data(total1)
normalized_data1 = standard(X1)

abnomal_skin, abnomal_frame, X_0, X_scores_0, X_1, X_scores_1, outlier_indice_0, outlier_indice_1 = LOF(a, X0, X1, total0, total1, normalized_data0, normalized_data1)

for i in total0:
    