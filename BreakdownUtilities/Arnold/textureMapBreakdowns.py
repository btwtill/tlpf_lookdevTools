import maya.cmds as cmds
import mtoa.aovs as aovs


#select what aov you want to create
def textureBreakdownAovsUI():
    aovList = {
        "diffuse" : [".baseColor", "1"],
        "roughness" : [".specularRoughness", "2"],
        "normal" : [".normalCamera", "3"],
        "metal" : [".metalness", "4"],
        "subsurfaceColor" : [".subsurfaceColor", "5"],
        "subsufaceRadius" : [".subsurfaceRadius", "6"],
        "coatMap": [".coat", "7"]
    }
    return aovList

#select the shader you want to connect to the different aovs

def createCustomAovs(aovList):
    for aov, values in aovList.items():
        aovs.AOVInterface().addAOV(aov, aovType='rgba')
    
    #create displacement aov
    aovs.AOVInterface().addAOV("displacement", aovType='rgba')

def connectTexturesToAovs(aovList, materialSelection):
    for material in materialSelection:
        for aov, values in aovList.items():
            
            #look if the aovs have been connected already
            aovInputConnection = cmds.listConnections(f"{material}.aovId{values[1]}")
            
            if aovInputConnection == None:
                #connect aov name to material aovs
                cmds.connectAttr(f"aiAOV_{aov}.name", f"{material}.aovId{values[1]}")
            else:
                print(f"{material} aov Input {values[1]} already Connected")

            #look for the texture connected to the material ports
            inputConnection = cmds.listConnections(f"{material}{values[0]}", plugs=True)
            


            #logic to handle if there is no input connection
            if inputConnection == None:
                print(f"Material: {material}, Attribute: {values[0]} No Input Connection.")
            else:
                inputConnectionNodeStringList = inputConnection[0].split(".")
                inputConnectionNode = cmds.nodeType(inputConnectionNodeStringList[0])
                print(f"Material Channel Input Node type: {inputConnectionNode}")
                
                #check for Normal Map Node
                if inputConnectionNode == "aiNormalMap":
                    inputConnection = [f"{inputConnectionNodeStringList[0]}.input"]
                
                #get connections type
                connectionTpye = cmds.getAttr(inputConnection[0], type = True)
                print(f"attribute:{inputConnection[0]}, type: {connectionTpye}")

                #separete connections based on type
                if connectionTpye == "float":

                    #connect single float input to all RBG channels of the aov
                    for channel in "RGB":
                        cmds.connectAttr(inputConnection[0], f"{material}.id{values[1]}{channel}", force = True)
                else:

                    #connect multy channel input texture to aov 
                    cmds.connectAttr(inputConnection[0], f"{material}.id{values[1]}", force = True)
        
        #look if the displacement aov is already connected
        displacementAovInputConnection = cmds.listConnections(f"{material}.aovId8")

        if displacementAovInputConnection == None:
            #connect displacement aov to material
            cmds.connectAttr(f"aiAOV_displacement.name", f"{material}.aovId8")
        else:
            print(f"{material} diplacement aov already Connected!")

        #get displacement shader output node
        shaderNodeConnections = cmds.listConnections(f"{material}.outColor", plugs = True)
        print(shaderNodeConnections)

        #look for the string with .surfaceShader
        surfaceShaderAttribute = []
        for connection in shaderNodeConnections:
            if connection.endswith(".surfaceShader"):
                surfaceShaderAttribute.append(connection)

        #Filter out the strin part that indicates the shader Node
        print(f"Connected Surface Shader Attribute: {surfaceShaderAttribute}")
        surfaceShaderAttributeStringList = surfaceShaderAttribute[0].split(".")
        print(f"Material Shader Node: {surfaceShaderAttributeStringList[0]}")

        #get displacement input connection Attributes
        displacementInput = cmds.listConnections(f"{surfaceShaderAttributeStringList[0]}.displacementShader", plugs = True)
        print(f"Displacement Shader: {displacementInput}")

        #catch if there is no displacement attached to the Material
        if displacementInput == None:
            print(f"Material: {material} has no displacement Input!")
        else:
            for channel in "RGB":
                cmds.connectAttr(displacementInput[0], f"{material}.id8{channel}", force = True)


allCurrentAovs = aovs.AOVInterface().getAOVNodes(names=True)
alreadyExistent = False

for aovTuple in allCurrentAovs:
    if "displacement" in aovTuple:
        alreadyExistent = True
        break

if alreadyExistent:
    print("Aovs Already Created")
else:
    print(alreadyExistent)
    createCustomAovs(textureBreakdownAovsUI())

connectTexturesToAovs(textureBreakdownAovsUI(), cmds.ls(sl=True))