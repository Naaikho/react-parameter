import sys, os
import time
import platform
from typing import Union

PAUSE = "pause" if platform.system() == "Windows" else "read var"
CLEAR = "cls" if platform.system() == "Windows" else "clear"

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
    os.system(CLEAR)
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
    appIndex = 0
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

    # found end of consr app = {...} in file (if the const is not on one line)
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

    # found all parameters in const app = {...} in file and put them in params list
    params = []
    for l in iFile:
      l = "".join(l.split(" ")).strip()
      types = "any"
      if(("const[" in l or "const [" in l) and not l.strip().startswith("//")):
        if file.endswith(("tsx", "ts")) and "<" in l and ">" in l:
          # split and keep the types between firsts "<" and ">" (to catch Component<Array<Type>>() for example)
          types: str = ">".join("<".join(l.split("<")[1:]).split(">")[:-1])
        l = l.split("=")[0].strip()
        l = l.split("[")[1].split("]")[0].strip().split(",")
        l = [x.strip() for x in l]
        if l[0] != "":
          params.append({
            "var": l[0],
            "type": types
          })
        if l[1] != "":
          params.append({
            "var": l[1],
            "type": f"React.Dispatch<React.SetStateAction<{types}>>"
          })

    # format params list to make new interface with all parameters and types
    interfaceContent = None
    if(params and file.endswith(("tsx", "ts"))):
      interfaceContent = ["{}: {}".format(x["var"], x["type"] if x["type"] else "any") for x in params]
      interfaceContent.append("[key: string]: any;")
      interfaceContent = "export interface NkContext {\n  " + ";\n  ".join(interfaceContent) + "\n}\n"

    # format params list to become new const app = {...} in file
    app = (" " * spaceNb) + "const app{}".format((": NkContext" if file.endswith(("tsx", "ts")) else "")) + " = {" + ",".join([x["var"] for x in params]) + "};"

    # include new const app = {...} in file
    nFile = "\n".join(sep[0] + [app] + sep[1])

    # write file
    open(pFile, "w").write(nFile)
    if(interfaceContent):
      imports = ""
      contextTypepath = os.path.join(iPath, "types", "nkContext.types.ts")
      if not os.path.exists(os.path.join(iPath, "types")):
        os.mkdir(os.path.join(iPath, "types"))
      if os.path.exists(contextTypepath):
        imports = open(contextTypepath, "r").read().split("\n")
        imports = [x for x in imports if x.startswith("import")]
        imports = "\n".join(imports) + "\n\n"
      open(os.path.join(iPath, "types", "nkContext.types.ts"), "w").write(imports + interfaceContent)

    # update last update time
    lu = os.path.getmtime(pFile)

  time.sleep(0.5)