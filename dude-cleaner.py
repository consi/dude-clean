#!/usr/bin/env python
import sqlite3
import argparse
import os
import sys
import coloredlogs
import logging
from tqdm import tqdm

#Setup logging
coloredlogs.install(level="INFO")
log = logging.getLogger("main")

class CleanDudeDB(object):
    __DUDE_DB_INIT = """PRAGMA foreign_keys=OFF;
PRAGMA page_size=2048;
PRAGMA application_id=0;
PRAGMA user_version=1;
CREATE TABLE objs (id integer primary key, obj blob);
CREATE TABLE outages (timeAndServiceID integer primary key, serviceID integer, deviceID integer, mapID integer, time integer, status integer, duration integer);
CREATE TABLE chart_values_raw (sourceIDandTime integer primary key, value);
CREATE TABLE chart_values_10min (sourceIDandTime integer primary key, value);
CREATE TABLE chart_values_2hour (sourceIDandTime integer primary key, value);
CREATE TABLE chart_values_1day (sourceIDandTime integer primary key, value);"""
    __DUDE_INDEX = """CREATE INDEX outages_idx_serviceID_time ON outages(serviceID, time);
CREATE INDEX outages_idx_deviceID_time ON outages(deviceID, timeAndServiceID);
CREATE INDEX outages_idx_mapID_time ON outages(mapID, timeAndServiceID);"""
    def __init__(self, source_sqlite, dest_sqlite):
        #Setup logger
        self.log = logging.getLogger("dude-cleaner")
        #Expand paths
        self.source = os.path.expanduser(
            source_sqlite
        )
        self.dest = os.path.expanduser(
            dest_sqlite
        )
        # Check if destination exists
        if os.path.exists(self.dest):
            #Exit if exists
            self.log.critical("Destination file {filename} exists!".format(
                filename = self.dest
            ))
            sys.exit(1)
        else:
            #Run db initialization if this is a new db
            self.log.info("Proceeding with initialization of {filename} db.".format(
                filename = self.dest
            ))
            self.__init_db()
        
        # Now copy data
        self.__copy_data()
        # And do reindex
        self.__reindex()
        self.log.info("Database is hopefully repaired. Output size is: {size}MB, Reduced: {reduced}MB".format(
            size = float(os.path.getsize(self.dest)) / 1024.0 / 1024.0,
            reduced = (
                    float(os.path.getsize(self.source)) - float(os.path.getsize(self.dest))
            ) / 1024.0 / 1024.0
        ))
        # And close databases
        self.source_conn.close()
        self.dest_conn.close()

    def __copy_data(self):
        self.log.info
        self.log.info("Selecting all data from objs from source database")
        count = self.src_cur.execute("SELECT COUNT(*) FROM objs").fetchone()[0]
        self.log.info("Starting database repair.")
        self.src_cur.execute('select * from objs')
        for item in tqdm(self.src_cur, total=count):
            self.dest_cur.execute("insert into objs values (?, ?)", (item[0], item[1]))
        self.dest_conn.commit()

    def __reindex(self):
        self.log.info("Doing database reindex.")
        for query in self.__DUDE_INDEX.split("\n"):
            self.log.info("Query: {query}".format(query=query))
            self.dest_cur.execute(query)
        self.dest_conn.commit()

    def __init_db(self):
        try:
            self.source_conn = sqlite3.connect(self.source)
        except Exception as error:
            self.log.error("Cannot connect to source db {e}".format(
                e=error
            ))
            sys.exit(1)
        try:
            self.dest_conn = sqlite3.connect(self.dest)
        except Exception as error:
            self.log.error("Cannot create destination db {e}".format(
                e=error
            ))
            sys.exit(1)
        self.log.info("Proceeding with schema init.")
        self.dest_cur = self.dest_conn.cursor()
        self.src_cur = self.source_conn.cursor()
        for query in self.__DUDE_DB_INIT.split("\n"):
            self.log.info("Query: {query}".format(query=query))
            self.dest_cur.execute(query)
        self.dest_conn.commit()

if __name__ == "__main__":
    log.info("dude-cleaner.py - Dude database cleanup script - Marek Wajdzik <wajdzik.m@gmail.com> - 2018")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--source",
        help="Source dude database file", required=True
    )
    parser.add_argument(
        "-d", "--dest",
        help="Destination dude database file", required=True
    )
    args = parser.parse_args()
    CleanDudeDB(args.source, args.dest)