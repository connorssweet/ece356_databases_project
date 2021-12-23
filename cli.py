#python - cli
import mysql.connector as mysql


#lists of flags used for each table and each CRUD operation
mandatoryCreateFlags = ["-flowKey", "-flowStart", "-src_ip", "-src_port", "-dest_ip", "-dest_port", "-protocolType"]

optionalCreateFlagsFlow = ["-src_ip_numeric"]

optionalCreateFlagsFlowStatistics = ["-flowEndReason", "-category", "-app_protocol", "-web_service"]

optionalCreateFlagsForwardFlowStatistics = ["-f_minPS", "-f_maxPS", "-f_avgPS", "-f_stdDevPS", "-f_minPIAT", \
                                            "-f_maxPIAT", "-f_avgPIAT", "-f_stdDevPIAT", "-f_flowStart", "-f_flowEnd", \
                                            "-f_flowDuration", "-f_pktTotalCount", "-f_octetTotalCount"]

optionalCreateFlagsBackwardFlowStatistics = ["-b_minPS", "-b_maxPS", "-b_avgPS", "-b_stdDevPS", "-b_minPIAT", \
                                             "-b_maxPIAT", "-b_avgPIAT", "-b_stdDevPIAT", "-b_flowStart", "-b_flowEnd", \
                                             "-b_flowDuration", "-b_pktTotalCount", "-b_octetTotalCount"]

optionalCreateFlagsTotalFlowStatistics = ["-minPS", "-maxPS", "-avgPS", "-stdDevPS", "-minPIAT", "-maxPIAT", "-avgPIAT", \
                                          "-stdDevPIAT", "-flowEnd", "-flowDuration", "-pktTotalCount", "-octetTotalCount"]

mandatoryCreateConnectionFlags = ["-src_ip", "-src_port", "-dest_ip", "-dest_port"]

optionalFlowFlags = ["-src_ip", "-src_port", "-dest_ip", "-dest_port", "-protocolType", "-src_ip_numeric"]

mandatory_RUD_Flags = ["-flowKey", "-flowStart"]
#Everything except flowKey

optional_RU_Flags = ["-flowKey", "-src_ip", "-src_port", "-dest_ip", "-dest_port", "-protocolType", "-src_ip_numeric", \
                    "-flowEndReason", "-category", "-app_protocol", "-web_service", "-minPS", "-maxPS", "-avgPS", \
                    "-stdDevPS", "-f_minPS", "-f_maxPS", "-f_avgPS", "-f_stdDevPS", "-b_minPS", "-b_maxPS", "-b_avgPS", \
                    "-b_stdDevPS", "-minPIAT", "-maxPIAT", "-avgPIAT", "-stdDevPIAT", "-f_minPIAT", "-f_maxPIAT", "-f_avgPIAT",\
                    "-f_stdDevPIAT", "-b_minPIAT", "-b_maxPIAT", "-b_avgPIAT", "-b_stdDevPIAT", "-flowStart", "-flowEnd",\
                    "flowDuration", "-f_flowStart", "-f_flowEnd", "-f_flowDuration", "-b_flowStart", "-b_flowEnd", "-b_flowDuration", \
                    "-pktTotalCount", "-octetTotalCount", "-f_pktTotalCount", "-f_octetTotalCount", "-b_pktTotalCount", "-b_octetTotalCount"]

#Create commands for each table
create_Flow_query                      = "INSERT INTO Flow(flowKey, flowStart, src_ip, src_port, dest_ip, dest_port, protocolType, src_ip_numeric) VALUES ("

create_FlowStatistics_query            = "INSERT INTO FlowStatistics(flowKey, flowStart, flowEndReason, category, app_protocol, web_service) VALUES ("

create_ForwardFlowStatistics_query     = "INSERT INTO ForwardFlowStatistics(flowKey, flowStart, f_minPS, f_maxPS, f_avgPS, f_stdDevPS, f_minPIAT, f_maxPIAT, f_avgPIAT, f_stdDevPIAT, f_flowStart, f_flowEnd, f_flowDuration, f_pktTotalCount, f_octetTotalCount) VALUES ("

