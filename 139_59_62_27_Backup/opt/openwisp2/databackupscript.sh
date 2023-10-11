#!/bin/bash

sourcehost="139.59.65.241"
sourceuser="root"
influxdb="/var/lib/influxdb"
dbsqlite3="/opt/openwisp2/db.sqlite3"


destinationhost="45.118.161.229"
destinationuser="ubuntu"
destinationdirectory="/home/ubuntu/NMS_Bkup_139_Server"       #as per our requirement create directory in destination
password="r1qtOQ8i%587"

 current_date=$(date +%Y-%m-%d-%H-%M)
logdirectory="/root/backup_log"
logfile="$logdirectory/$current_date.txt"

# Function to log messages to the log file
log_message() {
    echo "$(date +%Y-%m-%d-%H-%M) - $1" >> "$logfile"
}

log_message "Backup script execution started."

# Create directory on the destination host with the current date
sshpass -p "$password" ssh $destinationuser@$destinationhost "mkdir -p $destinationdirectory/$current_date" \
    && log_message "Created directory $destinationdirectory/$current_date on the destination host." \
    || log_message "Failed to create directory $destinationdirectory/$current_date on the destination host."

# Compress the source files

sudo tar -czf influxdb.tar.gz $influxdb \
    && log_message "Compressed source files to /tmp/source_files.tar.gz." \
    || log_message "Failed to compress source files."
    
    sudo tar -czf dbsqlite3.tar.gz $dbsqlite3 \
    && log_message "Compressed source files to /tmp/source_files.tar.gz." \
    || log_message "Failed to compress source files."


# Copy the compressed source file to the destination host
sshpass -p "$password" scp influxdb.tar.gz dbsqlite3.tar.gz $destinationuser@$destinationhost:$destinationdirectory/$current_date \
    && log_message "Copied source_files.tar.gz to $destinationdirectory/$current_date on the destination host." \
    || log_message "Failed to copy source_files.tar.gz to $destinationdirectory/$current_date on the destination host."

# Remove the temporary compressed file
rm influxdb.tar.gz
rm dbsqlite3.tar.gz

# Remove directories on the destination host older than 30 days
sshpass -p "$password" ssh $destinationuser@$destinationhost "find $destinationdirectory -type d -mtime +30 -exec rm -rf {} \;" \
    && log_message "Removed directories older than 30 days from $destinationdirectory on the destination host." \
    || log_message "Failed to remove directories older than 30 days from $destinationdirectory on the destination host."

# Log script execution end
log_message "Backup script execution completed."

# Remove old log files
find "$logdirectory" -name "*.txt" -mtime +30 -exec rm {} \;

