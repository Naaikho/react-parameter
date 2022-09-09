import sys, os
import time
import platform

PAUSE = "pause" if platform.system() == "Windows" else "read var"

path = sys.argv[1]

try:
    file = sys.argv[2]
except IndexError:
    file = "index.js"

iPath = os.path.join(path, "src")

if not os.path.exists(iPath):
    print("Error: Could not find './src/'")
    os.system(PAUSE)
    exit()

pFile = os.path.join(iPath, file)

if not os.path.exists(pFile):
    print("Error: Could not find './src/index.js'")
    os.system(PAUSE)
    exit()

lu = 0

while 1:
    # if file is edited, enter in condition
    if os.path.getmtime(pFile) > lu:
        os.system("cls")
        print("React Parameters initialized")
        print("")
        print("Last update: " + time.strftime("%H:%M:%S"))

        if os.path.exists(pFile):
            iFile = open(pFile, "r").read()
        else:
            print("Error: Could not find './src/index.js'")
            os.system(PAUSE)
            continue

        iFile = iFile.split("\n")

        app = []

        # found const app = {...} in file
        appIndex = -1
        spaceNb = 0
        for i in range(len(iFile)):
            if("const app" in iFile[i]):
                appIndex = i
                spaceNb = iFile[i].index("const")
                break

        if not appIndex:
            print("Error: Could not find the 'app' object in './src/index.js'")
            os.system(PAUSE)
            continue

        sep = []
        closeIndex = -1
        if not "}" in iFile[appIndex]:
            for i in range(appIndex, len(iFile)):
                if("}" in iFile[i]):
                    closeIndex = i
                    break
            sep.append(iFile[0:appIndex])
            sep.append(iFile[closeIndex+1:])
        else:
            sep.append(iFile[0:appIndex])
            sep.append(iFile[appIndex+1:])

        # print(sep)

        params = []

        for l in iFile:
            l = l.strip()
            if(("const[" in l or "const [" in l) and not l.startswith("//")):
                l = " ".join(l.split("=")[0].split(" ")[1:]).strip()
                l = l.split("[")[1].split("]")[0].strip().split(",")
                l = [x.strip() for x in l]
                params.append(l[0])
                params.append(l[1])

        app = (" " * spaceNb) + "const app = {" + ",".join(params) + "};"

        nFile = "\n".join(sep[0] + [app] + sep[1])

        # print(nFile)

        open(pFile, "w").write(nFile)

        lu = os.path.getmtime(pFile)

    time.sleep(0.5)