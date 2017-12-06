import csv
import errno
import os
def ensure_directory_exists(base_directory):
    """
    Makes a directory if it does not exist
    """
    try:
        os.makedirs(base_directory)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise ex

def load_dqn_weights_if_exist(dqns, weights_filename_prefix, weights_filename_extension=".h5"):
    """
    Loads weights if they exist, otherwise does nothing
    """
    for i, dqn in enumerate(dqns):
        # TODO should not work if only some weights available?
        dqn_filename = weights_filename_prefix + str(i) + weights_filename_extension
        if os.path.isfile(dqn_filename):
            print("Found old weights to use for agent {}".format(i))
            dqn.load(dqn_filename)

def save_dqn_weights(dqns, weights_filename_prefix, weights_filename_extension=".h5"):
    """
    Saves weights
    """
    ensure_directory_exists(os.path.splitext(weights_filename_prefix)[0])
    for i, dqn in enumerate(dqns):
        dqn_filename = weights_filename_prefix + str(i) + weights_filename_extension
        dqn.save(dqn_filename)

class Time_Series_Statistics_Store(object):
    """
    Logs time series data.
    Header should represent every column in data.
    For example:
        epoch | loss
        0     | 1
        1     | 0.5
        2     | 0.3
    """
    def __init__(self, header):
        self.statistics = []
        self.header = header
    def add_statistics(self, data):
        if len(data) != len(self.header):
            raise ValueError("Data length does not match header")
        self.statistics.append(data)
    def dump(self, dump_filename="statistics.csv"):
        ensure_directory_exists(os.path.splitext(dump_filename)[0])
        with open(dump_filename, "w") as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(self.header)
            for stat in self.statistics:
                wr.writerow(stat)
