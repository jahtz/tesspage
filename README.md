# TessPAGE
Train Tesseract OCR with PAGE GT

## Usage
### Convert from PageXML to Tesseract Ground Truth
`python3 tesspage.py -c <input_dir> <output_dir>`

### Train Tesseract (not implemented)
`python3 tesspage.py -c <output_dir>`
(output_dir: output_dir of convert)

### Convert and train (not implemented)
`python3 tesspage.py -f <input_dir> <output_dir>`

### Purge output_dir (not implemented)
`python3 tesspage.py -p <output_dir>`

## TODO
- [x] convert files automatically
- [ ] add tesseract training (manual guide:  [StackOverflow](https://stackoverflow.com/questions/43352918/how-do-i-train-tesseract-4-with-image-data-instead-of-a-font-file))
- [ ] locate training output
- [ ] purge output folder
