# Zhir Benchmark

![Cat driving](https://media1.tenor.com/images/b5db61d6f086de808c17fd34eb9870a9/tenor.gif?itemid=16109266)

This repo contains a test suite to measure accuracy of our models, pre-processing, and post-processing scripts. We need to keep a diverse test suite to make sure that we don't regress in some areas while focusing on other areas.

Areas we are now focusing on include:

| Area                             | Description                                                  |
| -------------------------------- | ------------------------------------------------------------ |
| [Clean Scan](./data/clean-scans) | This helps us see how our models perform when we use proper hardware to scan the documents. This use case is very important for business because they usually don't mind using proper hardware (e.g. a normal scanner/printer) to scan the documents. Performance mostly depends on the models, and on the ability of pre-processing scripts not to mess up the already good images. |
| [Screenshots](./data/screenshots)     | Screenshots of images. This use case is important for extracting text from PDFs whose encoding has been corrupted. Performance mostly depends on the models, and on the ability of pre-processing scripts not to mess up the already good images. |
| [Phones](./data/phones)               | Contains images that are taken by a cell phone. The images might need quite a bit of pre-processing for Tesseract to be able to do a good job. Performance depends on the pre-processing scripts. |
| [Posters](./data/posters)             | Images that have colorful or complex backgrounds. Examples: Book covers, posters, memes, infographics, etc... |
| [Edge Cases](./data/edge-cases)       | Images that measure edge cases. Examples: White text on black background. |
| Tables                           | TBD                                                          |
| Two-columns                      | TBD                                                          |

## Format

Each test case is made up of two files:

1. An image file. Which can either be a JPG or PNG file.
2. A text file that contains the Ground Truth.

Example: `s-1.jpg` and `s-1.txt`

## How to run tests

### Run tesseract on all images:

```
python3 .\src\tess.py source dest languages [--tessdata]
```

Examples:

```
python3 ./src/tess.py ./data ./out ckb
```

```
python3 ./src/tess.py ./data ./out ckb --tessdata ./tessdata
```

## Resources

1. https://github.com/eddieantonio/ocreval
2. https://github.com/Shreeshrii/tesstrain-ckb/issues/1