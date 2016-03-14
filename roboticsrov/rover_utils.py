import os
from roboticsrov_exception import RoboticsrovException

def get_data_path(subfolder = None):
    """ Get the data path for the rover, with possibility for a subfolder """

    config_path = os.path.join(os.path.expanduser('~'), '.config', 'rover')

    if (subfolder):
        config_path = os.path.join(config_path, subfolder)

    # If path doesn't exist, create it.
    if (not os.path.isdir(config_path)):
        try:
            os.makedirs(config_path)
        except OSError as e:
            raise RoboticsrovException("Failed to make data path for rover.")

    return config_path
