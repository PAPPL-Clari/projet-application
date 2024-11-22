import psycopg2
import config
import getDiplomaInfo

conn = psycopg2.connect(database = {config.database}, 
                        user = {config.user}, 
                        host= {config.host},
                        password = {config.password},
                        port = {config.port})

# Open a cursor to perform database operations
cur = conn.cursor()

(id_diplome, ref_diplome, nom_diplome, parcours,
 nom_specialisation,
 nom_ecole, acronyme_pays_ecole) = getDiplomaInfo(78)

print(getDiplomaInfo(78))

'''
# Execute a command: create datacamp_courses table
cur.execute("""INSERT INTO specialisation (id_specialisation, nom_specialisation)
            VALUES (0, nom_specialisation)
            """)
'''

# Make the changes to the database persistent
#conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()
