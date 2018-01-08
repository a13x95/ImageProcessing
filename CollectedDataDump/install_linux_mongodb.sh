#!/bin/bash
command -v mongod
if [ $? -eq 1 ]; then
    echo "Installing MongoDB for the first time..."
    cd /home/$(whoami)
    echo "Downloading archive..."
    curl -Ov https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.1.tgz
    tar -zxvf mongodb-linux-x86_64-3.6.1.tgz
    echo "Unarchiving..."
    rm -f mongodb-linux-x86_64-3.6.1.tgz
    mv mongodb-linux-x86_64-3.6.1 mongodb
    echo "Exporting environment variable..."
    echo -e "export PATH=$PATH:$(pwd)/mongodb/bin\n" >> ~/.bashrc
    echo -e "PATH=$PATH:$(pwd)/mongodb/bin\n" >> ~/.profile
    chmod +x ~/.bashrc
    chmod +x ~/.profile
    echo "Creating necessary directory for MongoDB data.."
    sudo mkdir -p /data/db
    sudo chmod o+rwx /data/db
    echo "Starting mongod daemon process..."
    sudo systemctl start mongod
    sudo systemctl enable mongod
    sudo systemctl status mongod
    echo "Done installing MongoDB"
else
    echo "MongoDB identified"
fi
