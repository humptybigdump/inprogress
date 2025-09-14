from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model, to_categorical

import matplotlib.pyplot as plt

# Hyperparameter des Tensorflow-Modells
batchsize = 100
nclasses  = 10
epochs    = 20
dropout   = 0.2

# MNIST-Datensatz: 60000 (train) + 10000 (test) Bilder (28x28 Pixels, 8 Bits)
datasize  = 28*28
( x_tr, y_tr ), ( x_te, y_te ) = mnist.load_data()


# Zeige eines der Bilder
fig,ax = plt.subplots()
ax.imshow( x_tr[12345] )

# Formatierung der Bilder (28x28) als Vektoren mit 784 Einträgen
x_tr = x_tr.reshape( 60000, datasize )

# Skalierung der 255 Graustufen (8-Bit-Integer) als Float zwischen 0 bis 1
x_tr = x_tr.astype( 'float32' )
x_tr /= 255

# 10 Klassen übersetzt in Matrix 
y_tr = to_categorical( y_tr, nclasses )

# dasselbe für die Testdaten
x_te = x_te.reshape( 10000, datasize )
x_te = x_te.astype( 'float32' )
x_te /= 255
y_te = to_categorical( y_te, nclasses )


# Konstruktion des Modells: Feed-Forward-Netz mit drei verdeckten Lagen
model = Sequential()
model.add( Dense( 100, activation = 'relu', input_shape = ( datasize, ) ) )
model.add( Dense( 100, activation = 'relu' ) )
model.add( Dense( 100, activation = 'relu' ) )
model.add( Dense( nclasses, activation = 'softmax' ) )
model.summary()

model.compile( optimizer = 'adam',
                loss = 'categorical_crossentropy',
                metrics = [ 'accuracy' ] )
                

# Training des Modells
history = model.fit( x_tr, y_tr,
                    epochs = epochs,
                    batch_size = batchsize,
                    verbose = 1,
                    validation_data = ( x_te, y_te ) )

# Grafische Darstellung des Models
plot_model( model, to_file = 'model.png', show_shapes = True )

# Auwwertung des Modells
score = model.evaluate( x_te, y_te, verbose = 0 )
print( "Wert der Verlustfunktion:", score[0] )
print( "Anteil korrekt klassifizierter Bilder (accuracy):", score[1] )