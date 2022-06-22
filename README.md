# VFB Entity Linking Experiment

This repository moved to [https://github.com/VirtualFlyBrain/neuron-to-paper-nlp](https://github.com/VirtualFlyBrain/neuron-to-paper-nlp).

A repository for entity linking experiments in the VFB domain.

Uses [SciSpacy](https://github.com/allenai/scispacy) to train the custom model and run entity linker.  

## Install

Create virtual environment for this project. Then install the following dependencies:

```
pip install scispacy
```

```
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_sm-0.5.0.tar.gz
```

Run `main.py` to test the model with custom sentences. 