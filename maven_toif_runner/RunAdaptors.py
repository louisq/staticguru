import fnmatch
import os
import subprocess

import sys
from git import Repo
import re

from config import TOIF_EXECUTABLE

__author__ = 'louisq'


class Adaptors:

    list_of_files = []

    GIT_REPO_HOME = "~/git"

    # Depends on the directory structure git/{organisation}/{project}
    REPO_REGEX = re.compile("(.+/git/(\w+)/(\w+))")
    JAVA_REGEX = re.compile("\./((?:\w+/)+\w+)(?:\$\w+)*\.class")

    MAXIMUM_NUMBER_OF_PROCESSES = 48
    SUB_PROCESS = []  # Do not modify this line

    ADAPTORS = ["Findbugs", "Jlint"]

    def __init__(self):
        print "Running CESEL TOIF python automation script on compiled classes"
        print "Arguments: %s" % str(sys.argv)

        self.REPO_PATH = sys.argv[1]
        self.OUTPUT_DIR = sys.argv[2]
        # TODO this might be flaky if ever we decide to change the path to somewhere else, but it should be good for now
        # output directory needs to be contained in root of repo path
        # self.REPO_PATH = self.OUTPUT_DIR[:self.OUTPUT_DIR.rfind("/")]
        self.HOUSE_KEEPING = sys.argv[3]
        self.execute()
        print "There are a total of %s classes which could be analysed using TOIF" % len(self.list_of_files)

    def execute(self):
        # todo Check if the housekeeping file exist. If it does not exist create it
        # repo_path = self.REPO_REGEX.match(os.path.abspath(".")).groups()
        # project_path = "%s.%s" % (repo_path[1], repo_path[2])

        repo = Repo(self.REPO_PATH)
        # commit_hash = repo.head.commit.hexsha
        modified_files = repo.head.commit.stats.files.keys()
        print modified_files

        # self.OUTPUT_DIR = os.path.join(self.OUTPUT_DIR, project_path, commit_hash)

        self.run_on_path(modified_files)

    def run_on_path(self, modified_files):
        paths = []
        for path, directory, files in os.walk("./"):
            # Identify all f the class
            # print files
            files = fnmatch.filter(files, '*.class')

            if len(files) > 0:

                for file_name in files:

                    file_path = os.path.join(path, file_name)

                    # print file_path
                    self.list_of_files.append(file_path)

                    if self._file_in_commit(modified_files, file_path):
                        self._run_all_adaptors_on_file(os.path.abspath(file_path), path, file_name)

                    # Prevent the creation of too many processes
                    if len(self.SUB_PROCESS) >= self.MAXIMUM_NUMBER_OF_PROCESSES:
                        for p in self.SUB_PROCESS:
                            p.wait()

    def _run_all_adaptors_on_file(self, file_path, dir, file):
        # common_args = ["--housekeeping", self.HOUSE_KEEPING, "--outputdirectory", self.OUTPUT_DIR, "--inputfile", file]
        common_args = ["--housekeeping", self.HOUSE_KEEPING, "--outputdirectory", self.OUTPUT_DIR, "--inputfile", file_path]
        # common_args = []
        for adaptor in self.ADAPTORS:
            self._run_adaptor_on_file(adaptor, common_args, dir)

    def _run_adaptor_on_file(self, adaptor, common_args, dir):

        # TODO remove full path of toif if not good
        adaptor_command = [TOIF_EXECUTABLE, "--adaptor", adaptor]
        # adaptor_command = ["/home/louisq/toif/toif/toif", "--adaptor", adaptor]
        adaptor_command.extend(common_args)
        print adaptor_command
        p = subprocess.Popen(adaptor_command, shell=False, cwd=dir)
        self.SUB_PROCESS.append(p)

    def _file_in_commit(self, modified_files, file_path):

        clean_path = self.JAVA_REGEX.match(file_path).groups()[0]

        for modified_file in modified_files:
            if clean_path in modified_file:
                print "Analysing %s" % modified_file
                return True

        return False


Adaptors()


