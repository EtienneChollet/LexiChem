-> This project was contrived to extract the molecular formulae and corresponding molecular weights provided by PubChem's XML database of chemical species. The program xmlScraper.py is very specific to the XML files provided by NCBI's PubChem chemical database and will probably be useless in any other context besides extracting data from the files found here: ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/.

-> xmlScraper.py extracts a very tiny amount of information (molecular formula and weight) from the XML files which contain chemical data that are housed in XML_Splits. The program will attempt to extract data from all of the files in XML_Splits, so make sure they are the unzipped ones from the appropriate source (ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/). I would recommend doing this in batches of 5 XML files. These files are large, and this program is configured to use as many CPUs on your machine as possible.  

-> After extracting data, xmlScraper.py sorts the formulae by molecular weight and stores the data into a (more convenient) CSV file which will be housed in CSV_Splits. One CSV file will be made from each XML file. Since the XML files were processed asynchronously, the CSV file is not named in accordance with the data it contains, meaning that it is most likely not the data from its XML counterpart. 