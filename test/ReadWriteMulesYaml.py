# imported libraries
import os
import re
# from lib.box_message import BoxMessage
from datetime import datetime


class ReadWriteMulesYaml:
    def __init__(self, yaml_file, api_name, project_suffix=None):
        """
        Class to read the yaml file input and put it into a complicated dictionary structure to allow manipulation of
        the fields.

        :param yaml_file: the name of the yaml file to read to extract the keys from.
        :param api_name: the name of the api this key file is created for.
        :param project_suffix: a suffix to append to the mules API to allow deployment of the same API to the same
                               environment with different options.
        """
        self._api_name = api_name
        self._project_suffix = project_suffix
        self._regex_key = re.compile(r"([\-_ a-zA-Z0-9\.]*):")
        self._regex_key_value = re.compile(r"([\-_ a-zA-Z0-9\.]*): *(\".*\")")
        self._regex_key_file = re.compile(r"([:\-_ a-zA-Z0-9\.]*) *(\".*\")")
        self._archived_yaml_file = ''
        self._yaml_keys = []
        self._yaml_dict = {}
        self._space_dict = {}
        self._env_dict = {}
        self._error_code = 0
        self._errors = {}
        self._key_len = 0
        self._key_list = []
        self._key_file_name = ''
        self._key_file_created = False
        self._new_keys = []
        self._new_dict = {}
        self._last_code = 0
        self._number_leading_spaces = 0
        self._jenkins_secrets = '/var/lib/jenkins/secrets'

        if project_suffix:
            print("Using project suffix of '{}'".format(project_suffix))
            self._jenkins_secrets = os.path.join(self._jenkins_secrets, project_suffix)

        self._yaml_file = self._check_file_exists('a.yml')

    def _archive_existing_key_file(self, environment):
        """
        This will rename the existing key file and create a new one.

        :param environment: the environment to supply when creating a new key file.
        :return: None
        """
        old_file = self._jenkins_secrets + "/" + self._api_name + "." + environment
        now = datetime.now()
        new_filename = "{name}.{yy:04}-{mm:02}-{dd:02}_{h:02}:{m:02}:{s:02}".format(
            name=old_file, yy=now.year, mm=now.month, dd=now.day, h=now.hour, m=now.minute, s=now.second)
        try:
            os.rename(old_file, new_filename)
        except IOError as e:
            self.errors = "6:Cannot rename file {} to {}. Error = {}".format(old_file, new_filename, e)
        else:
            self._archived_yaml_file = os.path.basename(new_filename)
            self.build_key_file(environment)

    def _build_key(self, spaces, new_key):
        """
        Checks through dictionary of spaces by key to determine level of this space and ensure yaml fields line up.

        :param spaces: number of spaces in front of the new key found.
        :param new_key: name of the new key found
        :return: key in format 'key:key1:key2' etc.
        """
        updated_space_dict = {}
        created_key = ''
        largest_spaces_found = -1
        largest_key_found = ''

        if spaces == 0:
            # reset key
            self._key_list = []
            self._key_list.append(new_key)
            updated_space_dict[new_key] = 0
            created_key = new_key
        else:
            for key in self._space_dict:
                if largest_spaces_found < self._space_dict[key]:
                    largest_spaces_found = self._space_dict[key]
                    largest_key_found = key

                if self._space_dict[key] == spaces:
                    # match update the key list
                    created_key = self._set_new_key(key=key, new_key=new_key, replace=True)
                    updated_space_dict[created_key] = spaces

                elif spaces < self._space_dict[key]:
                    # spaces value is less than the value in spaces_dict[key] so not adding to updated_dictionary
                    continue
                else:
                    updated_space_dict[key] = self._space_dict[key]

            if largest_spaces_found < spaces:
                created_key = self._set_new_key(key=largest_key_found, new_key=new_key)
                updated_space_dict[created_key] = spaces

        self._space_dict = updated_space_dict.copy()

        return created_key

    def build_key_file(self, environment='uat'):
        """
        This takes the output read from the dev.yml file and creates the key file which can be updated to reflect the
        other key details. If the key file already exists it will compare the dev.yaml keys with the previous one. If
        there are new keys it will archive the old one. The details of the archive created are printed and the list of
        different keys can be viewed with the method print_new_keys.
        The name of the key file created will be the api number (extracted from the dev.yml file) and the environment
        name. eg: 123565.uat or 123345.prod
        This file will be created in the secrets folder for jenkins.

        :param environment: the name of the environment type to create the key file for.
                            Allowed variables are test, uat or prod
        :return: None
        """
        self._key_file_name = "{}.{}".format(self._api_name, environment)

        file_exits, filename = self._validate_environment(environment)

        key = ''

        if not file_exits:
            try:
                with open(filename, 'w') as fn:
                    for key in self._yaml_keys:
                        if key in self._yaml_dict and len(self._yaml_dict[key]) > 2 and self._yaml_dict[key][2]:
                            fn.write("{} {}\n".format(key, self.get_value_to_write(key)))

            except KeyError:
                self.errors = '7:cannot write key {} from dictionary. Key does not exist'.format(key)

            except IOError as e:
                self.errors = '7:IO error writing to key file {}. {}'.format(filename, e)
            else:
                self._key_file_created = True
        else:
            # read the existing file and compare the dictionary keys - if keys are the same then report nothing to do.
            self._check_current_key_file(filename)

            # otherwise archive the existing file and create a new one.
            if len(self._new_keys) > 0:
                self._archive_existing_key_file(environment)

    def _check_current_key_file(self, filename):
        """
        This will read the key file supplied and check the keys found with the existing dictionary of keys extracted
        from the dev.yaml file.
        If the keys are the same then this file is already up to date. If there are new or missing keys then flag with
        a message.

        :param filename: The name of the key file that it was supposed to create.
        :return: List of new keys found
        """
        self.read_yaml_file(filename=filename)
        self._new_keys = []

        for key, value in self._yaml_dict.items():
            if value[2] != '' and key not in self._new_dict:
                self.new_keys = key

    def _check_file_exists(self, filename):
        """
        This will check the file exists. If it does it will return the file name otherwise it will set an error.

        :param filename: Name of the file to check
        :return: Name of file found or None if no file
        """
        if os.path.exists(filename):
            if os.path.isfile(filename):
                return filename
            else:
                self.errors = '1:the file {} provided is not a real file'.format(filename)
        else:
            self.errors = '1:the filename {} provided does not exist'.format(filename)

        return None

    @property
    def error_code(self):
        """
        Only the largest error code number is stored here and can be retrieved for ease of reporting.

        :return: the largest error code
        """
        return self._error_code

    @error_code.setter
    def error_code(self, code):
        """
        Set the error code to the largest number found

        :param code: the error code number
        :return: the integer version of the code supplied or
        """
        try:
            code_num = int(code)
        except ValueError:
            print("Code {} supplied is not an integer".format(code))
        else:
            self._last_code = code_num

            if self._error_code < code_num:
                self._error_code = code_num

    @property
    def errors(self):
        """
        :return: the list of errors found
        """
        return self._errors

    @errors.setter
    def errors(self, message):
        """
        Keeps a record of the errors detected when reading the release details

        :param message: the error number:the error message
        :return: None
        """
        self.error_code = message[:1]
        try:
            self.errors[self._last_code] + "\nERROR: " + message[2:]
        except KeyError:
            self.errors[self._last_code] = "ERROR: " + message[2:]

    @property
    def new_keys(self) -> list:
        """
        This will return the list of new keys detected

        :return: list of new keys
        """
        return self._new_keys

    @new_keys.setter
    def new_keys(self, key):
        """
        This will take the key supplied and append it to the list of new keys and update the number found.

        :param key: the key to add to the list
        :return: None
        """
        self._new_keys.append(key)

    @property
    def number_of_new_keys(self):
        """
        This will return the number of keys in the list _new_keys

        :return: number of new keys
        """
        return len(self._new_keys)

    def get_key_value(self, input_string):
        """
        Takes the string input and extracts the name of the key (value before the :) and the attribute value
        (value after the :). Note in some cases there will not be an attribute value.

        :param input_string: the string to examine
        :return: tuple(key, value)
        """
        key = value = ''
        if self._regex_key_value.match(input_string):
            matching = self._regex_key_value.match(input_string).groups()
            key = matching[0].lstrip().rstrip()
            value = matching[1].lstrip().rstrip()

        elif self._regex_key.match(input_string):
            matching = self._regex_key.match(input_string)
            key = matching.group(1).lstrip().rstrip()

        return key, value

    @staticmethod
    def get_number_leading_spaces(input_string):
        """
        Takes a line and returns the number of leading spaces

        :param input_string: the string with 0 or more leading spaces
        :return: the number of leading spaces
        """
        try:
            return len(input_string) - len(input_string.lstrip(' '))
        except AttributeError:
            return 0

    def get_value_to_write(self, key):
        """
        This will return the key value to write to the key file. If the key exists in self._new_dict then it will use
        this value otherwise it will use the value in the self._yaml_dict

        :param key: the key to extract from the dictionary
        :return: the value to write to the file
        """
        value = ''
        if key in self._new_dict:
            value = self._new_dict[key]
        elif key in self._yaml_dict and len(self._yaml_dict[key]) > 2 and self._yaml_dict[key][2]:
            value = self._yaml_dict[key][2]

        return value

    def _parse_key_file(self, lines, file_name):
        """
        Run through the existing key file and extract the details to see if they match the new keys supplied.

        :param lines: lines read from existing key file.
        :param file_name: name of key file being validated.
        :return: dictionary of keys and their values read from existing yaml file
        """
        mydict = {}

        for line_read in lines:
            line = line_read.rstrip()

            if line == '':
                continue

            if self._regex_key_file.match(line):
                matching = self._regex_key_file.match(line).groups()
                key = matching[0].lstrip().rstrip()
                value = matching[1].lstrip().rstrip()
                mydict[key] = value
                self.new_keys = key
            else:
                self.errors = "8:Line '{}' in keyfile {} is not in format 'key':'value'".format(line, file_name)

        return mydict

    def _parse_yaml_file(self, lines):
        """
        Runs through the list of lines read from the yaml file and builds the internal dictionary.

        :param lines: list of lines read.
        :return: dictionary of key and values in yaml file
        """
        regex = re.compile(r" *#")
        mydict = {}

        for line_read in lines:
            line = line_read.rstrip()
            if regex.match(line) or len(line) == 0:
                continue
            else:
                leading_spaces = self.get_number_leading_spaces(input_string=line)
                new_key, value = self.get_key_value(input_string=line)

                key = self._build_key(leading_spaces, new_key)

                if key is not None:
                    spaces = len(self._key_list) - 1
                    mydict[key] = [spaces, new_key, value]
                    self._yaml_keys.append(key)

        return mydict

    def print_new_keys(self):
        """
        This will check if there are any new keys in the yaml file. If there are it will return the number of
        keys found and print a list of them.

        :return: number of new keys or 0 if no new keys
        """
        message = []
        key_details = [" "]
        if self._key_file_created:
            if self._project_suffix:
                key_details.append("New key file created is: {}/{}".format(self._project_suffix, self._key_file_name))
            else:
                key_details.append("New key file created is: {}".format(self._key_file_name))

            key_details.append("Please review and update as new values will be copied from dev.yaml")
        else:
            key_details.append("Existing key file used: {}".format(self._key_file_name))

        if self.number_of_new_keys > 0:
            message.append("There were {} new keys detected when checking the yaml file:  {}:".format(
                self.number_of_new_keys, self._yaml_file))
            message.append("The list of new keys are:")

            for key in sorted(self._new_keys):
                message.append(key)

            message.append("Old key file has been archived to {}".format(self._archived_yaml_file))
        elif not self._key_file_created:
            message.append("No new keys detected in yaml file: {}".format(self._yaml_file))

        message += key_details
        # bm = BoxMessage(message=message, max_line_len=80)
        # bm.print_box()

        return self.number_of_new_keys

    def read_key_file_and_write_yaml(self, environment):
        """
        This will read the key file for the supplied environment based upon the api:id in the dictionary. It
        will then use the lines read to create a dictionary of key:values to be used to replace the existing
        dictionary values already read.

        :param environment: the environment name to read the key file from (test, uat or prod)
        :return: None
        """
        self._key_file_name = "{}.{}".format(self._api_name, environment)

        file_exists, filename = self._validate_environment(name=environment)

        if file_exists:
            try:
                with open(filename) as fn:
                    lines = fn.readlines()
                    self._env_dict = self._parse_key_file(lines, filename)
            except IOError as e:
                self.errors = '9:Could not read the keys file {}. {}'.format(filename, e)
            else:
                self._write_new_environment_file(environment=environment)
        else:
            self.errors = '9:No such key file {}'.format(filename)

    def read_yaml_file(self, filename=None):
        """
        This reads the yaml file supplied and extracts it into the internal dictionary.

        :param filename: the name of the yaml file to be read or the one stored internally if none provided.
        :return: None
        """
        if filename is None:
            file_to_read = self._yaml_file
        else:
            file_to_read = filename

        lines_read = []

        try:
            with open(file_to_read) as yf:
                for line in yf:
                    line = line.rstrip()

                    if self._regex_key.match(line) or self._regex_key_file.match(line):
                        lines_read.append(line)

        except IOError as e:
            self.errors = '2:cannot read content of {}. {}'.format(file_to_read, e)
        else:
            if len(self._yaml_dict) == 0:
                self._yaml_dict = self._parse_yaml_file(lines=lines_read)
            else:
                self._new_dict = self._parse_key_file(lines=lines_read, file_name=file_to_read)

    def _set_new_key(self, key, new_key, replace=False):
        """
        Updates the internal key list with the new key.

        :param key: key joined by : to be updated (same format as return value)
        :param new_key: new key to add or replace existing key
        :param replace: True = replace last entry with new key. False = append new key to list of keys
        :return: list of keys joined by : e.g. 'key:key1:key2'
        """
        #  self.errors = '4:New key detected {}'.format(new_key)
        self._key_list = key.split(':')

        if replace:
            self._key_list.pop()

        self._key_list.append(new_key)

        return ":".join(self._key_list)

    def _validate_environment(self, name):
        """
        This will ensure the environment name is an acceptable one and the file name that would be created does not
        exist.

        :param name: name of the environment
        :return: False (file does not exist) True (file exists),full path to new filename
        """
        file_exists = False
        filename = None

        if name.lower() == 'test' or name.lower() == 'uat' or name.lower() == 'prod':
            try:
                filename = '{}/{}.{}'.format(self._jenkins_secrets, self._api_name, name.lower())
                filename = filename.replace('"', '')
                if os.path.exists(filename):
                    file_exists = 1

            except KeyError:
                self.errors = '4:No key api:id found in yaml dictionary'

            except AttributeError:
                self.errors = '5:Environment name {} is not a string'.format(name)
        else:
            self.errors = '5:Environment name {} is invalid to build the key file. Expect test or uat or prod'.format(
                name)

        return file_exists, filename

    def _write_new_environment_file(self, environment):
        """
        This will update the dictionary read then create the new environment file (test.yaml, uat.yaml or prod.yaml) with the
        updated keys from the key file read.

        :param environment: the name of the environment file to build (test, uat or prod).yaml
        :return: None
        """
        self._new_keys = []

        for key in self._env_dict:
            # ensure existing keys updated with current key values
            if key in self._yaml_dict and len(self._yaml_dict[key]) > 2:
                self._yaml_dict[key][2] = self._env_dict[key]

        for key in self._yaml_dict:
            # check for new keys
            if self._yaml_dict[key][2] != '' and key not in self._env_dict:
                self.new_keys = key

        if self.number_of_new_keys > 0:
            self._archive_existing_key_file(environment)
            self.errors = "6:New key detected in the dev.yaml file. Aborting build of environment file until resolved."

        filepath_len = len(self._yaml_file) - 8
        new_filename = "{}{}.yaml".format(self._yaml_file[:filepath_len], environment)
        self._write_yaml_file(new_filename)

    def _write_yaml_file(self, output_filename):
        """
        This will create a yaml file from the dictionary and list of keys read. It should produce one in exactly the
        same format - but allows the values to be changed for different environments.

        :param output_filename: the name of the file to be created.

        :return: None
        """
        try:
            with open(output_filename, 'w') as out:
                for key in self._yaml_keys:
                    if key in self._yaml_dict and len(self._yaml_dict[key]) == 3:
                        num_spaces = self._yaml_dict[key][0] * 2
                        yaml_key = self._yaml_dict[key][1]
                        value = self._yaml_dict[key][2]

                        if num_spaces == 0:
                            line = "{}: {}".format(yaml_key, value)
                        elif num_spaces > 0:
                            line = "{}{}: {}".format(' ' * num_spaces, yaml_key, value)
                        else:
                            self.errors = '3:No number of spaces value in dictionary for key {}'.format(key)
                            line = ''
                    else:
                        self.errors = '4:No value in dictionary for key {}'.format(key)
                        line = ''

                    if len(line) > 0:
                        line = "{}\n".format(line.rstrip())
                        out.write(line)

        except IOError as e:
            self.errors = '4:Cannot create output file {}. {}'.format(output_filename, e)


if __name__ == '__main__':
    updater = ReadWriteMulesYaml('a.yml', 'api_name')
    updater.read_yaml_file()
