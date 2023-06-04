"""
Format danbooru tag input for Stable Diffusion.

Able to format danbooru URLs, tags and files (including nested ones).

Usage: tag_formatter.py <input>
Input can be:
  - A danbooru post URL
  - A file
  - Unformatted tags

Thanks parabirb for regex and LuqueDaniel for pybooru. 
Nothing in here is remotely pythonic, please dont expect it to be.
"""

import sys
import re
import os
import logging
from pybooru import Danbooru

# pybooru config
client = Danbooru('danbooru')

# logging config
file_handler = logging.FileHandler('log.log', mode='a')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S'))
logger = logging.getLogger('tag_formatter')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

logging.info("Started")

def detection(input_str):
    # Regular expression to match a file or path
    path_regex = r'^([^:]+\..+)|(\/.*)|([A-Za-z]:\\.*)$'
    # Regular expression to match a URL
    url_regex = r'^https?://danbooru\.donmai\.us/posts/\d+.*$'
    # Check if the input matches either regular expression
    if re.match(url_regex, input_str):
        return "URL"
    elif re.match(path_regex, input_str):
        return "File"
    elif os.path.isdir(input_str):
        return "Dir"
    else:
        return "Tags"

def folder_format():
    # To be done
    pass

def file_format(nested_file = None, nested_folder = None):
    if nested_file is None:
        input_file = r"" + sys.argv[1]
        output_file = os.path.splitext(sys.argv[1])[0] + "_formatted.txt"
        nstd = False
    else:
        input_file = r"" + nested_file
        output_file = os.path.splitext(nested_file)[0] + "_formatted.txt"
        nstd = True

    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        # holy shit these log statements are cancer but I want to keep them as one line
        for line in f_in:
            if detection(line) == "URL":
                # String concatenation is actually faster here than format string literals
                logger.info((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"Detected as a URL: {line.rstrip()}")
                postidregex = r"/posts/(\d+)"
                # Use regex to extract the post ID from the URL
                match = re.search(postidregex, line)
                if match:
                    post_id = match.group(1)
                    post = client.post_show(post_id)
                    # Extract the tags from the post information
                    tags = post['tag_string']
                    tag = tags.replace(" ", ", ").replace("_", " ")
                    f_out.write(tag+"\n")
                else:
                    logger.warning((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"No post ID found in URL: {line}")
            elif detection(line) == "File":
                logger.info((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"Detected as nested file: {line.strip()}")
                try:
                    file_format(line.strip())
                except FileNotFoundError:
                    logger.error((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"Could not find {line.strip()}")
            elif detection(line) == "Dir":
                logger.info((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"Detected as a directory: {line.strip()}")          
                folder_format()
            elif detection(line) == "Tags":
                logger.info((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"Detected as tags: {(line[:93] + '...')}") # Limit to 100 chars (excluding the ...)
                tag = line.replace(" ", ", ").replace("_", " ")
                f_out.write(tag+"\n")
        logger.info((f"[NESTED FILE] ({os.path.basename(input_file)}) " if nstd else f"[BASE FILE] ({os.path.basename(input_file)}) ") + f"Formatted tags saved to: {output_file}")
    

def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print("Usage: tag_formatter.py <input>\nInput can be:\n  - A danbooru post URL\n  - A file\n  - Unformatted tags")
        exit(1)

    if detection(input) == "File":
        logger.info(f"Detected as a file: {input.strip()}")
        try:
            file_format()
        except FileNotFoundError:
            logger.error(f"Could not find {input.strip()}")
    elif detection(input) == "Dir":
        logger.info(f"Detected as a directory: {input.strip()}")
        folder_format()
    elif detection(input) == "Tags":
        logger.info(f"Detected as tags: {(input[:93] + '...')}")
        tag = input.replace(" ", ", ").replace("_", " ")
        logger.info("Formatted tags: " + tag)
    elif detection(input) == "URL":
        logger.info(f"Detected as a URL: {input.rstrip()}")
        postidregex = r"/posts/(\d+)"
        # Use regex to extract the post ID from the URL
        match = re.search(postidregex, input)
        if match:
            post_id = match.group(1)
            logger.info(f"Post ID: {post_id}")
            post = client.post_show(post_id)
            # Extract the tags from the post information
            tags = post['tag_string']
            tag = tags.replace(" ", ", ").replace("_", " ")
            logger.info("Formatted tags: " + tag)
        else:
            logger.warning(f"No post ID found in URL: {input}")

main()
