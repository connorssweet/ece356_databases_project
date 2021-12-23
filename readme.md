1.	Install mysql-connector-python by running “pip install mysql-connector-python"
2.	Run updated_schema.sql in database
a.	Modify number of rows inserted from csv on line 66 if you wish to do so. Total number of rows in csv is 2,704,839. Line 66 states how many rows to ignore when loading data into the table such as “IGNORE 2,700,000 ROWS” will create a table with 4,839 rows,
3.	Open cli.py and modify the following lines 171, 342, 565 and 604 with correct values for host, user, passwd and database. If host requires port then add an additional property ‘ port=“yourPortNumber“ ’. If you want to connect to marmoset04 then change host to host=“marmoset04.shoshin.uwaterloo.ca”, user=“userID”, password=“yourPassword” and database=“databaseName”.
4.	To run CLI, type ‘python3 cli.py’ in terminal
5.	Program will ask for credentials. There are 2 users with authentication given to run CLI
a.	Admin: user=admin, password=admin (User is able to use delete command)
b.	Client: user=client, password=client (User is unable to use delete command)
6.	Run commands or type ‘help’ inside CLI for further instructions (refer to testcases for valid commands).
7.	Type ‘exit’ to exit out of CLI
