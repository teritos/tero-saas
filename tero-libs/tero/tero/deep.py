import configparser
import subprocess
import shlex
import os


def run_detector(image_path, cfg):
    predictions = []

    config = configparser.ConfigParser()
    config.read(cfg)
    deepnet = config['DEEPNET']
    bin_    = deepnet['DeepNeuralBinary']
    cfg     = deepnet['Cfg']
    data    = deepnet['Data']
    weights = deepnet['Weights']

    cmd = '{} detector test {} {} {} {}'.format(bin_, data, cfg, weights, image_path)
    cmd = shlex.split(cmd)

    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE)
    data = completed_process.stdout.split(b'\n')

    pcount, psize = data.split('H%23')[-1].split()
    import ipdb; ipdb.set_trace()

    return predictions 
