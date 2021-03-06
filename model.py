import tensorflow as tf
import numpy as np
class Model(object):
    def __init__(self):
        pass
    def construct(self,image_size,num_characters):
        ''' This method constructs the model based on the parametrs based '''

        #paraemeters for image and labels creation
        self.image_size=image_size
        self.num_characters=num_characters


        # placehoders
        self.image=tf.placeholder(dtype=tf.float32,shape=[None,self.image_size*self.image_size],name="self.image_input")
        self.label=tf.placeholder(dtype=tf.float32,shape=[None,num_characters])

        input_layer=tf.reshape(self.image,[-1,100,100,1])

        conv1=tf.layers.conv2d(input_layer,filters=4,kernel_size=[5,5],padding='same')
        pool1=tf.layers.max_pooling2d(conv1,pool_size=[2,2],strides=5)

        conv2=tf.layers.conv2d(pool1,filters=8,kernel_size=[5,5],padding='same')
        pool2=tf.layers.max_pooling2d(conv2,pool_size=[2,2],strides=2)

        pool2_flat=tf.reshape(pool2,[-1,10*10*8])
        dropout=tf.nn.dropout(pool2_flat,0.2)

        dense=tf.layers.dense(dropout,units=num_characters,activation=tf.nn.relu)

        print(self.image)
        print(self.label)
        print(conv1)
        print(pool1)
        print(conv2)
        print(pool2)
        print(pool2_flat)
        print(dropout)
        print(dense)




        self.logits=tf.nn.softmax(dense)
        self.predictions=tf.arg_max(self.logits,1)
        self.loss=tf.reduce_sum(tf.losses.log_loss(labels=self.label,predictions=self.logits))

        self.accuracy=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(self.label,1),tf.argmax(self.logits,1)),tf.float32))
        self.learning_rate=0.5

        self.optimizer=tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.loss)
        self.sess=tf.InteractiveSession()
        tf.global_variables_initializer().run()
        tf.local_variables_initializer().run()

    def train(self,images,labels):
        ''' This method trains the model that is constructed using the cosntruct method'''

        _,l,acc=self.sess.run([self.optimizer,self.loss,self.accuracy],feed_dict={self.image:images,self.label:labels})
        acc*=100
        l*=100
        print("Loss {} Accuaracy {}".format(l,acc))
        return l,acc

    def test(self,images,labels):
        ''' This method test the trained model using passed data'''
        l,acc=self.sess.run([self.loss,self.accuracy],feed_dict={self.image:images,self.label:labels})
        acc*=100
        l*=100
        print(" Accuaracy {}".format(acc))
        return l,acc

    def predict(self,images):
        '''prediction method'''
        p=self.sess.run([self.predictions],feed_dict={self.image:images})
        return p

    def save(self):
        saver=tf.train.Saver()
        saver.save(sess,"Model_Dump.ckpt")
        print("Model Stored in Disk")
        return

    def restore(self):
        saver=tf.train.Saver()
        saver.restore(sess,"Model_Dump.ckpt")
        print("Model Restored")
        return
