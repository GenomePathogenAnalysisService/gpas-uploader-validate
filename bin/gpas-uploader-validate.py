import argparse
import pathlib
import datetime

import pandas

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--upload_csv", required=True, help="path to the metadata CSV file that will be passed to the GPAS upload client")
    parser.add_argument("--tag_file", required = True, help="a plaintext file containing the allowed GPAS tags for this upload user -- the list is available on the GPAS portal under Upload | Tags")
    options = parser.parse_args()

    upload_csv = pathlib.Path(options.upload_csv)

    assert upload_csv.is_file(), 'provided upload CSV does not exist!'

    df = pandas.read_csv(upload_csv)

    assert 'instrument_platform' in df.columns, 'upload CSV must contain instrument_platform'

    assert len(df['instrument_platform'].unique()) == 1, 'each upload CSV must contain only a single instrument_platform.'

    sequencer = df['instrument_platform'].unique()[0]

    assert sequencer in ['Nanopore', 'Illumina'], 'instrument_platform must be one of Illumina or Nanopore'

    if sequencer == 'Nanopore':

        assert list(df.columns) == ['name', 'fastq', 'organisation', 'tags', 'specimenOrganism',
                                    'host', 'collectionDate', 'country', 'submissionTitle', 'submissionDescription',
                                    'instrument_platform', 'instrument_model', 'flowcell']

    if sequencer == 'Illumina':

        assert list(df.columns) == ['name', 'fastq1', 'fastq2', 'organisation', 'tags', 'specimenOrganism',
                                    'host', 'collectionDate', 'country', 'submissionTitle', 'submissionDescription',
                                    'instrument_platform', 'instrument_model', 'flowcell']

    with open('gpas_logo.txt') as INPUT:
        logo = INPUT.read()

    print(logo)

    # read in tags
    tag_file = pathlib.Path(options.tag_file)
    assert tag_file.is_file(), 'provided tag file does not exist!'

    allowed_tags = set()
    with open(tag_file, 'r') as INPUT:
        for line in INPUT:
            allowed_tags.add(line.rstrip())

    checks_pass = True

    if len(df.name.unique()) == len(df.name):
        names_unique = True
    else:
        names_unique = False

    if names_unique:
        print("All names given in the upload CSV are unique")
    else:
        checks_pass = False
        print("There are non-unique names in "+options.upload_csv)

    bad_tags = set()

    def check_tags(row):
        tags_ok = True
        cols = row['tags'].split(':')
        for i in cols:
            if i not in allowed_tags:
                tags_ok = False
                bad_tags.add(i)
        return tags_ok

    df['tags_ok'] = df.apply(check_tags,axis=1)

    if all(df.tags_ok):

        print("All tags validate against the tags provided in " + options.tag_file )

    else:

        checks_pass=False
        print("These rows do not validate: ", df[~df.tags_ok])
        print("..because they contain these tags: ", bad_tags)


    bad_dates=[]
    def check_collectionDate(row):

        try:
            datetime.date.fromisoformat(row['collectionDate'])
            return(True)
        except ValueError:
            bad_dates.append(row['collectionDate'])
            return(False)

    df['collectionDate_ok'] = df.apply(check_collectionDate,axis=1)

    if all(df.collectionDate_ok):

        print("All collectionDates are in the correct ISO format")

    else:

        checks_pass=False
        print("These rows do not validate: ", df[~df.collectionDate_ok])
        print("..because they contain these bad dates: ", bad_dates)

    print()
    if checks_pass:
        print("--> All preliminary checks pass and the metadata CSV can be passed to the upload Electron client")
    else:
        print("--> Please fix the above errors and try validating again. Do not pass this upload CSV to the Electron client.")
    # df.to_csv('results.csv')
