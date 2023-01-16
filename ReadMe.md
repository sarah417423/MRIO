## Prerequisites
None

### Input dataset prepara        
- Download and unpack the code with the folder structure. 
- Download Inter-Country-Input-Output tables from http://oe.cd/icio to the "ICIO" folder.
- Download the following regional account datasets to the "Regional account" folder
  - Sub "nama_10r_3gva_tabular.tsv" from [Gross value added at basic prices by NUTS 3 regions](https://ec.europa.eu/eurostat/databrowser/view/nama_10r_3gva/default/table?lang=en)
  - Sub "nama_10r_2gfcf_tabular.tsv" from [Gross fixed capital formation by NUTS 2 regions](https://ec.europa.eu/eurostat/databrowser/view/nama_10r_2gfcf/default/table?lang=en)
- Download the Regional road freight flow data "01_Trucktrafficflow.csv" and "02_NUTS-3-Regions.csv" [ETISplus](https://data.mendeley.com/datasets/py2zkrb65h "Named link title") to the "Freight traffic" folder.

### Run the model
- Run "Code availability.py".

### Technical Validation
- Run "Technical_Validation_by_sector.py".
- Run "Technical_Validation_by_country.py".
