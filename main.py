from job.dsa import DsaJob
from job.drive import DriveJob
from job.stare import StareJob
from job.chase import ChaseJob
from imgaug import augmenters as iaa

import os

if __name__ == '__main__':

    EXPERIMENTS_DIR_PATH = "/home/ubuntu/new_vessel_segmentation/vessel-segmentation/experiments"
    EXPERIMENT_NAME = "drive_example"

    arg_index = 1
    objective_fn, tuning_constant, ss_r, regularizer_args, learning_rate_and_kwargs, op_fun_and_kwargs, weight_init, act_fn, hist_eq,clahe_kwargs,per_image_normalization,gamma,seq = zip(["wce","gdice", "ss"], [1.0,1.0,1.0], [.05,.05,.05], [None, ("L1",.01),("L2",.01)], [(.001, {}), (.001, {}),(.01, {'decay_steps': 1, 'decay_rate': .1})], [("adam",{}),("rmsprop",{}),("adadelta",{})], ["He", "Xnormal", "default"], ["lrelu", "relu", "relu"], [False, False, True], [None, {"clipLimit": 2.0, "tileGridSize": (8, 8)}, {"clipLimit": 2.0, "tileGridSize": (8, 8)}], [False, True, True], [None, 1.0, 5.0], [None, None, iaa.Sequential([iaa.Crop(px=(0, 16)), iaa.Fliplr(0.5),iaa.GaussianBlur(sigma=(0, 3.0))])])[1]
    job = DriveJob(OUTPUTS_DIR_PATH=os.path.join(EXPERIMENTS_DIR_PATH, EXPERIMENT_NAME))
    job.run_cross_validation(WRK_DIR_PATH="/home/ubuntu/new_vessel_segmentation/vessel-segmentation/drive",
                             metrics_epoch_freq=1,viz_layer_epoch_freq=1,
                             n_epochs=2,n_splits=2,objective_fn=objective_fn,
                             tuning_constant=tuning_constant, ss_r=ss_r,
                             regularizer_args=regularizer_args,
                             op_fun_and_kwargs=op_fun_and_kwargs,
                             weight_init=weight_init, act_fn=act_fn,
                             seq=seq, hist_eq=hist_eq,
                             clahe_kwargs=clahe_kwargs,
                             per_image_normalization=per_image_normalization,
                             gamma=gamma)

