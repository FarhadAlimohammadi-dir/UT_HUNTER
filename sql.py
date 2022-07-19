import requests
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse,parse_qs,urlencode
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import engine
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from engine import *
from sess import *
from log import *


errors = [
    "error executing",
    "Warning.",
    "SQL syntax",
    "you have an error in this sql Syntax;",
    "warning: mysql",
    "SQL syntax.*?MySQL",
    "Warning.*?\Wmysqli?_",
    "MySQLSyntaxErrorException",
    "valid MySQL result",
    "check the manual that (corresponds to|fits) your MySQL server version",
    '''check the manual that (corresponds to|fits) your MariaDB server version fork="MariaDB" ''',
    '''check the manual that (corresponds to|fits) your Drizzle server version fork="Drizzle" ''',
    "Unknown column '[^ ]+' in 'field list'",
    "MySqlClient\.",
    "com\.mysql\.jdbc",
    "Zend_Db_(Adapter|Statement)_Mysqli_Exception",
    "Pdo[./_\\]Mysql",
    "MySqlException",
    "SQLSTATE\[\d+\]: Syntax error or access violation",
    '''MemSQL does not support this type of query fork="MemSQL"''',
    '''is not supported by MemSQL" fork="MemSQL"''',
    '''unsupported nested scalar subselect" fork="MemSQL"''',
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "PostgreSQL.*?ERROR",
    "Warning.*?\Wpg_",
    "valid PostgreSQL result",
    "Npgsql\.",
    "PG::SyntaxError:",
    "org\.postgresql\.util\.PSQLException",
    "ERROR:\s\ssyntax error at or near",
    "ERROR: parser: parse error at or near",
    "PostgreSQL query failed",
    "org\.postgresql\.jdbc",
    "Pdo[./_\\]Pgsql",
    "PSQLException",
    "Driver.*? SQL[\-\_\ ]*Server",
    "OLE DB.*? SQL Server",
    "\bSQL Server[^&lt;&quot;]+Driver",
    "Warning.*?\W(mssql|sqlsrv)_",
    "SQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}",
    "System\.Data\.SqlClient\.(SqlException|SqlConnection\.OnError)",
    "(?s)Exception.*?\bRoadhouse\.Cms\.",
    "Microsoft SQL Native Client error '[0-9a-fA-F]{8}",
    "\[SQL Server\]",
    "ODBC SQL Server Driver",
    "ODBC Driver \d+ for SQL Server",
    "SQLServer JDBC Driver",
    "com\.jnetdirect\.jsql",
    "macromedia\.jdbc\.sqlserver",
    "Zend_Db_(Adapter|Statement)_Sqlsrv_Exception",
    "com\.microsoft\.sqlserver\.jdbc",
    "Pdo[./_\\](Mssql|SqlSrv)",
    "SQL(Srv|Server)Exception",
    "Unclosed quotation mark after the character string",
    "Microsoft Access (\d+ )?Driver",
    "JET Database Engine",
    "Access Database Engine",
    "ODBC Microsoft Access",
    "Syntax error \(missing operator\) in query expression",
    "\bORA-\d{5}",
    "Oracle error",
    "Oracle.*?Driver",
    "Warning.*?\W(oci|ora)_",
    "quoted string not properly terminated",
    "SQL command not properly ended",
    "macromedia\.jdbc\.oracle",
    "oracle\.jdbc",
    "Zend_Db_(Adapter|Statement)_Oracle_Exception",
    "Pdo[./_\\](Oracle|OCI)",
    "OracleException",
    "CLI Driver.*?DB2",
    "DB2 SQL error",
    "\bdb2_\w+\(",
    "SQLCODE[=:\d, -]+SQLSTATE",
    "com\.ibm\.db2\.jcc",
    "Zend_Db_(Adapter|Statement)_Db2_Exception",
    "Pdo[./_\\]Ibm",
    "DB2Exception",
    "ibm_db_dbi\.ProgrammingError",
    "Warning.*?\Wifx_",
    "Exception.*?Informix",
    "Informix ODBC Driver",
    "ODBC Informix driver",
    "com\.informix\.jdbc",
    "weblogic\.jdbc\.informix",
    "Pdo[./_\\]Informix",
    "IfxException",
    "Dynamic SQL Error",
    "Warning.*?\Wibase_",
    "org\.firebirdsql\.jdbc",
    "Pdo[./_\\]Firebird",
    "SQLite/JDBCDriver",
    "SQLite\.Exception",
    "(Microsoft|System)\.Data\.SQLite\.SQLiteException",
    "Warning.*?\W(sqlite_|SQLite3::)",
    "\[SQLITE_ERROR\]",
    "SQLite error \d+:",
    "sqlite3.OperationalError:",
    "SQLite3::SQLException",
    "org\.sqlite\.JDBC",
    "Pdo[./_\\]Sqlite",
    "SQLiteException",
    "SQL error.*?POS([0-9]+)",
    "Warning.*?\Wmaxdb_",
    "DriverSapDB",
    "-3014.*?Invalid end of SQL statement",
    "com\.sap\.dbtech\.jdbc",
    "\[-3008\].*?: Invalid keyword or missing delimiter",
    "Warning.*?\Wsybase_",
    "Sybase message",
    "Sybase.*?Server message",
    "SybSQLException",
    "Sybase\.Data\.AseClient",
    "com\.sybase\.jdbc",
    "Warning.*?\Wingres_",
    "Ingres SQLSTATE",
    "Ingres\W.*?Driver",
    "Exception (condition )?\d+\. Transaction rollback",
    "com\.frontbase\.jdbc",
    "Syntax error 1. Missing",
    "(Semantic|Syntax) error [1-4]\d{2}\.",
    "Unexpected end of command in statement \[",
    "Unexpected token.*?in statement \[",
    "org\.hsqldb\.jdbc",
    "org\.h2\.jdbc",
    "\[42000-192\]",
    "![0-9]{5}![^\n]+(failed|unexpected|error|syntax|expected|violation|exception)",
    "\[MonetDB\]\[ODBC Driver",
    "nl\.cwi\.monetdb\.jdbc",
    "Syntax error: Encountered",
    "org\.apache\.derby",
    "ERROR 42X01",
    ", Sqlstate: (3F|42).{3}, (Routine|Hint|Position):",
    "/vertica/Parser/scan",
    "com\.vertica\.jdbc",
    "org\.jkiss\.dbeaver\.ext\.vertica",
    "com\.vertica\.dsi\.dataengine",
    "com\.mckoi\.JDBCDriver",
    "com\.mckoi\.database\.jdbc",
    "&lt;REGEX_LITERAL&gt;",
    "com\.facebook\.presto\.jdbc",
    "io\.prestosql\.jdbc",
    "com\.simba\.presto\.jdbc",
    "UNION query has different number of fields: \d+, \d+",
    "Altibase\.jdbc\.driver",
    "com\.mimer\.jdbc",
    "Syntax error,[^\n]+assumed to mean",
    "io\.crate\.client\.jdbc",
    "encountered after end of query",
    "A comparison operator is required here",
    "Syntax error",
    "rdmStmtPrepare\(.+?\) returned",
    "SQ074: Line \d+:",
    "SR185: Undefined procedure",
    "SQ200: No table ",
    "Virtuoso S0002 Error",
    "\[(Virtuoso Driver|Virtuoso iODBC Driver)\]\[Virtuoso Server\]",
]


