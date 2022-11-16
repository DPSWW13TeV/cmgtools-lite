import os

idir="jobs_TTmore"
missingChunks=[]

for i in os.listdir(idir):
    found=False
    if os.path.isfile(os.path.join(idir,i)) : continue
    for j in os.listdir(os.path.join(idir,i)):
        if 'url' in j:
            found=True
            break
    if  not found:
        missingChunks.append(i)
        
print missingChunks
