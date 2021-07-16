import os
import json
import re
from glob import glob
from typing import List

config = dict()

with open(os.path.join("config", "config.json"), 'r') as f:
    config = json.load(f)


def GetInputFile(name: str) -> str:
    """A function that returns the absolute path of a file,
    given its input name and the provided paths

    Args:
        name (str): The name of the file

    Returns:
        str: The relative file path
    """
    item = ""
    try:
        item = next(item["Path"]
                    for item in config["Data"] if item["Name"] == name)
    except StopIteration:
        pass
    print("File to fetch as input:", item)
    return item


def GetFinalOutput() -> List[str]:
    """Returns a list of the final file paths required to complete the pipeline

    Returns:
        List[str]: A list of final file paths
    """
    search = list()
    for item in config['Data']:
        search.append(
            re.search(
                r"^([A-Z:\\|\/]+)(.+[\\\/])(.+)(\.fa|\.fa\.gz)$",
                item["Path"]
            )
        )
    res = ["results/" + item.group(3) + extension for item in search for extension in [
        '.fa.gz', '.fa.gz.faidx', '.fa.gz.dict']]
    print("Files to generate: ", res)
    return res
