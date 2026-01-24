import os


def get_image_path(image_rel_path):
    # os.path.dirname(__file__) gets the directory this file (utils.py) is in, which is the project root.
    root_dir = os.path.dirname(__file__)
    return os.path.join(root_dir, image_rel_path)