create_BackwardFlowStatistics_query    = "INSERT INTO BackwardFlowStatistics(flowKey, flowStart, b_minPS, b_maxPS, b_avgPS, b_stdDevPS, b_minPIAT, b_maxPIAT, b_avgPIAT, b_stdDevPIAT, b_flowStart, b_flowEnd, b_flowDuration, b_pktTotalCount, b_octetTotalCount) VALUES ("

create_TotalFlowStatistics_query       = "INSERT INTO TotalFlowStatistics(flowKey, flowStart, minPS, maxPS, avgPS, stdDevPS, minPIAT, maxPIAT, avgPIAT, stdDevPIAT, flowEnd, flowDuration, pktTotalCount, octetTotalCount) VALUES ("

create_Host_query                      = "INSERT IGNORE INTO Host VALUES("

create_Connection_query                = "INSERT IGNORE INTO Connection VALUES("

create_terminate_query                 = ");"

delete_query                           = "DELETE FROM Flow WHERE flowKey="

table_join                             = "FROM Flow INNER JOIN FlowStatistics USING (flowKey, flowStart) INNER JOIN ForwardFlowStatistics USING (flowKey, flowStart) INNER JOIN TotalFlowStatistics USING (flowKey, flowStart) INNER JOIN BackwardFlowStatistics USING (flowKey, flowStart) "


passwordAdmin  = "admin"
passwordClient = "client" 

def userCreds():
    #Specify admin or client
    #prompt password until correct user and password has been input
    while True:
        print("Enter credentials")
        user = input("Enter user: ")
        password = input("Enter password: ")
        if user == "admin" and password == passwordAdmin:
            print("Successfully logged in with admin privileges")
            return True
        elif user=="client" and password == passwordClient:
            print("Successfully logged in with client privileges")
            return False
        else:
            print("Invalid Credentials. Please enter valid credentials\n")

def main():
    ADMIN_PRIV = userCreds()
   
    while True:
        print("Please insert command\n")
        getInput = input()
        getInput = getInput.split()
        if getInput[0] == "create":
            create(getInput[1:])
        elif getInput[0] == "read":
            read(getInput[1:])
        elif getInput[0] == "update":
            update(getInput[1:])
        elif getInput[0] == "delete":
            if(ADMIN_PRIV):
                delete(getInput[1:])
            else:
                print("Invalid command. Current user does not have privilege to delete\n")
        elif getInput[0] == "help":
            help(getInput[1:])
        elif getInput[0] == "exit":
            break
        elif getInput[0] == "relog":
            ADMIN_PRIV = userCreds()
        else:
            print("Invalid command. Use the \"help\" command to list valid commands.")

    print("Exiting CLI...")

#Creates and executes query for inserting into tables
def create(input):
    queryList = []
    #Check input to see if it is host flag
    if input[0] == "-host":
        queryList.append(createHost(input[1:]))

    #Check input to see if it is connection flag
    elif input[0] == "-connection":
        mandatoryFlagValues = createMandatoryFlags(input[1:], mandatoryCreateConnectionFlags)
        if len(mandatoryFlagValues) == 1:
            if mandatoryFlagValues == "0":
                return

        #append ip and port values and call host
        src_ip_flag = "-ip=" + mandatoryFlagValues[0]
        src_port_flag = "-port=" + mandatoryFlagValues[1]
        dest_ip_flag = "-ip=" + mandatoryFlagValues[2]
        dest_port_flag = "-port=" + mandatoryFlagValues[3]
        create(["-host", src_ip_flag, src_port_flag])
        create(["-host", dest_ip_flag, dest_port_flag])

        #add flag values to query
        query = create_Connection_query
        for i in range(len(mandatoryFlagValues)):
            query += mandatoryFlagValues[i] + ","
        
        #Remove additional commas
        query = query.rstrip(query[-1])
        query += create_terminate_query

        #Append query of inserting new src_ip, src_port, dest_ip and dest_port to Connection table to queryList
        queryList.append(query)

    #Check input to see if it is flow flag
    elif input[0] == "-flow":
        mandatoryFlagValues = createMandatoryFlags(input[1:], mandatoryCreateFlags)
        if len(mandatoryFlagValues) == 1:
            if mandatoryFlagValues == "0":
                return
        
        query = create_Flow_query
        for i in range(len(mandatoryFlagValues)):
            query += mandatoryFlagValues[i] + ","
        
        #call create functions for other tables to create seperate queries for those tables
        queryList = []
        queryList.append(createFlow(input[1:], query))
        queryList.append(createFlowStatistics(input[1:], mandatoryFlagValues[0], mandatoryFlagValues[1]))
        queryList.append(createForwardFlowStatistics(input[1:], mandatoryFlagValues[0], mandatoryFlagValues[1]))
        queryList.append(createBackwardFlowStatistics(input[1:], mandatoryFlagValues[0], mandatoryFlagValues[1]))
        queryList.append(createTotalFlowStatistics(input[1:], mandatoryFlagValues[0], mandatoryFlagValues[1]))

        #append src_ip, src_port, dest_ip and dest_port values and call connection
        src_ip_flag = "-src_ip=" + mandatoryFlagValues[2]
        src_port_flag = "-src_port=" + mandatoryFlagValues[3]
        dest_ip_flag = "-dest_ip=" + mandatoryFlagValues[4]
        dest_port_flag = "-dest_port=" + mandatoryFlagValues[5]
        connectionInput = ["-connection", src_ip_flag, src_port_flag, dest_ip_flag, dest_port_flag]
        create(connectionInput)
        
    
    #get connection
    db = mysql.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        passwd = "pasward",
        database = "ece356_project"
    )
    cursor = db.cursor()

    for x in range(len(queryList)):
        try:
            #execute query
            print(queryList[x])
            cursor.execute(queryList[x])
            #save table insertions onto database
            db.commit()
        except:
            print("Sql Error")
    
    if input[0] == "-host":
        print("\nSuccessful Host Creation\n")
    elif input[0] == "-connection":
        print("\nSuccessful Connection Creation\n")
    elif input[0] == "-flow":
        print("\nSuccessful Flow Creation\n")
    return

