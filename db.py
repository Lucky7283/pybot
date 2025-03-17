import mysql.connector
from functions import times
case={
    'host':'localhost',
    'user':'root',
    'password':'Q1w2e3r4t5y6u7i8o9p0',
    'database':'test'
}
def w(message):
    try:
        with mysql.connector.connect(**case) as conn:
            with conn.cursor() as cursor:
                tm=times()
        
                query='''
                    INSERT INTO chathistory 
                    (user_id, username, first_name, last_name, message, messsage_type, time) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    '''
                if message.text:
                    values=(
                        message.from_user.id,
                        message.from_user.username,
                        message.from_user.first_name,
                        message.from_user.last_name,
                        message.text,
                        message.content_type,
                        tm
                )
                elif message.caption:
                    values=(
                        message.from_user.id,
                        message.from_user.username,
                        message.from_user.first_name,
                        message.from_user.last_name,
                        message.caption,
                        message.content_type,
                    tm
                )
                else:
                    values=(
                        message.from_user.id,
                        message.from_user.username,
                        message.from_user.first_name,
                        message.from_user.last_name,
                        "multimedia",
                        message.content_type,
                        tm
                    )
                cursor.execute(query,values)
                conn.commit()
    except Exception as e:
        print(f'Error as database: {e}')
