#!/bin/bash

: ${PYTHON_COMMAND_FILE:?"Please set the PYTHON_COMMAND_FILE variable!"}
: ${PYTHON_COMMAND_FILE_FOLDER:?"Please set the PYTHON_COMMAND_FILE_FOLDER variable!"}
: ${PYTHON_COMMAND_FILE_PARAMS:?"Please set the PYTHON_COMMAND_FILE_PARAMS variable!"}
: ${PYTHON_COMMAND_PID_FILENAME:?"Please set the PYTHON_COMMAND_PID_FILENAME variable!"}
: ${PYTHON_COMMAND_PID_FOLDER:?"Please set the PYTHON_COMMAND_PID_FOLDER variable!"}

cd $PYTHON_COMMAND_FILE_FOLDER
nohup /usr/bin/python $PYTHON_COMMAND_FILE $PYTHON_COMMAND_FILE_PARAMS > /dev/null 2>&1 & echo $! > $PYTHON_COMMAND_PID_FOLDER/$PYTHON_COMMAND_PID_FILENAME