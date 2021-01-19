--> This software creates a sorted database of all known chemicals (sourced from PubChem) in the form of multiple csv files. First, the (gzip) XML files from PubChem (located [Here](ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/)) are downloaded to the machine that is running the software, then they are parsed to extract the molecular formula, average weight, and exact mass of each molecule in accordance with PubChem ID (PID). The file is read in binary to avoid unzipping the gzip file (each XML is ~15 GB) and parsed line-by-line to significantly reduce the useage of RAM. The database corresponding to one PubChem file is sorted by exact mass and written to a respective csv file. The csv files can be merged and sorted, or can be partitioned into mass ranges to improve the efficacy of sorting by mass. This process occurs for each of the ~150 files that PubChem has to offer, and is typically done in batches of 5, utilizing the multithreading power of the `concurrent.futures` module. 


-> xmlScraper.py downloads, parses, and searches, the XML files provided by PubChem's database, then deletes these files after extracting the relevant information. This script is very specific to the structure of PubChem's XML files, and will probably be useless in any other context besides those discussed here. PubChem is home to the largest database of chemicals, boasting a collection of around 111 million chemical species. 

-> xmlScraper.py extracts a very tiny amount of information (molecular formula and weight) from the XML files which contain chemical data that are housed in XML_Splits. The program will attempt to extract data from all of the files in XML_Splits, so make sure they are the unzipped ones from the appropriate source (ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/). I would recommend doing this in batches of 5 XML files. These files are large, and this program is configured to use as many CPUs on your machine as possible.  

-> After extracting data, xmlScraper.py sorts the formulae by molecular weight and stores the data into a (more convenient) CSV file which will be housed in CSV_Splits. One CSV file will be made from each XML file. Since the XML files were processed asynchronously, the CSV file is not named in accordance with the data it contains, meaning that it is most likely not the data from its XML counterpart. 
