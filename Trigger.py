import mysql.connector

connector = mysql.connector.connect(
    host = 'localhost',
    username = 'root',
    password = '',
    database = 'trigger_test'
)

cursor = connector.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS mahasiswa (
    NIM VARCHAR(13) PRIMARY KEY,
    Nama VARCHAR(100),
    Nilai FLOAT,
    Grade VARCHAR(2)
)
""")

connector.commit()
print("Table 'mahasiswa' created successfully.")


# BEFORE INSERT DATA 
cursor.execute(
    """
 CREATE TRIGGER IF NOT EXISTS insert_grade_trigger BEFORE INSERT ON mahasiswa FOR EACH ROW
 BEGIN
    SET NEW.Grade = CASE
        WHEN NEW.Nilai >= 90 THEN 'A'
        WHEN NEW.Nilai >= 85 THEN 'A-'
        WHEN NEW.Nilai >= 80 THEN 'B+'
        WHEN NEW.Nilai >= 75 THEN 'B'
        WHEN NEW.Nilai >= 70 THEN 'B-'
        WHEN NEW.Nilai >= 60 THEN 'C+'
        WHEN NEW.Nilai >= 55 THEN 'C'
        WHEN NEW.Nilai >= 45 THEN 'D'
        ELSE 'E'
        END;
END
"""
)

connector.commit()
print("Trigger 'insert_grade_trigger' created successfully.")
# END BEFORE INSTER DATA


# BEFORE UPDATE DATA
cursor.execute(
    """
 CREATE TRIGGER IF NOT EXISTS update_grade_trigger BEFORE UPDATE ON mahasiswa FOR EACH ROW
 BEGIN
    SET NEW.Grade = CASE
        WHEN NEW.Nilai >= 90 THEN 'A'
        WHEN NEW.Nilai >= 85 THEN 'A-'
        WHEN NEW.Nilai >= 80 THEN 'B+'
        WHEN NEW.Nilai >= 75 THEN 'B'
        WHEN NEW.Nilai >= 70 THEN 'B-'
        WHEN NEW.Nilai >= 60 THEN 'C+'
        WHEN NEW.Nilai >= 55 THEN 'C'
        WHEN NEW.Nilai >= 45 THEN 'D'
        ELSE 'E'
        END;
END
"""
)

connector.commit()
print("Trigger 'update_grade_trigger' created successfully.")
# END BEFORE UPDATE DATA

            
#INSERT DATA
cursor.execute("INSERT INTO mahasiswa (NIM, Nama, Nilai) VALUES ('0806022310001', 'Derick', 90.5)")
connector.commit()
print("1 row inserted to table 'mahasiswa' successfully.")

# INSERT DATA
cursor.execute("INSERT INTO mahasiswa (NIM, Nama, Nilai) VALUES ('0806022310014', 'Aron', 80.2)")
connector.commit()
print("1 row inserted to table 'mahasiswa' successfully.")

# PRINT INSERT DI TERMINAL
print("\nData After INPUT:")
cursor.execute("SELECT * FROM mahasiswa")
for row in cursor.fetchall():
    print(f"({row[0]}, {row[1]}, {row[2]}, {row[3]})")


# UPDATE DATA
cursor.execute("UPDATE mahasiswa SET Nilai = 70.2 WHERE Nama = 'Aron'")
connector.commit()
print("1 row updated in table 'mahasiswa' successfully.")

# PRINT UPDATE DI TERMINAL
print("\nData After UPDATE:")
cursor.execute("SELECT * FROM mahasiswa")
for row in cursor.fetchall():
    print(f"({row[0]}, {row[1]}, {row[2]}, {row[3]})")


cursor.close()
connector.close()