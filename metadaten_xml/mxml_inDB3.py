import mysql.connector
from music21 import *




#Verbindung zum Server
mydb = mysql.connector.connect(
        host="localhost",
        user="MusikDBNutzer",
        password="test",
        database="musiksuchmaschine"
    )
#öffnet xml oder mxml und wandelt es in einen music21 Stream

files=["1Certon-A_ce_matin.mxl"]


for file in files:
    score = converter.parse(file)

#das Stream Objekt verfügt über Metadaten print nur für den fall von fehlern als kontrolle
#https://web.mit.edu/music21/doc/moduleReference/moduleMetadata.html?#module-music21.metadata
#print(score.metadata.title)
#print(score.metadata.composer)
#print(score.metadata.date)
#print(score.metadata.all())
#print(score.duration)

#einzelen Variablen mit den entsprechenden Metadaten befüllen
    varTitle = score.metadata.title
    varComposer = score.metadata.composer
    varSonstiges = score.metadata.all()
    varSonstiges = str(varSonstiges)

#secondsMap zeigt alles an, was in Sekdunen angegeben wurde
#print(score.secondsMap)

# zeigt alles an, was irgendwie mit dem Tempo zu tun hat
#print(score.metronomeMarkBoundaries())
#print(varTitle)

#trägt Komponist in DB ein hier mit zwei Mal gleicher Code, eigentlich sollte es auch
#mit einem mycursor(multi=True) gehen, führte hier aber zu leeren Einträgen
    if varComposer != None:
        mycursor = mydb.cursor()
        sql = "INSERT INTO kuenstler (ID, Name) VALUES (NULL, %s)"
        val = (varComposer,)
        mycursor.execute(sql, val,)
        mydb.commit()

    # findet ID des Kuenstlers des aktuellen Stückes heraus
    #funktioniert noch nicht so ganz, weil er einen Touple rauswirft
    if varTitle != None:
        mycursor = mydb.cursor()
        sql = "SELECT ID FROM kuenstler WHERE Name = %s"
        val = (varComposer,)
        mycursor.execute(sql, val, )
        myresult = mycursor.fetchall()
        myresult = str(myresult[0])



    #Trägt Titel in DB ein
    #hier klappt es mit der Künstler ID noch nicht, weil er oben einen Touple rauswirft
    if varTitle != None:
        mycursor = mydb.cursor()
        sql = "INSERT INTO musikstueck (ID, Kuenstler_ID, Name, Sonstiges) VALUES (Null, %s, %s, %s)"
        val = (varTitle,myresult, varSonstiges)
        mycursor.execute(sql, val,)
        mydb.commit()

    #was jetzt noch fehlt: wie trage ich die Künstler ID richtig dem Musikstück ein?
    #wie regeln wir es, dass Künstler nicht doppelt eingetragen werden?
    #BPM, Länge 











