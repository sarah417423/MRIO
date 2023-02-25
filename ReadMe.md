## Prerequisites
Before running the software, please install the depencies via pip freeze > requirements.txt

### Prepare input dataset      
- Download and unpack the codes with the folder structure. 
- Download Inter-Country-Input-Output tables from http://oe.cd/icio to the "ICIO" folder.
- Download the following regional account datasets to the "Regional account" folder
  -  "nama_10r_3gva_tabular.tsv" from [Gross value added at basic prices by NUTS 3 regions](https://ec.europa.eu/eurostat/databrowser/view/nama_10r_3gva/default/table?lang=en)
  -  "nama_10r_2gfcf_tabular.tsv" from [Gross fixed capital formation by NUTS 2 regions](https://ec.europa.eu/eurostat/databrowser/view/nama_10r_2gfcf/default/table?lang=en)
- Download the Regional road freight flow data "01_Trucktrafficflow.csv" and "02_NUTS-3-Regions.csv" [ETISplus](https://data.mendeley.com/datasets/py2zkrb65h "Named link title") to the "Trucktraffic" folder.
- 
 

### Run the model
- Run "Code availability.py".
  - The results are generated under "MRIO" folder.
  - "NIO" ,"SRIO" and "Prior" are by-products during the estimating process. 

### Technical Validation
- The "Austria", "Finland" and "Scorland" folder contain the survey data or estimation on input-output tables from local government. We consider them as a ground truth for technical validation.
- File "SRIO_compare.xlsx" is used to match the sectors of MRIO and the ground truth.
- Run "Technical_Validation_by_sector.py".
- Run "Technical_Validation_by_country.py".
- Results are generated under "Technical validation" folder.

