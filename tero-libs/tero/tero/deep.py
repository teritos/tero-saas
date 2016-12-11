import configparser
import subprocess
import shlex
import os


def run_detector(image_path, cfg=None):
    predictions = []

    config = configparser.ConfigParser()
    config.read(cfg or os.getenv('DEEPINI'))
    deepnet = config['DEEPNET']
    bin_    = deepnet['DeepNeuralBinary']
    cfg     = deepnet['Cfg']
    data    = deepnet['Data']
    weights = deepnet['Weights']
    os.chdir(deepnet['Chdir'])

    cmd = '{} detector test {} {} {} {}'.format(bin_, data, cfg, weights, image_path)
    cmd = shlex.split(cmd)

    completed_process = subprocess.run(cmd, stdout=subprocess.PIPE)
    data = completed_process.stdout.split(b'\n')

    return data 
