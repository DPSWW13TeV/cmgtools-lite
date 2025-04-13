import os 
#nfiles=[f for f in os.listdir(os.getcwd()) if f.endswith('.txt')]
for i in range(103):
    fin = open("dummy.txt","r")
    fout=open("fr-pdf_{}.txt".format(i),"w")
    for line in fin.readlines():
        line=line.replace('NUM',str(i));
        fout.write(line)
    fout.close()
    
