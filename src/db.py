
import sqlite3
import re
from numpy import extract
import pandas as pd
import os
from logs import Log


class DB:
    def __init__(self):
        self.db_file = 'temp.db'
        self.file = None

        CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.temp_file = f'{CURRENT_DIR}/temp/temp.sql'
        self.log = Log()

    def make_sqlite3_connection(self):
        try:
            self.con = sqlite3.connect(self.db_file)
            self.cursor = self.con.cursor()
        except:
            os.mkdir(self.db_file)
        finally:
            self.con = sqlite3.connect(self.db_file)
            self.cursor = self.con.cursor()

    def clear_sqlite3_connection(self):
        self.con.close()
        os.remove(self.db_file)

    def mysql_to_sqlite_types(column_types, sqlite_types):
        # Convert mysql types to sqlite types
        new_types = []
        for column_type in column_types:
            if column_type in sqlite_types:
                new_types.append(sqlite_types[column_type])
            else:
                new_types.append("TEXT")
        return new_types
    
    def remove_escape_characters_from_list(self, string_list):
        concatenated_string = ' '.join(string_list)  # Join all elements into one string
        
        cleaned_string = re.sub(r',\s+\)', r')', concatenated_string)
        cleaned_list = cleaned_string.split(';')  # Split back into list if needed
        cleaned_list = [string + ';' for string in cleaned_list if string.strip()]

        
        return cleaned_list


    def convert_to_sqlite(self, sql_list):
        type_mapping = {
            'TINYINT': 'INTEGER',
            'SMALLINT': 'INTEGER',
            'MEDIUMINT': 'INTEGER',
            'BIGINT': 'INTEGER',
            'UNSIGNED INT': 'INTEGER',
            'FLOAT': 'REAL',
            'DOUBLE': 'REAL',
            'DECIMAL': 'NUMERIC',
            'NUMERIC': 'NUMERIC',
            'CHAR': 'TEXT',
            'VARCHAR': 'TEXT',
            'VARTEXT': 'TEXT',
            'TINYTEXT': 'TEXT',
            'TEXT': 'TEXT',
            'MEDIUMTEXT': 'TEXT',
            'LONGTEXT': 'TEXT',
            'BLOB': 'BLOB',
            'TINYBLOB': 'BLOB',
            'MEDIUMBLOB': 'BLOB',
            'LONGBLOB': 'BLOB',
            'BOOLEAN': 'INTEGER',
            'DATE': 'TEXT',
            'TIME': 'TEXT',
            'TIMESTAMP': 'TEXT',
            'DATETIME': 'TEXT',
            'ENUM': 'TEXT',
            'SET': 'TEXT',
            'YEAR': 'INTEGER',
            'JSON': 'TEXT',
        }

        keyword_mapping = {
        'AUTO_INCREMENT': 'AUTOINCREMENT',
        'INT NOT NULL AUTOINCREMENT': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'ENGINE=INNODB': '',
        'DEFAULT CHARSET=utf8': '',
        'CHARACTER SET utf8': '',
        'COLLATE utf8_bin': '',
        'ON UPDATE CURRENT_TIMESTAMP': '',
        'USING BTREE': ''
        }

        converted_list = []
        for sql in sql_list:
            for mysql_type, sqlite_type in type_mapping.items():
                sql = sql.replace(mysql_type, sqlite_type)

            for mysql_keyword, sqlite_keyword in keyword_mapping.items():
                sql = sql.replace(mysql_keyword, sqlite_keyword)            
            
            converted_list.append(sql)

        return converted_list
    
    def parse_sqlite3(self, file):
            
            self.make_sqlite3_connection()
            cols = self.extract_column_names(file)
            #connection_string = f'sqlite:///{file}'
            try:
                with open(file, 'r') as sql_file:
                    sql_query = sql_file.read()
                
                sqlCommands= sql_query.split(';')
                for command in sqlCommands:
                    command = command.strip()
                    try:
                        self.cursor.execute(command)
                    except sqlite3.OperationalError as msg:
                        self.log.error(f'Command skipped: {msg}')

                    table_name_query = "SELECT name FROM sqlite_master WHERE type='table';"
                    table_names = self.cursor.execute(table_name_query).fetchall()

                    if table_names:
                        
                        dfs = []
                        for table_name in table_names:
                            table_name = table_name[0]
                                                        
                            df = pd.read_sql(f'SELECT * FROM {table_name}', self.con)
                            dfs.append(df)
                        if dfs:
                            # Concatenate all dataframes if there are multiple tables
                            df = pd.concat(dfs, ignore_index=True)
                        else:
                            df = pd.DataFrame()
                    else:
                        df = pd.DataFrame()
                
               
                if 'name' in df.columns and 'seq' in df.columns:
                    df = df.drop(columns=['name', 'seq'])
                    
                self.log.info(f'DF Columns: {df.columns}')
                self.log.info(f'DataFrame: {df}')
                self.clear_sqlite3_connection()
                return df
            except Exception as e:
                print(f"An error occurred while parsing SQL file: {e}")
                return None
            
    def extract_column_names(self, sql_file):
        # Read the SQL file
        with open(sql_file, 'r') as file:
            sql_script = file.read()

        # Find all CREATE TABLE statements
        create_table_statements = re.findall(r'CREATE TABLE \w+ \((.*?)\);', sql_script, re.DOTALL)

        # Initialize an empty list to store column names
        column_names = []

        # Iterate over each CREATE TABLE statement
        for statement in create_table_statements:
            # Extract column definitions
            columns = re.findall(r'\s*(\w+)\s+\w+', statement)
            # Add column names to the list
            column_names.extend(columns)

        return column_names
           
    def parse_mysql(self, mysql_file):
        with open(mysql_file, 'r') as file:
            data = file.read()
            new_data = []
            for lines in data:
                data = re.sub(r'PRIMARY KEY\s*\(([^)]+)\)', '', data)
            new_data.append(data)
        cleaned_data = self.remove_escape_characters_from_list(new_data)

        result = self.convert_to_sqlite(cleaned_data)
        
        
        with open(self.temp_file, 'w') as temp:
                self.log.info(f'Writing file: {self.temp_file}')
                temp.writelines(result)

        return self.parse_sqlite3(self.temp_file)      

        
        

    def parse_postgresql(self, host, user, password, database):
        pass
        

       