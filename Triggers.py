import mysql.connector

con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='trigger_test'
)

cursor = con.cursor()

# DROP triggers jika ada
trigger_names = [
    "insert_grade_trigger", "update_grade_trigger",
    "after_insert_trigger", "after_update_trigger",
    "before_delete_trigger", "after_delete_trigger"
]
for trig in trigger_names:
    cursor.execute(f"DROP TRIGGER IF EXISTS {trig}")

# DROP tables jika ada
cursor.execute("DROP TABLE IF EXISTS mahasiswa")
cursor.execute("DROP TABLE IF EXISTS log_trigger")
con.commit()
print("Existing tables and triggers dropped successfully.")

# CREATE TABLE mahasiswa
cursor.execute("""
CREATE TABLE mahasiswa (
    NIM VARCHAR(13) PRIMARY KEY,
    Nama VARCHAR(100),
    Nilai FLOAT,
    Grade VARCHAR(2)
)
""")

# CREATE TABLE log_trigger
cursor.execute("""
CREATE TABLE log_trigger (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aksi VARCHAR(50),
    keterangan TEXT,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
con.commit()
print("Tables created successfully.")

# TRIGGER: BEFORE INSERT
cursor.execute("""
CREATE TRIGGER insert_grade_trigger BEFORE INSERT ON mahasiswa
FOR EACH ROW
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
""")

# TRIGGER: BEFORE UPDATE
cursor.execute("""
CREATE TRIGGER update_grade_trigger BEFORE UPDATE ON mahasiswa
FOR EACH ROW
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
""")

# TRIGGER: AFTER INSERT
cursor.execute("""
CREATE TRIGGER after_insert_trigger AFTER INSERT ON mahasiswa
FOR EACH ROW
BEGIN
    INSERT INTO log_trigger (aksi, keterangan)
    VALUES ('INSERT', CONCAT('Data baru ditambahkan untuk NIM: ', NEW.NIM));
END
""")

# TRIGGER: AFTER UPDATE
cursor.execute("""
CREATE TRIGGER after_update_trigger AFTER UPDATE ON mahasiswa
FOR EACH ROW
BEGIN
    INSERT INTO log_trigger (aksi, keterangan)
    VALUES ('UPDATE', CONCAT('Data diperbarui untuk NIM: ', NEW.NIM));
END
""")

# TRIGGER: BEFORE DELETE
cursor.execute("""
CREATE TRIGGER before_delete_trigger BEFORE DELETE ON mahasiswa
FOR EACH ROW
BEGIN
    INSERT INTO log_trigger (aksi, keterangan)
    VALUES ('BEFORE DELETE', CONCAT('Akan menghapus data mahasiswa dengan NIM: ', OLD.NIM));
END
""")

# TRIGGER: AFTER DELETE
cursor.execute("""
CREATE TRIGGER after_delete_trigger AFTER DELETE ON mahasiswa
FOR EACH ROW
BEGIN
    INSERT INTO log_trigger (aksi, keterangan)
    VALUES ('AFTER DELETE', CONCAT('Data mahasiswa dengan NIM ', OLD.NIM, ' telah dihapus.'));
END
""")

con.commit()
print("All triggers created successfully.")

# Insert test data
cursor.execute("INSERT INTO mahasiswa (NIM, Nama, Nilai) VALUES ('0806022310001', 'Derick', 90.5)")
cursor.execute("INSERT INTO mahasiswa (NIM, Nama, Nilai) VALUES ('0806022310014', 'Aron', 80.2)")
cursor.execute("INSERT INTO mahasiswa (NIM, Nama, Nilai) VALUES ('0806022310010', 'Deny', 40.2)")
con.commit()

# Update test
cursor.execute("UPDATE mahasiswa SET Nilai = 70.2 WHERE Nama = 'Aron'")
con.commit()

# Delete test
cursor.execute("DELETE FROM mahasiswa WHERE Nama = 'Derick'")
con.commit()

# Tampilkan data mahasiswa
print("\nData mahasiswa setelah operasi:")
cursor.execute("SELECT * FROM mahasiswa")
for row in cursor.fetchall():
    print(f"({row[0]}, {row[1]}, {row[2]}, {row[3]})")

# Tampilkan log trigger
print("\nLog trigger:")
cursor.execute("SELECT aksi, keterangan, waktu FROM log_trigger")
for row in cursor.fetchall():
    print(f"[{row[2]}] {row[0]} - {row[1]}")

cursor.close()
con.close()
