import argparse
import glob
import os
import shutil
import subprocess


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


parser = argparse.ArgumentParser(
    description="Runs tesseract on all image_paths using the specified language model(s)."
)

parser.add_argument(
    "source", help="The folder that contains the images.")
parser.add_argument(
    "dest", help="Destination Folder.")

parser.add_argument(
    "langs", help="The models to use with tesseract. Examples: ckb or ckb+eng.")
parser.add_argument(
    "--tessdata", help="Path for tesseract models.")

args = parser.parse_args()

image_paths = []
types = ['*.jpg', '*.jpeg', '*.png']
for image_type in types:
    pattern = os.path.join(args.source, '*/' + image_type)
    image_paths.extend(glob.glob(pattern))

args.dest = os.path.join(args.dest, args.langs)

for image in image_paths:
    print(image)
    gt_path = os.path.splitext(image)[0] + ".txt"

    # if there is no ground truth for the image, ignore it
    if not os.path.exists(gt_path):
        image_paths.remove(image)
        print("skipped")
        continue

    # get destination dir for the current image
    dir_name = os.path.dirname(image).replace(args.source, "")
    if (dir_name.startswith('/') or dir_name.startswith('\\')):
        dir_name = dir_name.strip('/\\')
    dir_name = os.path.join(args.dest, dir_name)

    # copy image and ground truth to destination dir
    makedirs(dir_name)
    shutil.copy(gt_path, dir_name)
    shutil.copy(image, dir_name)

    # run tesseract :D
    env = os.environ.copy()
    if args.tessdata is not None:
        env["TESSDATA_PREFIX"] = args.tessdata

    actual_path = os.path.join(dir_name, os.path.splitext(
        os.path.basename(image))[0] + ".actual")

    subprocess.run(["tesseract", "-l", args.langs,
                    image, actual_path, "txt"], env=env)
