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

### Define allowed tags

The user must create a plaintext file containing the permitted tags for that user as shown in the GPAS portal. Login to the GPAS portal as usual. Then by clicking the three horizontal lines in the top left, navigate to the `Upload` page and choose the `Tags` tab. You should see a list like

![GPAS portal](https://github.com/GenomePathogenAnalysisService/gpas-uploader-validate/blob/main/gpas-screenshot.png?raw=true)

Carefully copy (capitalisation is important) the `Tag Name`s into a plaintext file with one tag per line. There is an example file in `examples/tags.txt` to show you the format

```
$ head examples/tags.txt
University_of_Oxford
HPRU
BRC_Covid
Batch_passed_neg_ctrl
GPAS_OxUni
Good_quality
Negative_control
Poor_quality
Positive_control
```

### Run script on upload CSV file

To get help

```
$ gpas-uploader-validate.py --help
usage: gpas-uploader-validate.py [-h] --upload_csv UPLOAD_CSV --tag_file TAG_FILE

optional arguments:
  -h, --help            show this help message and exit
  --upload_csv UPLOAD_CSV
                        path to the metadata CSV file that will be passed to the GPAS upload client
  --tag_file TAG_FILE   a plaintext file containing the allowed GPAS tags for this upload user -- the list is available on the GPAS portal under Upload |
                        Tags                       
```

This is a successful run:

```
$ gpas-uploader-validate.py --upload_csv examples/nanopore-samplesheet-template-good.csv --tag_file examples/tags.txt

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

All names given in the upload CSV are unique
All tags validate against the tags provided in examples/tags.txt
All collectionDates are in the correct ISO format

--> All preliminary checks pass and the metadata CSV can be passed to the upload Electron client
```

And this is one where issues have been identified

```
$ gpas-uploader-validate.py --upload_csv examples/illumina-samplesheet-template-fail.csv --tag_file examples/tags.txt

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

There are non-unique names in examples/illumina-samplesheet-template-fail.csv

These rows do not validate:                                     name                                           fastq1  ... flowcell tags_ok
1  cc858517-7bff-48d1-a2ce-58fd9b9a3b6e  80c19a80-597b-4012-b747-63dd02d40c9f_1.fastq.gz  ...       96   False

[1 rows x 15 columns]
..because they contain these tags:  {'negative control', 'GPAS_Oxuni'}

These rows do not validate:                                     name                                           fastq1  ... tags_ok collectionDate_ok
0  cc858517-7bff-48d1-a2ce-58fd9b9a3b6e  cc858517-7bff-48d1-a2ce-58fd9b9a3b6e_1.fastq.gz  ...    True             False

[1 rows x 16 columns]
..because they contain these bad dates:  ['2000/01/16']


--> Please fix the above errors and try validating again. Do not pass this upload CSV to the Electron client.
```