class sql:

    def __init__(self):
        self.proxy_type = 0
        self.headers = ''
        self.payload = "'"


    def setInfo(self,headers,proxy_type):
        self.proxy_type = proxy_type
        self.headers = headers


    def detect_sql_error(self,txt: str):

        txt = txt.lower()

        for err in errors:
            if err.lower() in txt:
                return True
        return False



    def sql_get_param(self,url: str):
        sess = self.sess()

        if '&' not in url:
            return

        parsed = urlparse.urlparse(url)
        querys = parsed.query.split("&")

        new_query = "&".join(["{}{}".format(query, self.payload) for query in querys])
        parsed = parsed._replace(query=new_query)
        url = urlparse.urlunparse(parsed)

        Log.warning("Found link GET Method: " + url)

        if not url.startswith("mailto:") and not url.startswith("tel:"):
            req = sess.get(url, verify=False)
            if self.detect_sql_error(req.text):
                Log.high("Detected SQL (GET) at " + req.url)
                file = open("sql_get_params.txt", "a+")
                file.write(str(req.url) + "\n")
                file.close()

            else:
                Log.info("Page using GET method but SQL vulnerability not found")
        else:
            pass



    def sql_post(self,url):

        sess = self.sess()

        txt = sess.get(url).text

        bsObj = BeautifulSoup(txt, "html.parser")
        forms = bsObj.find_all("form", method=True)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = url

            if form["method"].lower().strip() == "post":

                Log.warning("Url using POST method SQL: " + url)
                Log.info("getting fields ...")

                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key["type"] == "submit":
                            Log.info("Form key name: " +  key["name"] + " value: " +  "<Submit Confirm>")
                            keys.update({key["name"]: key["name"]})

                        else:
                            Log.info("Form key name: " +  key["name"] + " value: " +  self.payload)
                            keys.update({key["name"]: self.payload})

                    except Exception as e:
                        Log.info("Internal error: " + str(e))


                Log.info("Sending SQL payload (POST) method ..")
                req = sess.post(urljoin(url, action), data=keys)
                if self.detect_sql_error(req.text):
                    Log.high("Detected SQL (POST) at " + urljoin(url, action))
                    file = open("sql_post.txt", "a+")
                    file.write(str(urljoin(url, action)) + "\n" + str(keys) + '\n\n')
                    file.close()
                    Log.high("Post data: " + str(keys))
                else:
                    Log.info("Page using POST method but SQL vulnerability not found")



    def sql_get_form(self,url):

        sess = self.sess()
        txt = sess.get(url).text

        #print(txt)

        bsObj = BeautifulSoup(txt, "html.parser")
        forms = bsObj.find_all("form", method=True)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = url

            if form["method"].lower().strip() == "get":

                Log.warning("Url using GET method SQL: "  + urljoin(url, action))
                Log.info("Getting inputs ...")

                keys = {}
                for key in form.find_all(["input", "textarea"]):
                    try:
                        if key["type"] == "submit":
                            keys.update({key["name"]: key["name"]})

                        else:
                            keys.update({key["name"]: self.payload})

                    except Exception as e:
                        Log.info("Internal error: " + str(e))
                        try:
                            keys.update({key["name"]: self.payload})
                        except KeyError as e:
                            Log.info("Internal error: " + str(e))

                Log.info("Sending payload (GET) method...")

                req = sess.get(urljoin(url, action), params=keys)
                if self.detect_sql_error(req.text):
                    Log.high("Detected SQL (GET) at " + url)
                    file = open("sql_get.txt", "a+")
                    file.write(str(urljoin(url, action)) + "\n\n")
                    file.close()
                    Log.high("GET data: " + str(keys))
                else:
                    Log.info("Page using GET_FORM method but SQL vulnerability not found")


    def sess(self):

        if self.proxy_type == 4:
            session = sess(self.headers)

        else:
            session = sessProxy(self.headers,self.proxy_type)

        return session