DROP TABLE IF EXISTS TotalFlowStatistics;
DROP TABLE IF EXISTS BackwardFlowStatistics;
DROP TABLE IF EXISTS ForwardFlowStatistics;
DROP TABLE IF EXISTS FlowStatistics;
DROP TABLE IF EXISTS Flow;
DROP TABLE IF EXISTS Connection;
DROP TABLE IF EXISTS Host;
DROP TABLE IF EXISTS InternetTrafficInternal;

CREATE TABLE InternetTrafficInternal(
    flow_key varchar(250),
    src_ip_numeric bigint,
    src_ip varchar(250),
    src_port int,
    dst_ip varchar(250),
    dst_port int,
    proto int,
    pktTotalCount int,
    octetTotalCount bigint,
    min_ps int, 
    max_ps int,
    avg_ps decimal(40,25),
    std_dev_ps decimal(40,25),
    flowStart decimal(40,25),
    flowEnd decimal(40,25),
    flowDuration decimal(40,25),
    min_piat decimal(40,25),
    max_piat decimal(40,25),
    avg_piat decimal(40,25),
    std_dev_piat decimal(40,25),
    f_pktTotalCount int,
    f_octetTotalCount bigint,
    f_min_ps int, 
    f_max_ps int,
    f_avg_ps decimal(40,25),
    f_std_dev_ps decimal(40,25),
    f_flowStart decimal(40,25),
    f_flowEnd decimal(40,25),
    f_flowDuration decimal(40,25),
    f_min_piat decimal(40,25),
    f_max_piat decimal(40,25),
    f_avg_piat decimal(40,25),
    f_std_dev_piat decimal(40,25),
    b_pktTotalCount int,
    b_octetTotalCount bigint,    
    b_min_ps int, 
    b_max_ps int,
    b_avg_ps decimal(40,25),
    b_std_dev_ps decimal(40,25),
    b_flowStart decimal(40,25),
    b_flowEnd decimal(40,25),
    b_flowDuration decimal(40,25),
    b_min_piat decimal(40,25),
    b_max_piat decimal(40,25),
    b_avg_piat decimal(40,25),
    b_std_dev_piat decimal(40,25),
	flowEndReason int,
    category varchar(250),
    application_protocol varchar(250),
    web_service varchar(250)
);

LOAD DATA INFILE '/var/lib/mysql-files/21-Network-Traffic/Unicauca-dataset-April-June-2019-Network-flows.csv' INTO TABLE InternetTrafficInternal
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 ROWS
  (
	flow_key,
    src_ip_numeric,
    src_ip,
    src_port,
    dst_ip,
    dst_port,
    proto,
    pktTotalCount,
    octetTotalCount,
    min_ps, 
    max_ps,
    avg_ps,
    std_dev_ps,
    flowStart,
    flowEnd,
    flowDuration,
    min_piat,
    max_piat,
    avg_piat,
    std_dev_piat,
    f_pktTotalCount,
    f_octetTotalCount,
    f_min_ps, 
    f_max_ps,
    f_avg_ps,
    f_std_dev_ps,
    f_flowStart,
    f_flowEnd,
    f_flowDuration,
    f_min_piat,
    f_max_piat,
    f_avg_piat,
    f_std_dev_piat,
    b_pktTotalCount,
    b_octetTotalCount,    
    b_min_ps, 
    b_max_ps,
    b_avg_ps,
    b_std_dev_ps,
    b_flowStart,
    b_flowEnd,
    b_flowDuration,
    b_min_piat,
    b_max_piat,
    b_avg_piat,
    b_std_dev_piat,
	flowEndReason,
    category,
    application_protocol,
    web_service 
  );

CREATE TABLE Host (
	ip varchar(250) NOT NULL,
	port int NOT NULL CHECK (port>=0 AND port<=65535),
	PRIMARY KEY(ip,port)
);

INSERT IGNORE INTO Host (ip, port)
SELECT DISTINCT src_ip, src_port FROM InternetTrafficInternal;

INSERT IGNORE INTO Host (ip, port)
SELECT DISTINCT dst_ip, dst_port FROM InternetTrafficInternal;

