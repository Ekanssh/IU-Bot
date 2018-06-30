#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
A class for using database with aiopg

Attributes:
    Funtions:
        .connect:
            Help:
                Connects to our only heroku database.
            Arguments:
                Does not take any arguments. The database information used is for the only database we are using.

        .execute:
            Help:
                Executes a given SQL statement with optional arguments.
            Arguments:
                statement:
                    The statement to execute
                args:
                    The arguments for the SQL statements to run with. No fear of SQL injections!!
            Example Usage:
                await aio.execute("SELECT * FROM Dailies WHERE id = %s", (360022804357185537, ))  #Where `aio` is an instance of this class.
    Variables:
        .conn:
            stores the `Connection` object of the instance. You mostly do not need it.
        .cursor:
            stores the `Cursor` object of the Connection
"""

import aiopg
import os


class aiopg_commands:
    async def connect(self):
        #self.dsn = "dbname=d1b1qi3p5efneq user=ynhburlpfyrfon password=14e33018bf4991471bae5c11d2d57ab4424120299510a7891e61ee0123e81bc8 host=ec2-79-125-117-53.eu-west-1.compute.amazonaws.com"
        self.conn = await aiopg.connect(database=os.getenv('DATABASE'),
                                        user=os.getenv('USER'),
                                        password=os.getenv('PASSWORD'),
                                        host=os.getenv('HOST'))
        self.cursor = await self.conn.cursor()
        # self.pool = await aiopg.create_pool(self.dsn)

    async def execute(self, statement, args: tuple = None):
        if args is None:
            await self.cursor.execute(statement)
        else:
            await self.cursor.execute(statement, args)
