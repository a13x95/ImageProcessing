import os
import sys
from urllib import request

from pymongo import MongoClient

if sys.platform.startswith('win'):
    import winreg


def install_windows_mongodb(buffer_size=20480):
    def install():
        print('Downloading MongoDB...')
        mongodb_download_link = 'http://downloads.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-3.6.2-rc0' \
                                '-signed.msi?_ga=2.218738649.1785730929.1515319333-36074608.1515319333 '
        mongodb_exe_url = request.urlopen(mongodb_download_link)
        with open('mongodb.msi', 'wb') as executable:
            data = mongodb_exe_url.read(buffer_size)
            while data:
                executable.write(data)
                data = mongodb_exe_url.read(buffer_size)
        mongodb_exe_url.close()
        print('Installing MongoDB...')
        if not os.path.exists('C:\\data'):
            os.mkdir('C:\\data')
        if not os.path.exists('C:\\data\\db'):
            os.mkdir('C:\\data\\db')
        os.system('mongodb.msi')
        os.remove('mongodb.msi')
        user_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        environment_key_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        environment_key = winreg.OpenKey(user_registry, environment_key_path, 0, winreg.KEY_ALL_ACCESS)
        path_env_var_value = winreg.QueryValueEx(environment_key, 'PATH')[0]
        if path_env_var_value:
            path_env_var_value += 'C:\\Program Files\\MongoDB\\Server\\3.6\\bin;'
        else:
            path_env_var_value = 'C:\\Program Files\\MongoDB\\Server\\3.6\\bin;'
        winreg.SetValueEx(environment_key, 'PATH', 0, winreg.REG_EXPAND_SZ, path_env_var_value)

    def make_mongodb_service():
        if not os.path.exists('C:\\data\\log'):
            os.mkdir('C:\\data\\log')
        with open('mongod.cfg', 'r') as config_file:
            with open('C:\\Program Files\\MongoDB\\Server\\3.6\\mongod.cfg', 'w') as service_config_file:
                service_config_file.write(config_file.read())
        os.system('mongod --config "C:\\Program Files\\MongoDB\\Server\\3.6\\mongod.cfg" --install')
        os.system('sc.exe create MongoDB binPath= "\"C:\Program Files\MongoDB\Server\3.6\bin\mongod.exe\" --service'
                  ' --config=\"C:\Program Files\MongoDB\Server\3.6\mongod.cfg\"" DisplayName= "MongoDB" start= "auto"')
        os.system('net start MongoDB')

    if not os.path.exists('C:\\Program Files\\MongoDB\\Server\\'):
        install()
        make_mongodb_service()
    else:
        print('MongoDB identified')


def install_mongodb():
    print(f'Identified platform: {sys.platform}')
    if sys.platform == 'linux' or sys.platform == 'darwin':
        os.system('bash install_linux_mongodb.sh && . ~/.bashrc')
    elif sys.platform.startswith('win'):
        install_windows_mongodb()


install_mongodb()


class DatabaseConnection:
    """
    Class used to create a database connection that supports operations like insert, delete, update and find.
    """

    def __init__(self, database_name='medicalImagesDb', database_collection='medicalImages'):
        database_client = MongoClient()
        self.db = database_client[database_name]
        self.collection = self.db[database_collection]

    def insert_entry(self, entry_json):
        """
        :param entry_json: a dictionary or a list of dictionaries treated as items to be added to the collection
        :return: A list of errors that occurred while inserting. If there were no problems,
        an empty list will be returned
        """
        insertion_errors = []
        if isinstance(entry_json, list):
            for entry in entry_json:
                if isinstance(entry, dict):
                    insertion_result = self.collection.insert_one(entry)
                    if not insertion_result.acknowledged:
                        insertion_errors += [f'Failed to insert {entry}']
                else:
                    insertion_errors += [f'{entry} is not json formatted']
        elif isinstance(entry_json, dict):
            insertion_result = self.collection.insert_one(entry_json)
            if not insertion_result.acknowledged:
                insertion_errors += [f'Failed to insert {entry_json}']
        else:
            insertion_errors += [f'{entry_json} is not json formatted']
        return insertion_errors

    def delete_entry(self, entry_description_json, multiple_deletions=False):
        """
        :param entry_description_json: a dictionary that specifies the values that the object to be deleted have
        (used for object identification)
        :param multiple_deletions: True if many/all entries that match the description should be deleted,
        False otherwise
        :return: True if successful deleted the entry/entries, False if failed to delete
        """
        if not isinstance(entry_description_json, dict):
            return False
        if entry_description_json == {}:
            multiple_deletions = True
        if multiple_deletions:
            deletion_result = self.collection.delete_many(entry_description_json)
        else:
            deletion_result = self.collection.delete_one(entry_description_json)
        return deletion_result.acknowledged

    def update_entry(self, entry_description_json, entry_updates_json, multiple_updates=False):
        """
        :param entry_description_json: a dictionary that specifies the values that the object to be updated have
        (used for object identification)
        :param entry_updates_json: a dictionary that specifies the new values that the object should have
        :param multiple_updates: True if many/all entries that match the description should be updated, False otherwise
        :return: True if the update was successful, False on failure (if no permissions or no object to update)
        """
        if not isinstance(entry_description_json, dict) or not isinstance(entry_updates_json, dict):
            return None
        entry_update_json = {'$set': entry_updates_json}
        if self.collection.find(entry_description_json).count() == 0:
            return False
        if multiple_updates:
            update_result = self.collection.update_many(entry_description_json, entry_update_json)
        else:
            update_result = self.collection.update_one(entry_description_json, entry_update_json)
        return True if update_result.acknowledged else False

    def get_database_entry(self, entry_description_json, multiple_results=False, results_count=0):
        """
        :param entry_description_json: a dictionary that specifies the values that the object/objects to be found have
        (used for object identification); {} should be the description json if all database objects are wanted
        :param multiple_results: True if multiple results are wanted, False if only one should be found
        :param results_count: Maximum number of results. 0 means all matches from database.
        :return: a list of entries that matched the description, None if error occurred
        """
        if not isinstance(entry_description_json, dict):
            return None
        if multiple_results:
            result = list(self.collection.find(entry_description_json, limit=results_count))
            for entry in result:
                del entry['_id']
            return result
        entry = self.collection.find_one(entry_description_json)
        del entry['_id']
        return [entry]
