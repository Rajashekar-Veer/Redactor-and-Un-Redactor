# **Text Analysis on Norman Police Data**

## **Overview** 
	In this project we download a Daily Incident Summary PDF file from Norman Police Department website, and we read and process the data from the PDF file and create an SQLite database (policeDept.db) to store the extracted data. From the database we write a select query to print the Nature field and number of times a Nature has occurred in the downloaded file.

### **Setup.py and setup.cfg:** 
The setup.py file is used to automatically find the packages during the execution of the program.
The setup.cfg file is needed for executing pytest command which is need to run the test cases on the project.

### **Pipfile and Pipfile.lock:** 
Pipfile is used to create a virtual environment for execution of our project. This is created using below command.
pipenv install –python 3.8.1

### **main.py** 
The main.py is the starting point of execution of our program. 
The main.py can be executed after cloning the project cs5293sp20-project0 from git into local system by running the below line of code.

> pipenv run python project0/main.py –incidents URL

The main.py takes one parameter which is the URL of the PDF file. The main.py calls the functions
fetchIncidents(url), extractIncidents(), created(), dbInsert(db,incidents), dbStatus(db) from project0.py file.


### **project0.py**  
The project0.py contains all the function necessary to complete this project.
The functioning of each functions is mentioned below.

• **fetchIncidents(url):** 
In this function we use urllib.urlopen() function to open the PDF file from the url that we passed as argument to the fetchIncidents() function, and then from the opened file we read the data by using urlib.open(), and stored the data which is in form of object to a globally declared tempFile. 
The tempFile is then returned to the main.py file.

• **extractIncidents():** 
In this function we read in the tempFile that contains the PDF data bytes and using PdfFileReader() function from PyPDF2 library, we extract the text data from the tempFile.
Data = PdfFileReader(tempFile).getPage(i).extractText() is the code used to extract text data from the tempFile.
The text data that is extracted is then processed by various Text analysis technique and converted to a list of lists containing row records of the PDF file.  To do this we first remove the unwanted data i.e headers and footer using sub() function of regular expression.
Once the unwanted information is removed we then split the continuous text data into row records and the data is stored in a list by using re.split(r'\s+(?=\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2})', data). This List is then taken into a loop and each element of the list is iterated and is again split based on ‘\n’ into a sublist which containing each field value.
Later we check whether each sublist is of length 5 elements, if not based on our assumption that there is missing data in only Nature field we insert ‘NA’ to the fourth position of the sublist and is appended back to the main list.
The formatted data that is in form of list of lists where each sublist holding each row is then returned to main.py file 

• **createdb():** 
In this function we create an SQLite database with name ‘policeDept.db’. A table with a name incidents is created in this database. We use SQLite package to create the database using python 3.8.1.
With the help of cursor and execute function we can run the query within the database using python.
The table is created within the database using the below script.
CREATE TABLE IF NOT EXISTS incidents (DataTime TEXT, incidentNumber TEXT, location TEXT, Nature TEXT, incidentORI TEXT).
Once the table is created, we commit the changes using commit() function. The database name is returned to main.py file.


• **dbInsert(db, incidents):**
Once the database in created, dbInsert(db, incidents) is called from main.py file.
This parameter takes 2 parameters that is db = database name and incidents data from extractIncidents() function. 
In this function, the database connection is made and the incidents records are stored into the table one record after other using a for loop. The insert query is below.
INSERT INTO incidents VALUES (?, ?, ?, ?, ?);
Once all the incidents records are inserted, the changes are committed in the database.  


• **dbStatus(db):**
The main.py file calls dbStatus() function once the data is inserted using dbInsert(db,incidents). In this method again the connection to the database is made a query is executed in the database to fetch all the count of each Nature that is inserted in the database.
Query for fetching the nature and its count is below.
SELECT nature||"|"||count(*) as nature FROM incidents group by nature order by nature;
 
The query result is then printed on the console and the same is returned to main.py.



### **test_project0.py** 
The test_project0.py file consists of all test case related to each function defined in project0.py.
On execution of test_project0.py runs all the test cases with project0.py and returns whether the test cases pass or fail. 
There are 5 test cases written for each of the function defined in project0, these test cases are below.

• **test_fetchIncidents():**
This test case is used to test fetchIncidents() function in project0.py. This function executes the fetchIncidents() and get the retuned temFile pointer. The assert statement is used to check whether the tempFile contains data, if the condition is false it triggers an error.
assert project0.fetchIncidents(url) is not None

• **test_extractIncidents():**
This test case is used to test extractIncidents() function in project0.py file. This function executes extractIncidents() function and fetches the row data as retuned by the extractIncident fuction.
The assert statement is used to check whether each sublist has 5 elements, if the condition is false it triggers an error.
assert len(i) == 5

• **test_createdb():**
This test case is used to test createdb() function in project0.py file. This function execute  createdb() function and retrieves the database name that is created by project0.py. The assert statement checks whether the returned name matches ‘policeDept.db’, if the condition is false it triggers an error.
assert databaseName == 'policeDept.db'

• **test_dbInsert():**
The test_dbInsert() test case is used to test the dbInsert(db, incidents) function in project0.py.
The function execute dbInsert() function by passing arguments such as database name and incidents row records.
Once the dbInsert() function is executed, it opens up a database connection and with cursor and execute function a query is executed on the database and we fetch the 1st row data.
The assert statement checks whether the length of row data is same as the length of incident data that is passed. If the condition is false it triggers an error.
assert count[0] == len(incidents)


• **test_dbStatus():**
The test_dbStatus() test case is used to test the dbStatus() function in project0.py file.
This function executes fetchIncidents(), extractIncidents(), createdb() and dbStatus() function and retrieves the records that is printed at the end of the function.
The assert statement checks whether the data the is retrieved is not null. If the condition is false it triggers an error.
assert records is not None
 		
	







 


  
	
