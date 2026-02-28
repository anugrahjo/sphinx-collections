import os
from inspect import isfunction
from shutil import rmtree

from sphinx_collections.drivers import Driver


class WriterFunctionDriver(Driver): # the function itself writes files into a target folder
    # A combination of FunctionDriver and CopyFolderDriver
    def run(self):

        if not isfunction(self.config["source"]):
            self.error("Source option must be a user-defined function. Nothing else.")
            return
        
        if not os.path.exists(self.config["target"]):
            self.info("Target {} does not exist, creating target ...".format(self.config["target"]))
            os.mkdir(self.config["target"])

        self.info("Run function...")
        try:
            function = self.config["source"]
            # result = function(self.config)
            function(self.config)
        except Exception as e:
            self.error("Problems during executing writer function", e)

        # write_result = self.config.get("write_result", True)
        # if write_result and result is not None:
        #     try:
        #         with open(self.config["target"], "w") as target_file:
        #             target_file.writelines(result.split("\n"))
        #     except IOError as e:
        #         self.error("Problems during writing function result to file", e)

    def clean(self):
        try:
            rmtree(self.config["target"])
            self.info("Folder deleted: {}".format(self.config["target"]))
        except FileNotFoundError:
            pass  # Already cleaned? I'm okay with it.
        except IOError as e:
            self.error("Problems during cleaning for collection {}".format(self.config["name"]), e)