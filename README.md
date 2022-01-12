# gpas-uploader-validate

This is a simple Python script that checks the upload CSV file for 
* the provided Tags are allowed for this user
* the `collectionDate` is provided in the correct ISO format e.g. `2021-01-13`
* the `names` in the upload CSV file are unique

## Installation

To install

```
$ git clone https://github.com:GenomePathogenAnalysisService/gpas-uploader-validate.git
$ cd gpas-uploader-validate
$ python setup.py install --user
```

The only pre-requisite is `pandas`. If the above does not install `pandas` for you install it via `pip install pandas --user`.

## Usage

The user must create a plaintext file containing the permitted tags for that user as shown in the GPAS portal. Login to the GPAS portal as usual. Then by clicking the three horizontal lines in the top left, navigate to the `Upload` page and choose the `Tags` tab. You should see a list like

![GPAS portal](https://github.com/GenomePathogenAnalysisService/gpas-uploader-validate/blob/main/gpas-screenshot.png?raw=true)




