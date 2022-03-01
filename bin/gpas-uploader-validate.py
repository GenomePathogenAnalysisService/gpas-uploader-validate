import argparse
import pathlib
import datetime

import pandas
import pandera
import gpas_uploader_validate


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--upload_csv", required=True, help="path to the metadata CSV file that will be passed to the GPAS upload client")
    parser.add_argument("--tag_file", required=False, help="a plaintext file containing the allowed GPAS tags for this upload user -- the list is available on the GPAS portal under Upload | Tags")
    options = parser.parse_args()

    with open('gpas_logo.txt') as INPUT:
        logo = INPUT.read()
    print(logo)

    upload_csv = pathlib.Path(options.upload_csv)

    assert upload_csv.is_file(), 'provided upload CSV does not exist!'

    checks_pass = True

    df = pandas.read_csv(upload_csv)
    assert 'name' in df.columns, 'upload CSV must contain a column called name that contains the sample names'

    df.set_index('name', inplace=True,verify_integrity=False)

    try:
        gpas_uploader_validate.IlluminaFASTQCheckSchema.validate(df, lazy=True)
    except pandera.errors.SchemaErrors as err:
        checks_pass = False
        print(err)
        print(err.failure_cases)


    # read in tags if specified
    if options.tag_file:

        tag_file = pathlib.Path(options.tag_file)
        assert tag_file.is_file(), 'provided tag file does not exist!'

        allowed_tags = set()
        with open(tag_file, 'r') as INPUT:
            for line in INPUT:
                allowed_tags.add(line.rstrip())

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
            print()


    print()
    if checks_pass:
        print("--> All preliminary checks pass and the metadata CSV can be passed to the upload Electron client")
    else:
        print("--> Please fix the above errors and try validating again. Do not pass this upload CSV to the Electron client.")
