# TessPage
Toolset for Tesseract training with PageXML Ground-Truth

## Usage
### Install & Setup:
1. Clone tesspage:
    ```
    $ git clone https://github.com/Jatzelberger/tesspage
    ```

2. Install dependencies:
    ```
    $ sudo apt install -y tesseract-ocr libtesseract-dev libtool pkg-config make wget bash unzip bc
    $ cd tesspage
    $ pip install -r requirements.txt
   ```
3. Setup:
   - auto (experimental):
     ```
     $ python3 tesspage.py -s
     ```
   - manual:
     ```
     $ git clone https://github.com/tesseract-ocr/tesstrain
     $ git clone https://github.com/tesseract-ocr/tessdata_best
     $ cd ./tesstrain
     $ make tesseract-langdata
     $ cd ..
     ```
     - optional: `$ mkdir ./input`, `$ mkdir ./output`

### Generate Ground-Truth
```
in tesspage folder:
$ python3 tesspage.py -g <input_folder> <output_folder>
```

### Train Model
```
$ cd tesstrain
$ make training MODEL_NAME=<model_name> START_MODEL=<start_model> DATA_DIR=<data_dir> GROUND_TRUTH_DIR=<gt_dir> TESSDATA=<tessdata_best_dict> MAX_ITERATIONS=<iterations>
```
- `model_name`: select your model name
- `start_model`: select start model. Custom or Lang-Code (e.g. "eng") from [langdata](https://github.com/tesseract-ocr/langdata)
- `data_dir`: default: _/path/to/tesspage/tesstrain/data_
- `gt_dir`: default: _/path/to/tesspage/output_
- `tessdata_best_dict`: default: _/path/to/tesspage/tessdata_best_
- `iterations`: default: 10000

Full argument list: `$ make help` or [here](https://github.com/tesseract-ocr/tesstrain#train)

## TODO:
- [x] more robust PageXML converter
- [ ] start training from script
- [ ] use Tesseract from script
- [ ] convert Tesseract prediction data back to PageXML
- [ ] add option to purge output directory (all files or Tesstrain temp files)
