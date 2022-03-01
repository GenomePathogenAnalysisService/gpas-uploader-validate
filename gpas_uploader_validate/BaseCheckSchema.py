import datetime

import pandas

import pandera
from pandera.typing import Index, DataFrame, Series
import pycountry

class BaseCheckSchema(pandera.SchemaModel):
    '''
    Class that validates the common fields in a GPAS upload CSV.
    '''

    # validate that batch is alphanumeric only
    batch: Series[str] = pandera.Field(str_matches=r'^[A-Za-z0-9._-]+$',
                                       coerce=True)

    # validate run_id is alphanumeric but can also be null
    run_id: Series[str] = pandera.Field(str_matches=r'^[A-Za-z0-9._-]+$',
                                        nullable=True, coerce=True)

    # validate (sample) name is alphanumeric and insist it is unique
    name: Index[str] = pandera.Field(str_matches=r'^[A-Za-z0-9._-]+$',
                                     unique=True, coerce=True)

    # insist that control is one of positive, negative or null
    control: Series[str] = pandera.Field(nullable=True,
                                         isin=['positive','negative',None],
                                         coerce=True)

    # validate that the collection is in the ISO format, is no earlier than 01-Jan-2019 and no later than today
    collection_date: Series[pandera.DateTime] = pandera.Field(gt='2019-01-01',
                                                              le=str(datetime.date.today()),
                                                              coerce=True)

    # insist that the country is one of the entries in the specified lookup table
    country: Series[str] = pandera.Field(isin=[i.alpha_3 for i in pycountry.countries],
                                         coerce=True)

    region: Series[str] = pandera.Field(nullable=True, isin=[i.name for i in list(pycountry.subdivisions)], coerce=True)

    postal_code: Series[str] = pandera.Field(nullable=True, coerce=True)

    # insist that the tags is alphanumeric, including : as it is the delimiter
    tags: Series[str] = pandera.Field(nullable=True,str_matches=r'^[A-Za-z0-9:_-]+$', coerce=True)

    # at present host can only be human
    host: Series[str] = pandera.Field(isin=['human'], coerce=True)

    # at present specimen_organism can only be SARS-CoV-2
    specimen_organism: Series[str] = pandera.Field(isin=['SARS-CoV-2'], coerce=True)

    # at present primer_schema can only be auto
    primer_scheme: Series[str] = pandera.Field(isin=['auto'], coerce=True)

    # insist that instrument_platform can only be Illumina or Nanopore
    instrument_platform: Series[str] = pandera.Field(isin=['Illumina', 'Nanopore'], coerce=True )

    # custom method that checks that the collection_date is only the date and does not include the time
    # e.g. "2022-03-01" will pass but "2022-03-01 10:20:32" will fail
    @pandera.check("collection_date")
    def check_collection_date(cls, a):
        return(a.dt.floor('d') == a).all()

    class Config:
        name = "BaseCheckSchema"
        strict = True
        coerce = True
