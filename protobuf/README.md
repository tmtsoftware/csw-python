This directory stores protobuf filesused by CSW.  To construct the files here, use:

``
protoc --python_out=.. csw_protobuf/*.proto 
protoc --python_out=.. scalapb/*.proto 
``

from the this directory.

These files are copied from CSW Event Service 
(https://github.com/tmtsoftware/csw/tree/master/csw-event-client/src/main/protobuf/csw_protobuf).
Perhaps at some point the files can be pulled directly from that project, or, in the future,
some other shared repository, but for now, they are copied and must be synchronized manually.

