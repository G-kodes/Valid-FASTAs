import os
import json
import re
from glob import glob
from typing import List

config = dict()

with open(os.path.join("config", "config.json"), 'r') as f:
    config = json.load(f)


def GetInputFile(wildcards: object = dict()) -> str:
    """A function that returns the absolute path of a file,
    given its input name and the provided paths

    Args:
        wildcards (object): The name of the file

    Returns:
        str: The relative file path
    """
    reX = r"^([A-Z]{0,1}:{1}[\\|\/]{1,2}){0,1}(.+[\\\/])*(.+)(\.fa|\.fa\.gz|\.fa\.gz\.faidx|\.fa\.gz\.dict)$"
    # regexMatches = re.search(
    #     reX,
    #     wildcards.file
    # )

    try:
        item = next(next(file for file in dataset['Files'] if re.search(reX, file).group(
            4) == wildcards.ext and re.search(reX, file).group(3) == wildcards.filename) for dataset in config["Data"])
    except Exception:
        item = "Error: No Match Found for this input request. FILENAME: " + \
            wildcards.filename + wildcards.ext
    print("File to fetch as input:", item)
    return {"file": item}


def GetFinalOutput(wildcards: object = dict()) -> List[str]:
    """Returns a list of the final file paths required to complete the pipeline

    Returns:
        List[str]: A list of final file paths
    """
    res = list()
    for item in config['Data']:
        for file in item['Files']:
            reX = re.search(
                r"^([A-Z]{0,1}:{1}[\\|\/]{1,2}){0,1}(.+[\\\/])*(.+)(\.fa|\.fa\.gz|\.fa\.gz\.faidx|\.fa\.gz\.dict)$",
                file
            )
            for extension in ['.fa.gz', '.fa.gz.faidx', '.fa.gz.dict']:
                res.append(
                    os.path.join(
                        "results",
                        reX.group(3) + extension
                    )
                )

    print("Files to generate: ", res)
    return res