#generates query to create a Host entity
def createHost(input):
    #Insert new host ip and port to query
    query = create_Host_query
    if (input[0].rpartition('='))[0] == "-ip":
        query += (input[0].rpartition('='))[2] + "," + (input[1].rpartition('='))[2] + create_terminate_query
    else:
        query += (input[1].rpartition('='))[2] + "," + (input[0].rpartition('='))[2] + create_terminate_query

    #return completed query
    return query

#extracts mandatory flag values from input
def createMandatoryFlags(input, mandatoryFlags):
    checkMandatoryFlags = [False for i in range(len(mandatoryFlags))]
    mandatoryFlagValues = ["Empty"] * len(mandatoryFlags)
    for i in range(len(mandatoryFlags)):
        flag = mandatoryFlags[i]
        b = False
        for j in range(len(input)):
            #Check to see if current iteration of index flag is mandatory flag
            if flag == (input[j].rpartition('='))[0]:
                if not checkMandatoryFlags[i]:
                    checkMandatoryFlags[i] = True
                    mandatoryFlagValues[i] = (input[j].rpartition('='))[2]
                    b = True
                    break
                else:
                    #Error Message
                    print("Duplicate flag found. Use \"help -create\" for information on required flags.\n")
                    return "0"
        if not b:
            #Error Message
            print("Missing one or more mandatory flag for \"create\" command. Use \"help -create\" for information on required flags.\n")
            return "0"
    
    return mandatoryFlagValues

# return query for Flow table
def createFlow(input, query): 
    return createDownstream(input, query, optionalCreateFlagsFlow)

# return query for FlowStatistics table
def createFlowStatistics(input, flowKey, flowStart):
    query = create_FlowStatistics_query + flowKey + "," + flowStart + ","
    return createDownstream(input, query, optionalCreateFlagsFlowStatistics)

# return query for ForwardStatistics table
def createForwardFlowStatistics(input, flowKey, flowStart):
    query = create_ForwardFlowStatistics_query + flowKey + "," + flowStart + ","
    return createDownstream(input, query, optionalCreateFlagsForwardFlowStatistics)

# return query for BackwardStatistics table
def createBackwardFlowStatistics(input, flowKey, flowStart):
    query = create_BackwardFlowStatistics_query + flowKey + "," + flowStart + ","
    return createDownstream(input, query, optionalCreateFlagsBackwardFlowStatistics)

# return query for TotalStatistics table
def createTotalFlowStatistics(input, flowKey, flowStart):
    query = create_TotalFlowStatistics_query + flowKey + "," + flowStart + ","
    return createDownstream(input, query, optionalCreateFlagsTotalFlowStatistics)

