# Tutorials for running distribued Keras (v1.2.2) on Analytics Zoo
Tutorials for running _**distribued Keras (v1.2.2) on Analytics Zoo**_. These tutorials are ported from François Chollet's [Jupyter notebooks](https://github.com/fchollet/deep-learning-with-python-notebooks) for the book [Deep Learning with Python (Manning Publications)](https://www.manning.com/books/deep-learning-with-python?a_aid=keras&a_bid=76564dff)

This repository is built to describe how to write Keras-style code and directly run it in analytics-zoo so that we could run the original Keras code in distributed mode via limited modification. We make this repository based on notebook https://github.com/fchollet/deep-learning-with-python-notebooks#companion-jupyter-notebooks-for-the-book-deep-learning-with-python, which is the sample code repository of book "Deep Learning with Python" based on Keras 2.0.8 and we pick some basic chapters from it. 

Currently analytics-zoo builds its Keras-style code based on Keras 1.2.2. Thus, this repository contains the code of implementation of original Keras 2.0.8 code based on Keras 1.2.2, and how to modify the code in order to run it in analytics-zoo.

To make it simple, we omit the description of plenty concepts here and you could find them in original notebook above [(link)](https://github.com/fchollet/deep-learning-with-python-notebooks#companion-jupyter-notebooks-for-the-book-deep-learning-with-python). Besides, we directly post Keras 1.2.2 code here and the replacements needed from Keras 2.0.8 to Keras 1.2.2 are noted in `Keras_2-to-1.md`.

This repository use Python 3.5, Analytics Zoo 0.4.0 (zoo code). We post the summary of Keras-to-zoo code convertion as well as the table of contents.

## First of all
Make sure you have analytics-zoo installed, see install guide [here](https://analytics-zoo.github.io/master/#PythonUserGuide/install/). Then set the environment variables like following
  
    PYSPARK_PYTHON=/path_to_your_python
    PYSPARK_DRIVER_PYTHON=/path_to_your_python
    # To avoid version conflict, in my ubuntu, this path is /usr/bin/python3.5

    SPARK_DRIVER_MEMORY=4g
    # If you encounter heap space exception, you could simply increase this variable to 8g, 16g, etc. 
    # If no more memory is available on your machine, you could consider reduce the data size.

Then, make sure you have following code at the beginning of your zoo code.
  
    from zoo.common.nncontext import *
    sc = init_nncontext(init_spark_conf().setMaster("local[4]"))
    
we set core number to 4 above, you can also set it with another number. But we still recommend 4 because analytics-zoo need the core number could divide the batch size of learning, which is normal set as powers of 4, e.g. 16, 32, 128. Error would be raised if this requirement is not satisfied.

## Summary of Keras-to-zoo code convertion
This section is written for user who has experience on Keras.

For previous Keras user, we hope them can get start with Analytics Zoo in a short time. In Keras API of Analytics Zoo, most of the code writing is just as Keras 1.2.2 so that you can run your Keras code just based on just few modifications. We summarize the modifications need to make here, attached with the link to the example code chapter.

#### Accuracy checkout
Currently in analytics-zoo, `fit` method does not have any return. Results can only be checked via tensorboard, see [Chapter 3.5]()

#### Predict result
The return of `predict` method is RDD, so you need to call `collect` method to collect them, see [Chapter 3.5]()

#### Parameters not supported
Analytics-zoo does not support following parameters currently

* verbose: to control the console output. In Analytics Zoo, there is no need to set this parameter. Training log would be outputed in INFO message.

## Table of contents

The main purpose of this repository is to decribe the convertion from Keras to analytics-zoo so that we rename the notebooks to make it more experienced-user oriented. We keep the chapter index so you could still make a reference to the original notebook [here](https://github.com/fchollet/deep-learning-with-python-notebooks#companion-jupyter-notebooks-for-the-book-deep-learning-with-python). We only keep some key description of the original notebook.

* Chapter 2:
    * [2.1: A first look at a neural network]()
* Chapter 3:
    * [3.5: Classifying movie reviews]()
    * [3.6: Classifying newswires]()
    * [3.7: Predicting house prices]()
* Chapter 4:
    * [4.4: Underfitting and overfitting]()
* Chapter 5:
    * [5.1: Introduction to convnets]()
* Chapter 6:
    * [6.2: Understanding RNNs]()

    
