import re, os


jobid="9807000"


def eventid(inFile):
    file1 = open(inFile, 'r')
    Lines = file1.readlines()    
    #event_id={'WJets0':[[],[]],'STop':[[],[]],'data':[[],[]],'TTbar':[[],[]],'WW':[[],[]],'WZ':[[],[]],'WJets1':[[],[]]}
    event_id={'WJets0':[],'STop':[],'data':[0],'TTbar':[]}#,'WW':[],'WZ':[],'WJets1':[]}
    #nums=[line.split('selection')[-1] for line in Lines if 'selection' in line]
    for line in Lines:
        if 'selection' in line:
            info_str=re.search('for(.*)selection(.*)[?0-9]', line).group(0).split()
            #['for', '_WJets0', 'passing', 'the', 'selection', '310258914', 'eventweight', '0.415399909873']
            if info_str[1].split('_')[-1] in event_id.keys():
                event_id[info_str[1].split('_')[-1]].append((info_str[5],info_str[7]))
        else: continue
    return event_id



outFile=open("out_skim.txt", 'w')

for lep in ("mu,el").split(','):
    outFile.write('##----------------------------------%s--------------------\n'%lep)
    nums_skim=[];nums_frnd=[];
    skimFile= "jobs/Nbkg_"+jobid+"_"+lep+"_skim.out"
    frndsFile="jobs/Nbkg_"+jobid+"_"+lep+"_frnd.out"
    #    print skimFile,frndsFile
    nums_skim=eventid(skimFile)
    nums_frnd=eventid(frndsFile)
    frmt_str = "%6s %40s \n"  
    
    #print type(nums_skim),type(nums_frnd),nums_frnd.keys(),nums_skim.keys(),len(nums_skim['WJets0'])
    missing_eId={'WJets0':[],'STop':[],'data':[],'TTbar':[]}#,'WW':[],'WZ':[],'WJets1':[]}
    for pId in missing_eId.keys():
        print pId
        if len(nums_skim[pId]) !=  len(nums_frnd[pId]): 
            print 'mismathc for', pId
            larger=nums_skim if len(nums_skim[pId]) > len(nums_frnd[pId]) else nums_frnd
            shorter=nums_skim if len(nums_skim[pId]) < len(nums_frnd[pId]) else nums_frnd
            print lep,"\t",pId,"\t nums_skim has more events " if larger == nums_skim else "nums_frnd has more events"
            addstr=" missing from %s" %("skim" if len(nums_skim[pId]) < len(nums_frnd[pId]) else "frnd" )
            missing_eId[pId] = [value[0]+"\t"+value[1]+"\t"+ addstr for value in larger[pId] if value not in shorter[pId]]
 #           print [value for value in larger[pId] if value not in shorter[pId]]
#    print missing_eId

    for iK,iV in missing_eId.iteritems():
        #print iK,iV
        #outFile.write(frmt_str%(iK+"_"+str(len(iV)),iV))
        outFile.write(iK +" : mismatched entries "+str(len(iV)) +"\n")
        for ivalue in iV:
            outFile.write(ivalue+"\n")
        outFile.write("\n")

outFile.close()

#            print "missing event ids",pId,len(missing_eId)

#   for i in missing_eId

#    numbers_skim[
#lst3 = [value for value in numbers if value not in numbers_skim]






###line="IMPCHK event number for         _WJets0         passing the selection   1495836"
#            nums=line.split('selection')[-1] 
#            label=re.search('_(.*)passing', line).group(1).split()[0]    