#simplified function for create where queries are created according to flags given as input
def createDownstream(input, query, createFlagsList):
    checkOptionalFlags = [False for i in range(len(createFlagsList))]
    optionalFlagValues = [-1] * len(createFlagsList)
    for i in range(len(createFlagsList)):
        flag = createFlagsList[i]
        for j in range(len(input)):
            if flag == (input[j].rpartition('='))[0]:
                if not checkOptionalFlags[i]:
                    checkOptionalFlags[i] = True
                    optionalFlagValues[i] = (input[j].rpartition('='))[2]
                    break
                else:
                    print("Duplicate flag found. Use \"help -create\" for information on required flags.\n")
                    return
    
    for i in range(len(optionalFlagValues)):
        if optionalFlagValues[i] != -1:
            query += optionalFlagValues[i] + ","
        else:
            query += "NULL,"

    #Remove additional commas
    query = query.rstrip(query[-1])
    query += create_terminate_query
    
    return query

#Reads data values in tables for given flags
def read(input):

    query = "SELECT "
    
    #Not enough number of arguments/flags
    if len(input) < 1:
        print("Missing one or more mandatory flag for \"read\" command. Use \"help -read\" for information on required flags.\n")
        return
    
    #checks for existence of optional limit flag
    limit = False
    if (input[-1].rpartition('='))[0] == "-limit":
        limit = True
        limitAmount = (input[-1].rpartition('='))[2]

    w_exists = False

    if limit:
        w_index = len(input) - 1
    else:
        w_index = len(input)
    
    #Check to see if -w flag is in input
    for i in range(len(input)):
        if input[i] == "-w":
            if w_exists == True:
                print("Duplicate flag found. Use \"help -read\" for information on required flags.\n")
                return
            w_index = i
            w_exists = True

    #takes the input and parses the select flags, adds correct column names to query
    query = parseSelectFlags(input, query, w_index, w_exists)
    if query == -1:
        return

    #if -w is found then check to see conditions for WHERE
    if w_exists:
        query = parseWhereConditions(input, query, w_index)
    #if -w is not found check to see if -limit flag is in input
    else:
        if (input[len(input)-1].rpartition("="))[0] == "-limit":
            limit = True
            limitAmount = (input[len(input)-1].rpartition('='))[2]
        
    #run SQL query
    #check if run successful or not
    
    if limit:
        query += " limit " + limitAmount
    query += ';'

    #get connection
    db = mysql.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        passwd = "pasward",
        database = "ece356_project"
    )
    cursor = db.cursor()

    #execute query
    print(query)
    print("\n")
    try:
        cursor.execute(query)
        #prints all columns as tuples
        print(cursor.fetchall())
        print("\n")
    except:
        print("SQL Error Occurred")

    print("Successfully read values from tables.\n")
    return

#returns query for read after parsing selection flags
def parseSelectFlags(input, query, w_index, w_exists):
    
    #Check to see if -s is in input
    if input[0] == "-s":
        flagFound = False
        for i in range(1,w_index):
            flag = input[i]
            #Check to see -limit flag is in input
            if (flag.rpartition('='))[0] == "-limit":
                continue
            #Check to see -all flag is in input
            elif flag == "-all":
                flagFound = True
                if w_exists:
                    #Wrong placement of -w
                    if not w_index == 2:
                        #Error Message
                        print("Invalid flag used in conjunction with \"-all\". Use \"help -read\" for information on required flags.\n")
                        return -1
                else:
                    if len(input) > 3 or (len(input) == 3 and (not (input[2].rpartition('='))[0] == "-limit") ):
                        #Error Message
                        print("Invalid flag used in conjunction with \"-all\". Use \"help -read\" for information on required flags.\n")
                        return -1
                query += "* "
            
            #find all matching flags from input in optional_RU_Flags
            elif flag in optional_RU_Flags:
                flagFound = True
                query += flag[1:] + ','
            
            else:
                #Error Message
                print("Invalid flag(s) used . Use \"help -read\" for information on required flags.\n")
                return -1
    else:
        #Error Message
        print("Invalid flag(s) used. Use \"help -read\" for information on required flags.\n")
        return -1

    if not flagFound:
        #Error Message
        print("No select flags found. Use \"help -read\" for information on required flags.\n")
        return -1
    
    #remove ending commas
    query = query.rstrip(query[-1])
    query += " " + table_join

    return query

