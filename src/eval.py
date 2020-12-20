import argparse
import glob
import os
import shutil
import subprocess
import zhirpy


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def run_sum_app(files, report_path, app):
    if len(files) == 1:
        shutil.copy(files[0], report_path)
        return

    f = open(report_path, "w")
    args = files[:]  # copy list by value
    args.insert(0, app)
    subprocess.run(args=args, stdout=f)
    f.close()


def char_accuracy_sum(files, report_path):
    run_sum_app(files, report_path, 'accsum')


def word_accuracy_sum(files, report_path):
    run_sum_app(files, report_path, 'wordaccsum')


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
    "--dirty", action="store_true", help="Don't run clean script.")

args = parser.parse_args()

image_paths = []
types = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG']
for image_type in types:
    pattern = os.path.join(args.source, '*/' + image_type)
    image_paths.extend(glob.glob(pattern))

args.dest = os.path.join(args.dest, args.langs)

character_accuracy_reports = []
word_accuracy_reports = []

if os.path.exists(args.dest):
    shutil.rmtree(args.dest)

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

    # copy ground truth to destination dir
    makedirs(dir_name)
    shutil.copy(gt_path, dir_name)

    dest_image = os.path.join(dir_name, os.path.basename(image))
    if (args.dirty):
        shutil.copy(image, dest_image)
    else:
        # clean image and put it in the destination dir
        zhirpy.clean(image, dest_image)

    # run tesseract :D
    env = os.environ.copy()
    actual_path = os.path.join(dir_name, os.path.splitext(
        os.path.basename(image))[0] + ".actual")

    subprocess.run(["tesseract", "-l", args.langs,
                    dest_image, actual_path, "txt"], stdout=subprocess.DEVNULL)

    actual_path = actual_path + ".txt"  # tesseract appends .txt

    # run char accuracy
    ca_path = os.path.join(dir_name, os.path.splitext(
        os.path.basename(image))[0] + ".ca.txt")
    character_accuracy_reports.append(ca_path)
    subprocess.run(["accuracy", gt_path, actual_path, ca_path])

    # run word accuracy
    wa_path = os.path.join(dir_name, os.path.splitext(
        os.path.basename(image))[0] + ".wa.txt")
    word_accuracy_reports.append(wa_path)
    subprocess.run(["wordacc", gt_path, actual_path, wa_path])

for dir in os.listdir(args.dest):
    full_path = os.path.join(args.dest, dir)
    if not os.path.isdir(full_path):
        continue

    char_accuracy_sum(glob.glob(full_path + '/*.ca.txt'),
                      os.path.join(full_path, 'character_accuracy.txt'))

    word_accuracy_sum(glob.glob(full_path + '/*.wa.txt'),
                      os.path.join(full_path, 'word_accuracy.txt'))

# final summary
char_accuracy_sum(character_accuracy_reports, os.path.join(
    args.dest, 'character_accuracy.txt'))
word_accuracy_sum(word_accuracy_reports, os.path.join(
    args.dest, 'word_accuracy.txt'))
