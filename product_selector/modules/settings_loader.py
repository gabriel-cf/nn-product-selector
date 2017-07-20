import os
import json

def _get_dic_from_json(jsonFile):
    """ Returns the settings file as a dictionary
    """
    with open(jsonFile) as data_file:
        dic = json.load(data_file)
    return dic

class SettingsLoader(object):
    """ """
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(ROOT_DIR, 'config.json')
    CONFIG_DIC = _get_dic_from_json(CONFIG_FILE)

    @staticmethod
    def _loadPath(relativePath):
        """ Returns the path specified in the configuration dictionary
            if and only if it is a valid path
        """
        path = os.path.join(SettingsLoader.ROOT_DIR, relativePath)
        if not os.path.exists(path):
            raise ValueError("For file '%s' the retrieved path '%s' was not valid" % (fileName, path))
        return path

    @staticmethod
    def _raiseOnInvalidSetting(key):
        if not key in SettingsLoader.CONFIG_DIC:
            raise ValueError("The setting '%s' does not match any known one", key)

    @staticmethod
    def getPath(key):
        SettingsLoader._raiseOnInvalidSetting(key)
        return SettingsLoader._loadPath(SettingsLoader.CONFIG_DIC[key])

    @staticmethod
    def getValue(key):
        SettingsLoader._raiseOnInvalidSetting(key)
        return SettingsLoader.CONFIG_DIC[key]
