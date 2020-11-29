-> This project was created to extract the molecular weights and formulae of each chemical species found in PubChem's XML database (located at ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/).

-> xmlScraper.py downloads, parses, and searches, the XML files provided by PubChem's database, then deletes these files after extracting the relevant information. This script is very specific to the structure of PubChem's XML files, and will probably be useless in any other context besides those disclosed here. Although this may seem rather narrow, PubChem is home to the largest chemical database, boasting a collection of around 111 million chemical species. 

-> xmlScraper.py extracts a very tiny amount of information (molecular formula and weight) from the XML files which contain chemical data that are housed in XML_Splits. The program will attempt to extract data from all of the files in XML_Splits, so make sure they are the unzipped ones from the appropriate source (ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/). I would recommend doing this in batches of 5 XML files. These files are large, and this program is configured to use as many CPUs on your machine as possible.  

-> After extracting data, xmlScraper.py sorts the formulae by molecular weight and stores the data into a (more convenient) CSV file which will be housed in CSV_Splits. One CSV file will be made from each XML file. Since the XML files were processed asynchronously, the CSV file is not named in accordance with the data it contains, meaning that it is most likely not the data from its XML counterpart. 
