#!/bin/bash

INPUTDATADIR=/home/fubao/workDir/CiscoWish/data/service_request_staging_DB
RANGEDIFFTHRESHOLD=1.2
BUCKETSIZENUM=2000000
OUTPUTNUMERICALRES=/home/fubao/workDir/CiscoWish/CreateGraph/GraphMatching/SpydeWks/Codes/output/numericalOutput

NONNUMPREFIXLENGTH=2
NONSAMPLERECORDNUM=4000
RECORDPAIRSIMITHRESHOLD=0.5
OUTPUTNONNUMDIR=/home/fubao/workDir/CiscoWish/CreateGraph/GraphMatching/SpydeWks/Codes/output/nonNumericalOutput

INTERMEDIATEOUTFLAG=False
MACHINNO=0
MACHINENUM=4

echo "Start Database Matching..."
#python3 -m cProfile -o myscript.cprof manuallyDistributedmainEntry.py -i $INPUTDATADIR -rdt $RANGEDIFFTHRESHOLD -bs $BUCKETSIZENUM -oNum $OUTPUTNUMERICALRES  -pl $NONNUMPREFIXLENGTH -spNum $NONSAMPLERECORDNUM -recsimt $RECORDPAIRSIMITHRESHOLD -oNonDir $OUTPUTNONNUMDIR -interOFlg $INTERMEDIATEOUTFLAG -macNo $MACHINNO -macNums $MACHINENUM 

#python3 -m cProfile -o output.pstats manuallyDistributedmainEntry.py -i $INPUTDATADIR -rdt $RANGEDIFFTHRESHOLD -bs $BUCKETSIZENUM -oNum $OUTPUTNUMERICALRES  -pl $NONNUMPREFIXLENGTH -spNum $NONSAMPLERECORDNUM -recsimt $RECORDPAIRSIMITHRESHOLD -oNonDir $OUTPUTNONNUMDIR -interOFlg $INTERMEDIATEOUTFLAG -macNo $MACHINNO -macNums $MACHINENUM 
#python3 manuallyDistributedmainEntry.py -i $INPUTDATADIR -rdt $RANGEDIFFTHRESHOLD -bs $BUCKETSIZENUM -oNum $OUTPUTNUMERICALRES  -pl $NONNUMPREFIXLENGTH -spNum $NONSAMPLERECORDNUM -recsimt $RECORDPAIRSIMITHRESHOLD -oNonDir $OUTPUTNONNUMDIR -interOFlg $INTERMEDIATEOUTFLAG -macNo $MACHINNO -macNums $MACHINENUM 
python3 mainEntry.py -i $INPUTDATADIR -rdt $RANGEDIFFTHRESHOLD -bs $BUCKETSIZENUM -oNum $OUTPUTNUMERICALRES  -pl $NONNUMPREFIXLENGTH -spNum $NONSAMPLERECORDNUM -recsimt $RECORDPAIRSIMITHRESHOLD -oNonDir $OUTPUTNONNUMDIR -interOFlg $INTERMEDIATEOUTFLAG

.py



echo "End"

