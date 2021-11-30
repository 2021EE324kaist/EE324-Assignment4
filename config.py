db_1 = {
    'user'     : 'root',
    'password' : 'zkdltmxm',
    'host'     : '127.0.0.1',
    'port'     : '3306',
    'database' : 'tmp_db'
}

DB_URL_1 = f"mysql+mysqlconnector://{db_1['user']}:{db_1['password']}@{db_1['host']}:{db_1['port']}/{db_1['database']}?charset=utf8" 
