import os

import pandera
from pandera.typing import Index, DataFrame, Series

from gpas_uploader_validate import BaseCheckSchema


class IlluminaFASTQCheckSchema(BaseCheckSchema):
    '''
    panderas Schema Model for upload CSVs containing Illumina paired reads
    '''

    # validate that the fastq1 file is alphanumeric and unique
    fastq1: Series[str] = pandera.Field(unique=True, str_matches=r'^[A-Za-z0-9/._-]+$', str_endswith='_1.fastq.gz', coerce=True)

    # validate that the fastq2 file is alphanumeric and unique
    fastq2: Series[str] = pandera.Field(unique=True, str_matches=r'^[A-Za-z0-9/._-]+$', str_endswith='_2.fastq.gz', coerce=True)

    # insist that the path to the fastq1 exists
    @pandera.check('fastq1')
    def check_file_exists(cls, a, error='fastq1 file does not exist'):
        return all(a.map(os.path.isfile))

    # insist that the path to the fastq2 exists
    @pandera.check('fastq2')
    def check_file_exists(cls, a, error='fastq2 file does not exist'):
        return all(a.map(os.path.isfile))


class NanoporeFASTQCheckSchema(BaseCheckSchema):
    '''
    panderas Schema Model for upload CSVs containing Nanopore unpaired reads
    '''

    # validate that the fastq file is alphanumeric and unique
    fastq: Series[str] = pandera.Field(unique=True, str_matches=r'^[A-Za-z0-9/._-]+$', str_endswith='.fastq.gz', coerce=True)

    # insist that the path to the fastq exists
    @pandera.check('fastq')
    def check_file_exists(cls, a, error='fastq file does not exist'):
        return all(a.map(os.path.isfile))


class BAMCheckSchema(BaseCheckSchema):
    '''
    panderas Schema Model for upload CSVs containing BAM files
    '''

    # validate that the bam file is alphanumeric and unique
    bam: Series[str] = pandera.Field(unique=True, str_matches=r'^[A-Za-z0-9/._-]+$', str_endswith='.bam', coerce=True)

    # insist that the path to the bam exists
    @pandera.check('bam')
    def check_file_exists(cls, a, error='bam file does not exist'):
        return all(a.map(os.path.isfile))
