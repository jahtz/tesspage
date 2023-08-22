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
     ```
     $ python3 tesspage.py setup
     ```
   
### Structure
#### (after setup)
```
tesspage
│ README.md                 
│ requirements.txt          required pip packages
│ LICENSE                   license
└─ tesspage                 tesspage files
│  └ ...
└─ tesstrain¹               tesstrain files
│  └ ...
└─ data
│  │ eval                   default dir for evaluation
│  │ ground_truth           default dir for ground_truth output
│  │ ocr_input              default dir for tesseract image input
│  │ ocr_output             default dir for tesseract output
│  │ tessconfigs²           tesseract config files
│  │ tessdata_best³         training start model 
│  └ training_data          default dir for pagexml input
└─ tesspage.py              entry point

```
¹ [tesstrain](https://github.com/tesseract-ocr/tesstrain), ² [tessconfigs](https://github.com/tesseract-ocr/tessconfigs.git), ³ [tessdata_best](https://github.com/tesseract-ocr/tessdata_best) 

### Generate Ground-Truth
Copy PageXML + Image Files to `./data/training_data` (or custom folder)
```
python3 tesspage.py generate [--training_data <input_folder>] [--ground_truth <output_folder>]
```
- `--training_data`: input folder containing pagexml and image files [default: ./data/training_data/]
- `--ground_truth`: output folder (line image and text files after exec) [default: ./data/ground_truth/]

### Train Model
```
python3 tesspage.py training [--model_name <name>] [--start_model <model>] [--data_dir <folder>] [--ground_truth <folder>] [--tessdata <folder>] [--max_iterations <number>] [ARGS ...]
```
- `--model_name`: name of trained model [default: foo]
- `--start_model`: select start model. Previously trained model or lang-code (e.g. "eng") from [langdata](https://github.com/tesseract-ocr/langdata) [default: eng]
- `--data_dir`: tesstrain data dir [default: ./tesstrain/data/]
- `--ground_truth`: ground truth folder (line image and text files) [default: ./data/ground_truth/]
- `--tessdata`: training start model folder [default: ./data/tessdata_best/]
- `--max_iterations`: training iterations [default: 10000]
- `ARGS`: Full argument list [here](https://github.com/tesseract-ocr/tesstrain#train)

### Run Tesseract
```
python3 tesspage.py tesseract --model_name <name> [--input <path>] [--output <path>] [--data_dir <folder>] [--config_dir <config_dir>] [--config <config>] [ARGS ...]
```
- `--model_name`: select model, either language or custom trained model
- `--input`: input directory or image file
- `--output`: output directory
- `--data_dir`: tesstrain data dir [default: ./tesstrain/data/]
- `--config_dir`: Output config directory. [default: ./data/tessconfigs/configs/]
- `--config`: Config file to be used (txt, pdf, hocr, tsv, ...) [default: txt]
- `ARGS`: guide [here](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html)

### Evaluate Model
> [!NOTE]
> Coming soon.

### Help
```
python3 tesspage.py -h
```
## TODO:
- [x] more robust PageXML converter
- [x] start training from script
- [x] use Tesseract from script
- [ ] run Tesseract with pagexml output
- [ ] evaluate trained model