#returns query for read after parsing through conditional flags for WHERE
def parseWhereConditions(input, query, w_index):
    query += " WHERE "
    #if no conditional flags were used then return error message
    if w_index == len(input) - 1:
        print("Invalid flag(s) used . Use \"help -read\" for information on required flags.\n")
        return
        
    #Checks to see if -and conditional flag is in input
    elif input[w_index+1] == "-and":
        AND_flag = True
        
    #Checks to see if -or conditional flag is in input
    elif input[w_index+1] == "-or":
        AND_flag = False
    
    #Checks to see if -na conditional flag is in input and no -limit flag found right after -na
    elif input[w_index+1] == "-na" and len(input) > w_index+2 and (input[w_index+2].rpartition('='))[0] != "-limit":
        if len(input) > w_index + 4 or len(input) == w_index + 2 or (len(input) == w_index + 4 and (not (input[len(input)-1].rpartition('='))[0] == "-limit") ):
            print("Invalid flag(s) used. Use \"help -read\" for information on required flags.\n")
            return
        #-limit flag found in the correct placement and its value is stored
        elif (len(input) == w_index + 4 and (input[len(input)-1].rpartition('='))[0] == "-limit" ):
            limit = True
            limitAmount = (input[len(input)-1].rpartition('='))[2]
        
        #Get conditional operator's flag
        flag = checkOperator(input[w_index+2])
        if flag == -1:
            return
        #loop through all read flags until conditional operator's flag found
        if any(ext in flag for ext in optional_RU_Flags):
            query += (input[w_index+2])[1:]
        else:
            #error message
            print("Invalid flag used. Use \"help -read\" for information on required flags.\n")
            return
        w_index += 10
    else:
        #error message
        print("Invalid flag(s) used. Use \"help -read\" for information on required flags.\n")
        return
        
    for i in range(w_index+2,len(input)):
        #Get conditional operator's flag
        flag = checkOperator(input[i])
        if flag == -1:
            return
        
        #-limit flag found and its value is stored
        if flag == "-limit":
            if i == len(input) - 1:
                limit = True
                limitAmount = (input[i].rpartition('='))[2]
            else:
                #error message
                print("Invalid -limit flag used. Use \"help -read\" for information on required flags.\n")
                return
        
        #Loop through all flags and use correct conditional statement
        elif any(ext in flag for ext in optional_RU_Flags):
            query += (input[i])[1:]
            if AND_flag:
                query += " AND "
            else:
                query += " OR  "
    
    #remove extra AND or OR from query
    query = query.rstrip(query[len(query)-5:len(query)-1])
    return query

#Find the column names from the conditional flags
def checkOperator(input):
    if ">=" in input:
        flag = (input.rpartition(">="))[0] 
    elif ">" in input:
        flag = (input.rpartition(">"))[0] 
    elif "<=" in input:
        flag = (input.rpartition("<="))[0] 
    elif "<" in input:
        flag = (input.rpartition("<"))[0] 
    elif "!=" in input:
        flag = (input.rpartition("!="))[0] 
    elif "=" in input :
        flag = (input.rpartition("="))[0]  
    else:
        print("Invalid condition provided. Use \"help -read\" for information on required flags.\n")
        return -1
    return flag

