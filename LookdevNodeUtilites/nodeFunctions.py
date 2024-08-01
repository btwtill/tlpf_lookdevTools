import maya.cmds
#function to create a color constant and connect it to any aiSurface shader in a selection

def colorConstantToSelectionSurfaceShader(selectionList, name = "CombinedColorConstant"):
    #create new color constant
    newColorConstantNode = cmds.createNode("colorConstant", name = name)
    
    #filter selection list to only aiStandard Surface shaders
    filteredList = []
    for sel in selectionList:
        if cmds.nodeType(sel) == "aiStandardSurface":
            filteredList.append(sel)
   
    print(filteredList)
    
    #connect color constant to all the surface shaders
    for shader in filteredList:
        for channel in "RGB":
            cmds.connectAttr(f"{newColorConstantNode}.outColor{channel}", f"{shader}.baseColor{channel}")
        

selection = cmds.ls(sl=True)

colorConstantToSelectionSurfaceShader(selection)