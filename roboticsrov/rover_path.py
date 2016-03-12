import os

def get_data_path(subfolder, logger):
    """ Get the data path for the rover """

    config_path = os.path.join(os.path.expanduser('~'), '.config', 'rover')

    if (subfolder):
        config_path = os.path.join(config_path, subfolder)

    # If path doesn't exist, create it.
    if (not os.path.isdir(config_path)):
        try:
            os.makedirs(config_path)
            logger.send(["info","Created path at {0}".format(config_path)])
        except OSError as e:
            logger.send(["err", "Error creating path at {0}: {1}".format(config_path, e.message)])

    return config_path