#Updates data values in tables for given flags
def update(input):

    checkFlowKey = False
    checkFlowStart = False
    
    queryList = ["UPDATE Flow SET ", "UPDATE FlowStatistics SET ", "UPDATE ForwardFlowStatistics SET ", \
                 "UPDATE BackwardFlowStatistics SET ", "UPDATE TotalFlowStatistics SET "]
    
    flagLists = [optionalFlowFlags, optionalCreateFlagsFlowStatistics, \
                 optionalCreateFlagsForwardFlowStatistics, optionalCreateFlagsBackwardFlowStatistics, \
                 optionalCreateFlagsTotalFlowStatistics]
    
    queryCheckList = [False] * 5


    for i in range(len(input)):
        inputArr = input[i].rpartition('=')
        flagFound = False
        #Check to see if current iteration of index is a mandatory flag of flowKey
        if mandatory_RUD_Flags[0] == inputArr[0]:
            flagFound = True
            if checkFlowKey == True:
                print("Duplicate flag found. Use \"help -update\" for information on required flags.\n")
                return
            checkFlowKey = True
            flowKey = inputArr[2]
        
        #Check to see if current iteration of index is a mandatory flag of flowStart
        elif mandatory_RUD_Flags[1] == inputArr[0]:
            flagFound = True
            if checkFlowStart == True:
                print("Duplicate flag found. Use \"help -update\" for information on required flags.\n")
                return
            checkFlowStart = True
            flowStart = inputArr[2]

        #Add to query list for all relevant flags found for their corresponding tables
        for j in range(len(flagLists)):
            if inputArr[0] in flagLists[j]:
                flagFound = True
                queryList[j] += (input[i])[1:] + ','
                queryCheckList[j] = True
        
        if not flagFound:
            print("Flag not recognized. Use \"help -update\" for information on required flags.\n")
            return
    

    if not checkFlowKey or not checkFlowStart:
        print("Missing one or more mandatory flag for \"update\" command. Use \"help -update\" for information on required flags.\n")
        return

    #Finish update queries
    for i in range(len(queryList)):
        queryList[i] = queryList[i].rstrip((queryList[i])[-1]) + " WHERE flowKey=" + flowKey + "AND flowStart=" + flowStart + ';'

    #get connection
    db = mysql.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        passwd = "pasward",
        database = "ece356_project"
    )
    cursor = db.cursor()

    try:
        #execute query
        for i in range(len(queryCheckList)):
            if queryCheckList[i]:
                print(queryList[i])
                cursor.execute(queryList[i])
                db.commit()
        #save table changes onto database server
    except:
        print("SQL Error Occurred")
    
    print("\n")
    print("Successfully updated rows.\n")
    return
    #update flow table

#Deletes rows for given flowStart and flowKey values
def delete(input):
    query = "Empty"
    if len(input) < 2:
        print("Missing one or more mandatory flag for \"delete\" command. Use \"help -delete\" for information on required flags.\n")
        return
    elif len(input) > 2:
        print("Unexpected number of flags. Use \"help -delete\" for information on required flags.\n")
        return
    else:
        #Create deletion queries to be run in mysql
        query = delete_query + (input[0].rpartition('='))[2] + " AND flowStart=" + (input[1].rpartition('='))[2] + ';'
    
    #get connection
    db = mysql.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        passwd = "pasward",
        database = "ece356_project"
    )
    cursor = db.cursor()

    #execute query
    print(query)
    print("\n")
    try:
        cursor.execute(query)
        #save table deletions onto database server
        db.commit()
    except:
        print("Sql Error Occurred")

    print("Successfully deleted rows.\n")
    return

