# -*- coding: utf-8 -*-
import MySQLdb


conn = MySQLdb.connect('localhost', 'root', '', 
                                    'tutorialdb', charset="utf8",
                                    use_unicode=True)
cursor = conn.cursor()
        

cursor.execute("Select * from courses order by CID")
courses = cursor.fetchall()
for course in courses:    
    des = str(course[6]).stipe().replace("[","").replace("]","").replace("','","").replace("'","")        
cursor.execute("""update courses set description = %s where cid = %s""", 
                       (des,
                        str(course[0])))            
conn.commit()
