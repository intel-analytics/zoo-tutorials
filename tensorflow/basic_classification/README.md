# Distributted basic classification with Analytics Zoo
## Install Analytics Zoo
To install the Analytics Zoo, please follow [here](https://analytics-zoo.github.io/0.4.0/#PythonUserGuide/install/). We recommend you to install using non-pip method by cloning Analytcis Zoo repo so that you could always use the newest features.

## Setup Analytics Zoo
After installation, please follow [here](https://analytics-zoo.github.io/0.4.0/#PythonUserGuide/run/) to setup the environment.



## Run with jupyter notebook
To run notebook with Analytics Zoo environment, we need to use `dist/bin/jupyter-with-zoo.sh` to start the jupyter notebook kernel.
```shell
chmod +x analytics-zoo/dist/bin/jupyter-with-zoo.sh
analytics-zoo/dist/bin/jupyter-with-zoo.sh
```

## Tips
Here are some tips to resolve some typical problems.
1. Cannot import zoo in python
    + This might be caused by installation without `pip`, then you need to add Analytics Zoo into your `PYTHONPATH` by `export PYTHONPATH=$PYTHONPATH:/path/to/analytics-zoo/pyzoo`
2. For distributted training, evaluation, and prediction, we recommend you to use `tensorflow==1.10.0`.
