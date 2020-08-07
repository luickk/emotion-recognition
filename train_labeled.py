import keras
import random
from keras.layers import *
from keras.models import Model
from keras.regularizers import l2
from keras.optimizers import Adam
from cnn_model.models import *
from utils.data import *
import calendar
import time

def main():
    epochs = 50
    batchSize = 32
    VALTrainingFactor = 0.7
    learningRate=0.00001
    dataSetDir = 'data/MPI_large_centralcam_hi_islf_complete/**'
    files='data/labeled/**'

    classes = getClassesForDataSet(dataSetDir)

    cnnIn, cnnOutLayer = basicCNNModel((256, 256, 3), len(classes))
    mplIn, mplOutLayer = mplModel((68, 2), len(classes))

    midModel = multipleInputDataModel(mplOutLayer, cnnOutLayer, mplIn, cnnIn, len(classes))
    midModel.compile(loss="mean_absolute_percentage_error", optimizer=Adam(lr=1e-3, decay=1e-3 / 200))

    print('training model with mixed input on labeled data ')
    randomId = str(random.randrange(500))
    print('Model Id: ' + randomId)

    tbCallBack = keras.callbacks.TensorBoard(log_dir='data/tensorBoard/labeled_training_tb_'+str(learningRate)+'_'+randomId, histogram_freq=0, write_graph=True, write_images=True)

    data_gen = generateMixedInputDataBatches(files, batchSize, VALTrainingFactor)

    val_data_gen = generateMixedInputValDataBatches(files, batchSize, VALTrainingFactor)

    train_batch_count, val_batch_count = getDataMetric(files, batchSize, VALTrainingFactor)

    print('train_batch_count, val_batch_count: ', train_batch_count,', ', val_batch_count)

    midModel.fit(data_gen, validation_data=val_data_gen, validation_steps=val_batch_count, steps_per_epoch=train_batch_count, epochs=epochs, verbose=1, callbacks=[tbCallBack])
    midModel.save_weights('data/trainedModels/train_labeled_weights_'+randomId+'.h5')


if __name__ == "__main__":
    main()
