# gpas-uploader-validate

This is a simple Python script that
* defines `pandera` SchemaModel classes for validating the various types of upload CSV files that can be imported and used by other Python code
* provides a simple Python script `gpas-validate-upload.py` that can be used to validate an upload CSV on the command-line

The validation is now extensive and insists that
* `name` is unique in the upload CSV
* any files (`fastq1`, `fastq2`, `fastq` or `bam`) have the expected file extensions and exist in the file system at the specified location
* that the `country` is specified using a known ISO 3-letter code e.g. `FRA`, `MEX` according to [ISO-3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)
* if a `region` is specified, that it matches one of the known administrative regions for that `country`, as defined by [ISO-3166-2](https://en.wikipedia.org/wiki/ISO_3166-2)
* the `collection_date` is provided in the correct ISO format e.g. `2021-01-13`, isn't in the future (or earlier than 01-Jan-2019) and does not contain a time 
* the `names` in the upload CSV file are unique
* `host` can only be `human`, `specimen-organism` can only be `SARS-CoV-2` and `primer_scheme` can only be `auto`: this is to allow future functionality/developments
* the uploading user and organisation is not provided since the user is authenticated via the GPAS upload client so this is known
* `control` can only be one of `positive`, `negative` or null (i.e. not given)
* most fields are checked using regular expressions to e.g. exclude parentheses, slashes or other punctuation/characters that could cause problems in e.g. file names.

## Installation

To install

```
$ git clone https://github.com:GenomePathogenAnalysisService/gpas-uploader-validate.git
$ cd gpas-uploader-validate
$ python setup.py install --user
```

The pre-requisites are `pandas`, `pandera` and `pycountry`. 

If the above does not install these packages for you they can all be installed via e.g. `pip install pandas --user`.

## Usage

### Define allowed tags

The user must create a plaintext file containing the permitted tags for that user as shown in the GPAS portal. Login to the GPAS portal as usual. Then by clicking the three horizontal lines in the top left, navigate to the `Upload` page and choose the `Tags` tab. You should see a list like

![GPAS portal](https://github.com/GenomePathogenAnalysisService/gpas-uploader-validate/blob/main/gpas-screenshot.png?raw=true)

Carefully copy (capitalisation is important!) the `Tag Name`s into a plaintext file with one tag per line. There is a tag file in `gpas_uploader_validate/data/tags.txt` that is used by default (and works with the upload CSVs in `examples/`). It contains

```
$ head gpas_uploader_validate/data/tags.txt
University_of_Oxford
HPRU
BRC_Covid
GPAS_OxUni
Good_quality
Poor_quality
site0
repeat
```

### Run script on upload CSV file

To get help

```
$ gpas-validate-upload.py --help
usage: gpas-validate-upload.py [-h] --upload_csv UPLOAD_CSV [--tag_file TAG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --upload_csv UPLOAD_CSV
                        path to the metadata CSV file that will be passed to the GPAS upload client
  --tag_file TAG_FILE   a plaintext file containing the allowed GPAS tags for this upload user -- the
                        list is available on the GPAS portal under Upload | Tags. If not specified,
                        then a default set is used.                  
```

This is a successful run:

```
$ gpas-validate-upload.py --upload_csv examples/illumina-upload-csv-pass.csv

                                        .
                     ,          ((((   ((((
                   ####         (((,
                      .    ((/
                                      %  *(((
           ##/    ###    /   %
           ###       ,        .         .
                 *      #
           %%%        *        %%%%%      %%%%%%%%        %%%          %%%%
           %%%   %.         %%%%%%%%%%    %%%%%%%%%%     %%%%%      %%%%%%%%%
       %%                  %%%            %%%     %%%   %%% %%%     %%%%%
      %%%%                 %%%    %%%%%   %%%%%%%%%%   %%%   %%%       %%%%%%%
               *     (/    #%%%      %%%  %%%         %%%%%%%%%%%    %     %%%
              %%%             %%%%%%%%    %%%        %%%       %%%   %%%%%%%%
                   #     /
            ,  #       .   .
           %%%      /     ,   /
                 #%%                  #
                       %    ,#         (
                   ,%%(     ##         ###
                   %%%%                ###
                                 ##
                                ###*

All tags validate against the tags provided in /Users/fowler/packages/gpas-uploader-validate/gpas_uploader_validate/data/tags.txt

--> All preliminary checks pass and this upload CSV can be passed to the GPAS upload client
```

And this is one where two issues have been identified (country is `US` rather than `USA` and `control` is `neg` rather than `negative`.)

```
$ gpas-validate-upload.py --upload_csv examples/illumina-upload-csv-fail-few.csv

                                        .
                     ,          ((((   ((((
                   ####         (((,
                      .    ((/
                                      %  *(((
           ##/    ###    /   %
           ###       ,        .         .
                 *      #
           %%%        *        %%%%%      %%%%%%%%        %%%          %%%%
           %%%   %.         %%%%%%%%%%    %%%%%%%%%%     %%%%%      %%%%%%%%%
       %%                  %%%            %%%     %%%   %%% %%%     %%%%%
      %%%%                 %%%    %%%%%   %%%%%%%%%%   %%%   %%%       %%%%%%%
               *     (/    #%%%      %%%  %%%         %%%%%%%%%%%    %     %%%
              %%%             %%%%%%%%    %%%        %%%       %%%   %%%%%%%%
                   #     /
            ,  #       .   .
           %%%      /     ,   /
                 #%%                  #
                       %    ,#         (
                   ,%%(     ##         ###
                   %%%%                ###
                                 ##
                                ###*

All tags validate against the tags provided in /Users/fowler/packages/gpas-uploader-validate/gpas_uploader_validate/data/tags.txt

     sample               error
0  MN908947  problem in control
1  MN908948  problem in country

--> Please fix the above errors and try validating again. Do not pass this upload CSV to the GPAS upload client.
```
This upload CSV has lots of errors

```
$ gpas-validate-upload.py --upload_csv examples/illumina-upload-csv-fail-many.csv

                                        .
                     ,          ((((   ((((
                   ####         (((,
                      .    ((/
                                      %  *(((
           ##/    ###    /   %
           ###       ,        .         .
                 *      #
           %%%        *        %%%%%      %%%%%%%%        %%%          %%%%
           %%%   %.         %%%%%%%%%%    %%%%%%%%%%     %%%%%      %%%%%%%%%
       %%                  %%%            %%%     %%%   %%% %%%     %%%%%
      %%%%                 %%%    %%%%%   %%%%%%%%%%   %%%   %%%       %%%%%%%
               *     (/    #%%%      %%%  %%%         %%%%%%%%%%%    %     %%%
              %%%             %%%%%%%%    %%%        %%%       %%%   %%%%%%%%
                   #     /
            ,  #       .   .
           %%%      /     ,   /
                 #%%                  #
                       %    ,#         (
                   ,%%(     ##         ###
                   %%%%                ###
                                 ##
                                ###*


      sample                           error
0   MN908947                problem in batch
1   MN908947               problem in run_id
2   MN908947              problem in control
3   MN908947      problem in collection_date
4   MN908947              problem in country
5   MN908947               problem in region
6   MN908947                 problem in host
7   MN908947    problem in specimen_organism
8   MN908947        problem in primer_scheme
9   MN908947  problem in instrument_platform
10  MN908947               problem in fastq1
11  MN908947               problem in fastq2
0   MN908947            tags do not validate

--> Please fix the above errors and try validating again. Do not pass this upload CSV to the GPAS upload client.
```
