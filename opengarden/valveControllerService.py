import time
import sqlite3 
from sqlite3 import Error
import RPi.GPIO as GPIO
from datetime import datetime

relayin1=2
relayin2=3
relayin3=4
relayin4=17

def setupRasbperry():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(relayin1,GPIO.OUT)
    GPIO.setup(relayin2,GPIO.OUT)
    GPIO.setup(relayin3,GPIO.OUT)
    GPIO.setup(relayin4,GPIO.OUT)

    GPIO.output(relayin1,True)
    GPIO.output(relayin2,True)
    GPIO.output(relayin3,True)
    GPIO.output(relayin4,True)
    

def checkWateringStatus():
    print("checkWateringStatus")
    conn=getConnection()
    conn.row_factory=sqlite3.Row
    params=('pending','started')
    # date(date_from)>=date('now') 
    for row in conn.execute("SELECT * FROM watering_schedule WHERE 1=1 and status=? or status=?",params):
        print("==============================")
        print("date_from ",row["date_from"])
        print("date_to",row["date_to"])
        print("zone_id",row["zone_id"])
        print("status",row["status"])

        date_from=datetime.strptime(str(row["date_from"]),'%Y-%m-%d %H:%M:%S')
        date_to=datetime.strptime(str(row["date_to"]),'%Y-%m-%d %H:%M:%S')
        print(f'date_from formatted: {date_from} date_to formatted: {date_to} ')

        #compare the date from database with the system date       
        now=datetime.now()
        print("now: "+str(now))
        current_time_formatted=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'current time formatted: {current_time_formatted}')

        # t1=datetime(year=now.year,month=now.month,hour=now.hour,minute=now.minute)
        # t2=datetime(year=date_from.year,month=date_from.month,hour=date_from.hour,minute=date_from.minute)    

        print(f'current_date tstamp: {now.timestamp()},  date_from tstamp {date_from.timestamp()}, date_to tstamp: {date_to.timestamp()}')
    
        if(str(row['status'])=='pending' and now.timestamp()>=date_from.timestamp()):
            print("starting watering")
            print("zone: ", row["zone_id"])
            print("starting on: ",current_time_formatted)
            updateWatering(conn,"started",row["watering_id"])
            GPIO.output(relayin1,False)
            GPIO.output(relayin2,False)

        elif(str(row['status'])=='started' and now.timestamp()>=date_to.timestamp()):
            print("finish watering")
            print("zone: ", row["zone_id"])
            print("finshed on: ",current_time_formatted)
            updateWatering(conn,"completed",row["watering_id"])
            GPIO.output(relayin1,True)
            GPIO.output(relayin2,True)
        else:
            GPIO.output(relayin1,True)
            GPIO.output(relayin2,True)
        
    
    if(conn):
        conn.close()

    
def updateWatering(conn,status,watering_id):
    print("update watering")
    print(f'watering_id: {watering_id} status: {status}')
    params=(status,watering_id)
    try:
        with conn:
            #conn.execute(f"UPDATE watering_schedule set status='{status}' WHERE watering_id={watering_id}")
            conn.execute("UPDATE watering_schedule set status=? WHERE watering_id=?",params)
            conn.commit()
    except sqlite3.IntegrityError as error:
        print("couldn't update data")
        print(error)
    # finally:
    #     if(conn):
    #         conn.close()
    #         print("close connection ")


def createTestData():
    #[('2020-11-21 22:54:46', '2020-11-21 22:54:46', 1, 5, 'pending')]
    watering_schedule=[('2020-11-21 22:54:46', '2020-11-21 22:54:46', 5, 'pending'),('2020-11-21 22:54:46', '2020-11-21 22:54:46', 5, 'pending'),('2020-11-21 22:54:46', '2020-11-21 22:54:46', 5, 'pending')]

    conn=getConnection()
    c=conn.cursor()

    c.executemany("INSERT INTO watering_schedule(date_from,date_to,zone_id,status) VALUES(?,?,?,?)",watering_schedule)
    conn.commit()
    print(c.rowcount)

def createTestDataWithContextManager():
    watering_schedule=[('2020-11-21 22:54:46', '2020-11-21 22:54:46', 5, 'pending'),('2020-11-21 22:54:46', '2020-11-21 22:54:46', 5, 'pending'),('2020-11-21 22:54:46', '2020-11-21 22:54:46', 5, 'pending')]

    conn=getConnection()
    try:
        with conn:
            conn.executemany("INSERT INTO watering_schedule(date_from,date_to,zone_id,status) VALUES(?,?,?,?)",watering_schedule)
        
    except sqlite3.IntegrityError:
        print("Couldn't add the data")

def insertWatering(date_from,date_to,zone_id,status):
    watering_schedule=[(date_from,date_to,zone_id,status)]
    conn=getConnection()
    try:
        with conn:
            conn.executeMany("INSERT INTO watering_schedule(date_from,date_to,zone_id,status) VALUES(?,?,?,?)",watering_schedule)
    except sqlite3.IntegrityError:
        print("Couldn't add the data to watering schedule")        
    
def testConnection():
    print("sqlite info")
    print("library ",sqlite3.version)
    print("runtime ",sqlite3.sqlite_version)
    conn=sqlite3.connect('/home/pi/openwatering.db')

    status=('pending',)

    c=conn.cursor()
    c.execute('SELECT * FROM watering_schedule WHERE status=?',status)

    print(c.fetchall());


def getConnection():
    conn=None
    try: 
        conn=sqlite3.connect('/home/pi/openwatering.db')
    except Error as e:
        print("Couldn't get connection ")
        print(e)
    return conn


if __name__ == "__main__":
    while (True):        
        setupRasbperry()
        # testConnection()
        # createTestData()
        # createTestDataWithContextManager()
        checkWateringStatus()
        time.sleep(60)
