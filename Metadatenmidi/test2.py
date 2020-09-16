import re
from mido import MidiFile
import datetime
import mysql.connector

#mydb = mysql.connector.connect (
#    host="localhost",
#    user="metadb",
#    password="metadata",
#    database="metadata"
#)

files = ["AUD_CT0027.mid"]#, "AUD_AP1435H.mid", "AUD_CT0027.mid", "AUD_DS1189.mid"AUD_AP0164.mid]
for file in files:
    mid = MidiFile(file, clip=True)
    time = round(mid.length)
    time = str(datetime.timedelta(seconds=time))

    print(time)
    varmisc = []
    vardata = ""
    vartitle = ""
    varartist = ""
    vartempo = ""
    varkey = ""
    varurl = ""
    midi_data = []
    for track in mid.tracks:
        midi_data.append(track)
        for msg in mid.tracks[0]:
            midi_data.append(msg)
    midi_data = str(midi_data)
    x = re.search("<meta message.*time=0>", midi_data)
    remove_characters = ["<", ">", "meta message", "time=0", "'"]

    if x:
        a_string = str(x.string)
        for character in remove_characters:
            a_string = a_string.replace(character, "")
        if "track_name" in midi_data:
            print(a_string)
            vartitle = re.search("name=: (.*)", a_string)

        if "key_signature" in midi_data:
            varkey = a_string.replace("key_signature key=", "")
        if "set_tempo" in midi_data:
            var_tempo = re.search(r"set_tempo tempo=(.*?) time=0", midi_data).group(1)
            var_tempo = int(var_tempo)
            var_tempo = round(60000000 / var_tempo, 0)
            print(var_tempo)
        else:
            varmisc.append(a_string)
            miscstr = ",".join(varmisc)
    else:
        pass

    mycursor = mydb.cursor()

    sql = "INSERT INTO data (Dateiname, Titel, Interpret, Tempo, Tonart, URL, Sonstiges) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (vardata, vartitle, varartist, vartempo, varkey, varurl, miscstr)
    mycursor.execute(sql, val)

    mydb.commit()

    #print(mycursor.rowcount, "record inserted.")