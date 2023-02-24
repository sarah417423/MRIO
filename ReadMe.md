## Prerequisites
Please read "requirement.txt" to get the version of python and package used in codes.

### Prepare input dataset      
- Download and unpack the codes with the folder structure. 
- Download Inter-Country-Input-Output tables from http://oe.cd/icio to the "ICIO" folder.
- Download the following regional account datasets to the "Regional account" folder
  - Sub "nama_10r_3gva_tabular.tsv" from [Gross value added at basic prices by NUTS 3 regions](https://ec.europa.eu/eurostat/databrowser/view/nama_10r_3gva/default/table?lang=en)
  - Sub "nama_10r_2gfcf_tabular.tsv" from [Gross fixed capital formation by NUTS 2 regions](https://ec.europa.eu/eurostat/databrowser/view/nama_10r_2gfcf/default/table?lang=en)
- Download the Regional road freight flow data "01_Trucktrafficflow.csv" and "02_NUTS-3-Regions.csv" [ETISplus](https://data.mendeley.com/datasets/py2zkrb65h "Named link title") to the "Trucktraffic" folder.
- 
 

### Run the model
- Run "Code availability.py".
  - Sub The results are generated under "MRIO" folder
  - Sub "NIO" and "SRIO" are by-products during the estimating process. 

### Technical Validation
- The "Austria", "Finland" and "Scorland" folder contain the survey data or estimation on input-output tables from local government. We consider them as a ground truth for technical validation.
- Run "Technical_Validation_by_sector.py".
- Run "Technical_Validation_by_country.py".
- Results "SRIO_compare" is generated under "Technical validation" folder.

