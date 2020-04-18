from src.sqlite_helper import create_message_table, drop_message_table

"""
This script will create a SQLite table for you, and should be one time setup
The table name is message which will store all the Post message 
"""
create_message_table()


"""
If you need to drop the message table, un-comment the following code by removing the # sign in the beginning
"""
#
# drop_message_table()
#
