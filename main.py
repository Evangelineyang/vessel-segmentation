from job.dsa import DsaJob
from job.drive import DriveJob
from job.stare import StareJob
from job.chase import ChaseJob
from imgaug import augmenters as iaa
from itertools import product
from random import sample
import os

if __name__ == '__main__':

    num_searches = 1
    EXPERIMENTS_DIR_PATH = "/home/ubuntu/new_vessel_segmentation/vessel-segmentation/experiments2"

    metrics_epoch_freq = 1
    viz_layer_epoch_freq = 101
    n_epochs = 5

    WRK_DIR_PATH = "/home/ubuntu/new_vessel_segmentation/vessel-segmentation/drive"
    n_splits = 3

    ### RANDOM SEARCH
    tuning_constants = [1.0]
    ss_rs = [.5]
    objective_fns = ["wce"]
    regularizer_argss = [None]
    learning_rate_and_kwargss = [(.01, {})]

    op_fun_and_kwargss = [("adam", {})]
    weight_inits = ["He"]
    act_fns = ["lrelu"]
    act_leak_probs = [0.2]

    hist_eqs = [True,False]

    clahe_kwargss = [None]

    per_image_normalizations = [False]
    gammas = [1.0]

    seqs = [None]
    total_hyper_parameter_combos = list(product(tuning_constants, ss_rs, objective_fns,
                                                regularizer_argss, learning_rate_and_kwargss,
                                                op_fun_and_kwargss, weight_inits, act_fns,
                                                act_leak_probs, hist_eqs, clahe_kwargss,
                                                per_image_normalizations, gammas, seqs))
    cur_hyper_parameter_combos = sample(total_hyper_parameter_combos, num_searches)

    for tuning_constant, ss_r, objective_fn, regularizer_args, learning_rate_and_kwargs, op_fun_and_kwargs, weight_init,\
        act_fn, act_leak_prob, hist_eq, clahe_kwargs, per_image_normalization, gamma, seq in \
            cur_hyper_parameter_combos:

        EXPERIMENT_NAME = str((objective_fn,tuning_constant,ss_r if objective_fn=="ss" else None,regularizer_args,op_fun_and_kwargs,
                               learning_rate_and_kwargs, weight_init, act_fn, act_leak_prob, False if seq is None else True,
                               hist_eq, clahe_kwargs, per_image_normalization,gamma))
        OUTPUTS_DIR_PATH = os.path.join(EXPERIMENTS_DIR_PATH, EXPERIMENT_NAME)

        job = DriveJob(OUTPUTS_DIR_PATH=OUTPUTS_DIR_PATH)
        job.run_cv(WRK_DIR_PATH=WRK_DIR_PATH, mc=True, early_stopping=True, early_stopping_metric="auc",
                   save_model=False, save_sample_test_images=False,
                   metrics_epoch_freq=metrics_epoch_freq, viz_layer_epoch_freq=viz_layer_epoch_freq,
                   n_epochs=n_epochs, n_splits=n_splits, objective_fn=objective_fn,
                   tuning_constant=tuning_constant, ss_r=ss_r,
                   regularizer_args=regularizer_args,
                   op_fun_and_kwargs=op_fun_and_kwargs,
                   learning_rate_and_kwargs=learning_rate_and_kwargs,
                   weight_init=weight_init, act_fn=act_fn, act_leak_prob=act_leak_prob,
                   seq=seq, hist_eq=hist_eq,
                   clahe_kwargs=clahe_kwargs,
                   per_image_normalization=per_image_normalization,
                   gamma=gamma)