#Returns help commands and instructions for CLI
def help(input):
    #outputs all possible commands
    if len(input) == 0:
        print("\
These are the valid commands:\n\
create - creates an entry for the table: use \"help -create\" for flag information\n\
read - reads an entry from the table: use \"help -read\" for flag information\n\
update - updates an entry in the table: use \"help -update\" for flag information\n\
delete - deletes an entry in the table: use \"help -delete\" for flag information\n\
            ")

    elif input[0] == "-create":
        print("\
This is the format for the create command:\n\
    create <entity> <mandatory flags> <optional flags>\n\
\n\
The flags to choose which entity to create are:\n\
    -host: creates a host\n\
    -connection: creates a connection between two hosts\n\
    -flow: creates a flow along a connection\n\
\n\
Each entity has different mandatory flags, and they are as follows:\n\
\n\
For a host, the mandatory flags are:\n\
    -ip: ip address of the host\n\
    -port: port number of the host\
    \n\
\n\
For a connection, the mandatory flags are:\n\
    -src_ip\n\
    -src_port\n\
    -dest_ip\n\
    -dest_port\n\
    \n\
\
For a flow, the mandatory flags are:\n\
    -flowKey\n\
    -flowStart\n\
    -src_ip\n\
    -src_port\n\
    -dest_ip\n\
    -dest_port\n\
    -protocolType\n\
    \n\
All other flags are optional\n\
    Use help -flags for more info on all flags.\n\
    \n\
    WARNING: DO NOT put spaces between the FLAG and the OPERATOR and the VALUE\n\
    Examples:\n\
        Correct:\n\
        create -flow -flowKey='5' -flowStart=86054646 -src_ip='192.0.2.0' -src_port=80 -dest_ip='192.0.2.255' -dest_port=80 -protocolType=17\n\
        create -flow -flowKey='5' -flowStart=86054646 -src_ip='192.0.2.0' -src_port=80 -dest_ip='192.0.2.255' -dest_port=80 -protocolType=17 -src_ip_numeric=3221225984 -f_minPIAT=44 -f_avgPIAT=66 -f_pktTotalCount=9\n\
        \n\
        Incorrect:\n\
        create -flow -flowKey = '5' -flowStart =86054646 -src_ip= '192.0.2.0' -src_port=80 -dest_ip='192.0.2.255' -dest_port=80 -protocolType=17\n\
        create -flow -flowKey = '5' -flowStart =86054646 -src_ip= '192.0.2.0' -src_port=80 -dest_ip='192.0.2.255' -dest_port=80 -protocolType=17 -src_ip_numeric=3221225984 -f_minPIAT=44 -f_avgPIAT=66 -f_pktTotalCount=9\n\
            ")

    elif input[0] == "-read":
        print("\
This is the format for the read command:\n\
    read -s <list select flags> -w <connecting operator> <list selection condition flags> <optional: limit>\n\
\n\
The special flags for the read command are belows:\n\
    -all: select all flags - cannot be used in conjustion with other select flags\n\
    -limit=X: limits the number of outputs must occur at the end of the query\n\
    -w: OPTIONAL, used in conjunction with a connecting operator and one or more condition flags; only use when you want to include conditions\n\
    -w must occur after -s\n\
    <connecting operators> mandatory if -w flag is used\n\
    The connecting operators are:\n\
        -and: for multiple clauses. Usage: (-w -and clause1 clause2 ...) is equivalent to (WHERE clause1 AND clause2 AND ...). Number of clauses should be at least 2.\n\
        -or: for multple clauses. Usage: (-w -or clause1 clause2 ...) is equivalent to (WHERE clause1 OR clause2 OR ...). Number of clauses should be at least 2.\n\
        -na: for a single clause. Usage: (-w -na clause) is equivalent to (WHERE clause). Number of clauses should be 1.\n\
    \n\
All flags are available to be a part of the <list select flags>\n\
The list selection condition flags are the same as the list select flags but with the added distinction of there being some condition placed on the value\n\
    Use help -flags for more info on all flags.\n\
    \n\
Refer to the examples below:\n\
Examples: read -all \n\
          read -s -maxPS\n\
          read -s -f_maxPS -f_avgPS \n\
          read -s -maxPS -f_avgPS -limit=100\n\
          read -s -maxPS -f_avgPS -w -or -avgPS>1 -limit=100\n\
          read -s -minPS -pktTotalCount -w -and -minPS>=2 -avgPS<10 -limit=100 \n\
            ")

    elif input[0] == "-update":
        print("\
This is the format for the update command:\n\
    update -flowKey=VALUE -flowStart=VALUE <optional_flags>\n\
\n\
The optional flags include all other flags.\n\
    Use help -flags for more info on all flags.\n\
\n\
Examples:\n\
    update -flowKey='7' -flowStart=308902423 -f_stdDevPIAT=0.00025\n\
    update -flowKey='7' -flowStart=308902423 -minPS=22\n\
    update -flowKey='7' -flowStart=308902423 -flowDuration=3123 -avgPIAT=22.79\n\
            ")

    elif input[0] == "-delete":
        print("\
This is the format for the delete command:\n\
    delete -flowKey=VALUE -flowStart=VALUE\n\
\n\
Example:\n\
    delete -flowKey='7' -flowStart=308902423 \n\
")
    elif input[0] == "-flags":
        print("\
These are the available flags for the create, read, update, and delete commands:\n\
NOTE: Any querying on a flag of type varchar requires the value to be put in single quotes \n\
Ex: -flowKey='a04e5498a5b4a734b20e5238f7a3d35b' NOT -flowKey=a04e5498a5b4a734b20e5238f7a3d35b\n\
    \n\
    \n\
    -flowKey (varchar(250))              - Hash-based unique flow identifier\n\
    -flowStart (decimal(40,25))          - Start time in seconds of flow in UNIX time format\n\
    -src_ip (varchar(250))               - Network format of source IP\n\
    -src_port (int)                      - Port number for the source IP\n\
    -dest_ip (varchar(250))              - Network format of destination IP\n\
    -dest_port (int)                     - Port number for the destination IP\n\
    -protocolType (int)                  - IANA transport protocol number, either 1,6, or 17\n\
    -src_ip_numeric (bigint)             - Decimal format of source IP\n\
    -flowEndReason (int)                 - Backward packet arrival time standard deviation\n\
    -category (varchar(250))             - Type of nDPI communication\n\
    -app_protocol (varchar(250))         - Type of nDPI-detected application protocol\n\
    -web_service (varchar(250))          - Type of nDPI-detected  web-service\n\
    -minPS (int)                         - Total minimum packet size\n\
    -maxPS (int)                         - Total maximum packet size\n\
    -avgPS (decimal(40,25))              - Total average packet size\n\
    -stdDevPS (decimal(40,25))           - Total standard deviation of packet size\n\
    -minPIAT (decimal(40,25))            - Total minimum packet interarrival time\n\
    -maxPIAT (decimal(40,25))            - Total maximum packet interarrival time\n\
    -avgPIAT (decimal(40,25))            - Total average packet interarrival time\n\
    -stdDevPIAT (decimal(40,25))         - Total standard deviation of packet interarrival time\n\
    -flowEnd (decimal(40,25))            - End time in seconds of flow in UNIX time format\n\
    -flowDuration (decimal(40,25))       - Duration in seconds of flow in UNIX time format\n\
    -pktTotalCount (int)                 - Tally of all packets\n\
    -octetTotalCount (bigint)            - Tally of transmitted bytes with attention to the IP payload\n\
    -f_minPS (int)                       - Forward direction minimum packet size\n\
    -f_maxPS (int)                       - Forward direction maximum packet size\n\
    -f_avgPS (decimal(40,25))            - Forward direction average packet size\n\
    -f_stdDevPS (decimal(40,25))         - Forward direction standard deviation of packet size\n\
    -f_minPIAT (decimal(40,25))          - Forward direction minimum packet interarrival time\n\
    -f_maxPIAT (decimal(40,25))          - Forward direction maximum packet interarrival time\n\
    -f_avgPIAT (decimal(40,25))          - Forward direction average packet interarrival time\n\
    -f_stdDevPIAT (decimal(40,25))       - Forward direction standard deviation of packet interarrival time\n\
    -f_flowStart (decimal(40,25))        - Start time in seconds of flow in UNIX time format on forward trip\n\
    -f_flowEnd (decimal(40,25))          - End time in seconds of flow in UNIX time format on forward trip\n\
    -f_flowDuration (decimal(40,25))     - Duration in seconds of flow in UNIX time format on forward trip\n\
    -f_pktTotalCount (int)               - Tally of all packets on forward trip\n\
    -f_octetTotalCount (bigint)          - Tally of transmitted bytes with attention to the IP payload on forward trip\n\
    -b_minPS (int)                       - Backward direction minimum packet size\n\
    -b_maxPS (int)                       - Backward direction maximum packet size\n\
    -b_avgPS (decimal(40,25))            - Backward direction average packet size\n\
    -b_stdDevPS (decimal(40,25))         - Backward direction standard deviation of packet size\n\
    -b_minPIAT (decimal(40,25))          - Backward direction minimum packet interarrival time\n\
    -b_maxPIAT (decimal(40,25))          - Backward direction maximum packet interarrival time\n\
    -b_avgPIAT (decimal(40,25))          - Backward direction average packet interarrival time\n\
    -b_stdDevPIAT (decimal(40,25))       - Backward direction standard deviation of packet interarrival time\n\
    -b_flowStart (decimal(40,25))        - Start time in seconds of flow in UNIX time format on backward trip\n\
    -b_flowEnd (decimal(40,25))          - End time in seconds of flow in UNIX time format on backward trip\n\
    -b_flowDuration (decimal(40,25))     - Duration in seconds of flow in UNIX time format on backward trip\n\
    -b_pktTotalCount (int)               - Tally of all packets on backward trip\n\
    -b_octetTotalCount (bigint)          - Tally of transmitted bytes with attention to the IP payload on backward trip\n\
        ")

if __name__ == '__main__':
    main()