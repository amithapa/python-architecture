# import hashlib
# import os
# import shutil
# from pathlib import Path
#
# BLOCKSIZE = 65536
#
# def hash_file(path):
#     hasher = hashlib.sha1()
#     with path.open("rb") as file:
#         buf = file.read(BLOCKSIZE)
#         while buf:
#             hasher.update(buf)
#             buf = file.read(BLOCKSIZE
#     return hasher.hexdigest()
#
# def sync(source, dest):
#     # Walk the source folder and build a dict of filenames and their hashes
#     source_hashes = {}
#     # for folder, _, files in os.walk(source):
#         for fn in files:
#             source_hashes[hash_file(Path(folder) / fn)] = fn
