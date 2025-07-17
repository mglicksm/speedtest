# 
# Updated to use MariaDB by Copilot
# TODO: I don't think this is date/time stamped. I think InfluxDB automatically does that. 
#       Have not tried or tested it. 
#
import re
import subprocess
import mariadb

def execute_speedtest():
    try:
        # Execute speedtest-cli command
        response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        
        # Extract ping, download, and upload speeds
        ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)[0].replace(',', '.')
        download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)[0].replace(',', '.')
        upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)[0].replace(',', '.')

        return float(ping), float(download), float(upload)
    except Exception as e:
        print(f"Error executing speedtest: {e}")
        return None, None, None

def insert_speed_data(cursor, ping, download, upload):
    try:
        # Insert speed data into the database
        cursor.execute("INSERT INTO internetspeed (ping, download, upload) VALUES (?, ?, ?)", (ping, download, upload))
    except Exception as e:
        print(f"Error inserting speed data: {e}")

def main():
    try:
        # Connect to MariaDB
        conn = mariadb.connect(
            user="speedmonitor",
            password="yy78UUn&hh",
            host="qnap.local",
            port=3307,
            database="internetspeed"
        )
        cursor = conn.cursor()

        # Execute speedtest and get speed data
        ping, download, upload = execute_speedtest()

        if ping is not None and download is not None and upload is not None:
            # Insert speed data into the database
            insert_speed_data(cursor, ping, download, upload)
            conn.commit()
            print("Speed data inserted successfully.")
        else:
            print("Error getting speed data.")

        # Close the connection
        conn.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")

if __name__ == "__main__":
    main()