CREATE TABLE Connection (
	src_ip varchar(250) NOT NULL,
	src_port int NOT NULL,
	dest_ip varchar(250) NOT NULL,
	dest_port int NOT NULL,
	PRIMARY KEY(src_ip, src_port, dest_ip, dest_port),
	FOREIGN KEY (src_ip, src_port) REFERENCES Host(ip,port) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (dest_ip, dest_port) REFERENCES Host(ip,port) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT IGNORE INTO Connection (src_ip, src_port, dest_ip, dest_port)
SELECT DISTINCT src_ip, src_port, dst_ip, dst_port FROM InternetTrafficInternal;

CREATE TABLE Flow (
	flowKey varchar(250) NOT NULL,
	flowStart decimal(40,25) NOT NULL,
	src_ip_numeric bigint,
	src_ip varchar(250) NOT NULL,
	src_port int NOT NULL,
	dest_ip varchar(250) NOT NULL,
	dest_port int NOT NULL,
	protocolType int NOT NULL CHECK (protocolType=17 OR protocolType=6 OR protocolType=1),
	PRIMARY KEY (flowKey, flowStart),
	FOREIGN KEY (src_ip, src_port, dest_ip, dest_port) REFERENCES Connection(src_ip, src_port, dest_ip, dest_port) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT IGNORE INTO Flow (flowKey, flowStart, src_ip_numeric, src_ip, src_port, dest_ip, dest_port, protocolType)
SELECT flow_key, flowStart, src_ip_numeric, src_ip, src_port, dst_ip, dst_port, proto FROM InternetTrafficInternal;

CREATE TABLE FlowStatistics(
	flowKey varchar(250) NOT NULL,
	flowStart decimal(40,25) NOT NULL,
	flowEndReason int CHECK(flowEndReason>=0 AND flowEndReason<=5),
	category varchar(250) ,
	app_protocol varchar(250),
	web_service varchar(250),
	PRIMARY KEY (flowKey, flowStart),
	FOREIGN KEY (flowKey, flowStart) REFERENCES Flow(flowKey, flowStart) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT IGNORE INTO FlowStatistics (flowKey, flowStart, flowEndReason, category, app_protocol, web_service)
SELECT flow_key, flowStart, flowEndReason, category, application_protocol, web_service FROM InternetTrafficInternal;

CREATE TABLE ForwardFlowStatistics( 
	flowKey varchar(250) NOT NULL,
	flowStart decimal(40,25) NOT NULL,
	f_minPS int CHECK (f_minPS>=0),
	f_maxPS int CHECK (f_maxPS>=0),
	f_avgPS decimal(40,25) CHECK (f_avgPS>=0),
	f_stdDevPS decimal(40,25) CHECK (f_stdDevPS>=0),
	f_minPIAT decimal(40,25) CHECK (f_minPIAT>=0),
	f_maxPIAT decimal(40,25) CHECK (f_maxPIAT>=0),
	f_avgPIAT decimal(40,25) CHECK (f_avgPIAT>=0),
	f_stdDevPIAT decimal(40,25) CHECK (f_stdDevPIAT>=0),
	f_flowStart decimal(40,25) CHECK (f_flowStart>=0),
	f_flowEnd decimal(40,25) CHECK (f_flowEnd>=0),
	f_flowDuration decimal(40,25) CHECK (f_flowDuration>=0),
	f_pktTotalCount int CHECK(f_pktTotalCount>=0),
	f_octetTotalCount bigint CHECK(f_octetTotalCount>=0),
	PRIMARY KEY (flowKey, flowStart),
	FOREIGN KEY (flowKey, flowStart) REFERENCES Flow(flowKey, flowStart) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT IGNORE INTO ForwardFlowStatistics (flowKey, flowStart, f_minPS, f_maxPS, f_avgPS, f_stdDevPS, f_minPIAT, f_maxPIAT, f_avgPIAT, f_stdDevPIAT, f_flowStart, f_flowEnd, f_flowDuration, f_pktTotalCount, f_octetTotalCount)
SELECT flow_key, flowStart, f_min_ps, f_max_ps, f_avg_ps, f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat, f_flowStart, f_flowEnd, f_flowDuration, f_pktTotalCount, f_octetTotalCount FROM InternetTrafficInternal;

CREATE TABLE BackwardFlowStatistics( 
	flowKey varchar(250) NOT NULL,
	flowStart decimal(40,25) NOT NULL,
	b_minPS int CHECK (b_minPS>=0),
	b_maxPS int CHECK (b_maxPS>=0),
	b_avgPS decimal(40,25) CHECK (b_avgPS>=0),
	b_stdDevPS decimal(40,25) CHECK (b_stdDevPS>=0),
	b_minPIAT decimal(40,25) CHECK (b_minPIAT>=0),
	b_maxPIAT decimal(40,25) CHECK (b_maxPIAT>=0),
	b_avgPIAT decimal(40,25) CHECK (b_avgPIAT>=0),
	b_stdDevPIAT decimal(40,25) CHECK (b_stdDevPIAT>=0),
	b_flowStart decimal(40,25) CHECK (b_flowStart>=0),
	b_flowEnd decimal(40,25) CHECK (b_flowEnd>=0),
	b_flowDuration decimal(40,25) CHECK (b_flowDuration>=0),
	b_pktTotalCount int CHECK(b_pktTotalCount>=0),
	b_octetTotalCount bigint CHECK(b_octetTotalCount>=0),
	PRIMARY KEY (flowKey, flowStart),
	FOREIGN KEY (flowKey, flowStart) REFERENCES Flow(flowKey, flowStart) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT IGNORE INTO BackwardFlowStatistics (flowKey, flowStart, b_minPS, b_maxPS, b_avgPS, b_stdDevPS, b_minPIAT, b_maxPIAT, b_avgPIAT, b_stdDevPIAT, b_flowStart, b_flowEnd, b_flowDuration, b_pktTotalCount, b_octetTotalCount)
SELECT flow_key, flowStart, b_min_ps, b_max_ps, b_avg_ps, b_std_dev_ps, b_min_piat, b_max_piat, b_avg_piat, b_std_dev_piat, b_flowStart, b_flowEnd, b_flowDuration, b_pktTotalCount, b_octetTotalCount FROM InternetTrafficInternal;

CREATE TABLE TotalFlowStatistics( 
	flowKey varchar(250) NOT NULL,
	flowStart decimal(40,25) NOT NULL,
	minPS int CHECK (minPS>=0),
	maxPS int CHECK (maxPS>=0),
	avgPS decimal(40,25) CHECK (avgPS>=0),
	stdDevPS decimal(40,25) CHECK (stdDevPS>=0),
	minPIAT decimal(40,25) CHECK (minPIAT>=0),
	maxPIAT decimal(40,25) CHECK (maxPIAT>=0),
	avgPIAT decimal(40,25) CHECK (avgPIAT>=0),
	stdDevPIAT decimal(40,25) CHECK (stdDevPIAT>=0),
	flowEnd decimal(40,25) CHECK (flowEnd>=0),
	flowDuration decimal(40,25) CHECK (flowDuration>=0),
	pktTotalCount int CHECK(pktTotalCount>=0),
	octetTotalCount bigint CHECK(octetTotalCount>=0),
	PRIMARY KEY (flowKey, flowStart),
	FOREIGN KEY (flowKey, flowStart) REFERENCES Flow(flowKey, flowStart) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT IGNORE INTO TotalFlowStatistics (flowKey, flowStart, minPS, maxPS, avgPS, stdDevPS, minPIAT, maxPIAT, avgPIAT, stdDevPIAT, flowEnd, flowDuration, pktTotalCount, octetTotalCount)
SELECT flow_key, flowStart, min_ps, max_ps, avg_ps, std_dev_ps, min_piat, max_piat, avg_piat, std_dev_piat, flowEnd, flowDuration, pktTotalCount, octetTotalCount FROM InternetTrafficInternal;

CREATE INDEX idx_avgPS on TotalFlowStatistics (avgPS);
CREATE INDEX idx_stdDevPS on TotalFlowStatistics (stdDevPS);
CREATE INDEX idx_avgPIAT on TotalFlowStatistics (avgPIAT);
CREATE INDEX idx_stdDevPIAT on TotalFlowStatistics (stdDevPIAT);
CREATE INDEX idx_flowDuration on TotalFlowStatistics (flowDuration);
CREATE INDEX idx_pktTotalCount on TotalFlowStatistics (pktTotalCount);
CREATE INDEX idx_octetTotalCount on TotalFlowStatistics (octetTotalCount);