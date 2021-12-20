#############################################################################################
# Python Script to automate generation of xmls for Mitsuba renderer
#
# This script allows to change material parameters such as refractive index, alpha, albedo, sigmaT
# as well as the image size and samples per pixel.
#
# The generated batch file can be used to automate the rendering of the generated .xml files.
#
# David Norman Diaz Estrada
# davidnd@stud.ntnu.no
#############################################################################################

import sys, os

##########################################
# Set paths and folder names:
##########################################
exmfile= "renderingTemplateG5_3.xml" # Set the path to .xml rendering template
myOutputFolder="G5_4096_sampl_512x512"   # Give a name to the output folder that will contain all the generated xmls

workingPath=os.path.dirname(os.path.realpath(__file__))# Get path of this python script
OutputPath=workingPath+'\\'+myOutputFolder+'\\'
print("Output Folder: " + myOutputFolder)
print("Output Path: " + OutputPath)


##########################################
# Set general Rendering configurations:
##########################################
RenderWindows=True #set to true to generate batch file for rendering in Windows
RenderUbuntu=False #set to true to generate bash file for rendering in Ubuntu

mySamples = 4096              # declare number of samples for the integer
myWidth = 512                # width of image to render
myHeight = 512				 # height of image to render

#############################################
# Set the rendering parameters to be changed:
#############################################

#Declare list of parameters to be written in each rendering configuration:

Params_IOR = [1.10,1.33,1.50,2.00,2.41]
Params_alpha = [0.01,0.10,0.50]
Params_albedo = [0.1,0.5,0.8]
Params_sigmaT = [0,1,5]


#Variables to set initial value of each parameter in template:
prenameSigT    = '<spectrum name="sigmaT" value="/> <!--VARY SigmaT______________________________________________________________________________-->'
prenameAlbedo  = '<spectrum name="albedo" value="/> <!--VARY Albedo______________________________________________________________________________-->'
prenameIOR     = '<float name="intIOR" value="/><!-- VARY internal IOR________________________________________________________________________-->'
prenameAlpha   = '<float name="alpha" value="/> <!-- VARY roughness alpha________________________________________________________________________-->'
prenameSamples = '<integer name="sampleCount" value="/><!-- VARY Samples________________________________________________________________________-->'
prenameWidth   = '<integer name="width" value="/><!-- VARY Image width________________________________________________________________________-->'
prenameHeight  = '<integer name="height" value="/><!-- VARY Image height________________________________________________________________________-->'


#Variables to track the last change (value) in each rendering parameter:
lastnameSigT    = prenameSigT
lastnameAlbedo  = prenameAlbedo
lastnameIOR     = prenameIOR
lastnameAlpha   = prenameAlpha
lastnameSamples = prenameSamples
lastnameWidth   = prenameWidth
lastnameHeight  = prenameHeight



# CHANGE SAMPLES:
s = open(exmfile).read()
stringSamples = '<integer name="sampleCount" value="'+str(mySamples)+'"/><!-- VARY Samples________________________________________________________________________-->'
s = s.replace(lastnameSamples, stringSamples)
lastnameSamples = stringSamples
f = open(exmfile, 'w')
f.write(s)
f.close()

# CHANGE IMAGE WIDTH
s = open(exmfile).read()
stringWidth = '<integer name="width" value="'+str(myWidth)+'"/><!-- VARY Image width________________________________________________________________________-->'
s = s.replace(lastnameWidth, stringWidth)
lastnameWidth = stringWidth
f = open(exmfile, 'w')
f.write(s)
f.close()

# CHANGE IMAGE HEIGHT
s = open(exmfile).read()
stringHeight= '<integer name="height" value="'+str(myHeight)+'"/><!-- VARY Image height________________________________________________________________________-->'
s = s.replace(lastnameHeight, stringHeight)
lastnameHeight = stringHeight
f = open(exmfile, 'w')
f.write(s)
f.close()


# Create an xml file For each rendering configuration by replacing the values in template:

for current_alpha in Params_alpha:
	for current_albedo in Params_albedo:
		for current_sigmaT in Params_sigmaT:
			for current_IOR in Params_IOR:
				# CHANGE ALPHA:
				s = open(exmfile).read() #open and read rendering template
				stringAlpha = '<float name="alpha" value="'+ str(current_alpha) +'"/> <!-- VARY roughness alpha________________________________________________________________________-->'
				s = s.replace(lastnameAlpha, stringAlpha) #access to xml and replace last rendering config with current config
				lastnameAlpha = stringAlpha #update last rendering config for this parameter
				f = open(exmfile, 'w') #open rendering template in write mode,and save it as f
				f.write(s) #write changes and save it in f
				f.close() #close f (edited .xml)

				# CHANGE SIGMA T:
				s = open(exmfile).read()
				stringSigT = '<spectrum name="sigmaT" value="'+ str(current_sigmaT) +'"/> <!--VARY SigmaT______________________________________________________________________________-->'
				s = s.replace(lastnameSigT, stringSigT)
				lastnameSigT = stringSigT
				f = open(exmfile, 'w')
				f.write(s)
				f.close()

				#CHANGE ALBEDO:
				s = open(exmfile).read()
				stringAlbedo = '<spectrum name="albedo" value="'+ str(current_albedo) +'"/> <!--VARY Albedo______________________________________________________________________________-->'
				s = s.replace(lastnameAlbedo, stringAlbedo)
				lastnameAlbedo = stringAlbedo
				f = open(exmfile, 'w')
				f.write(s)
				f.close()

				#CHANGE IOR (index of refraction):
				s = open(exmfile).read()
				stringIOR = '<float name="intIOR" value="'+str(current_IOR)+'"/><!-- VARY internal IOR________________________________________________________________________-->'
				s = s.replace(lastnameIOR, stringIOR)
				lastnameIOR = stringIOR
				f = open(exmfile, 'w')
				f.write(s)
				f.close()



				#####################################################
				#Create a new .xml file with current rendering configuration:
				#####################################################
				filename = 'ior_'+str(current_IOR)+'_alpha_'+str(current_alpha) + '_albedo_'+str(current_albedo)+ '_sigT_'+str(current_sigmaT) +'_sampl_'+str(mySamples)
				print (filename)
				new_xml=open(OutputPath+filename+'.xml', 'w')
				new_xml.write(s)

				if RenderWindows:
					#####################################################
					# Create batch file for rendering (WINDOWS):
					#####################################################
					line='mitsuba -o '+ myOutputFolder+'/' + str(filename)+('.png ')+ myOutputFolder+'/' +str(filename)+('.xml')
					with open(OutputPath+'renderBatchFile.txt', 'a') as f1:
						f1.write(line + os.linesep)

				if RenderUbuntu:
					#####################################################
					# Create bash file for rendering (Ubuntu):
					#####################################################
					line = 'mitsuba '+ myOutputFolder+'/' +str(filename)+('.xml')+' && '+ 'mtsutil tonemap '+ myOutputFolder+'/'+str(filename)+('.exr')+ ' && '
					with open(OutputPath+'renderBashFile.txt', 'a') as f2:
						#f2.write(line + os.linesep)
						f2.write(line)

#####################################################
# Restore the .xml original template values:
#####################################################
s = open(exmfile).read()


s = s.replace(lastnameSigT, prenameSigT)
s = s.replace(lastnameAlbedo, prenameAlbedo)
s = s.replace(lastnameAlpha, prenameAlpha)
s = s.replace(lastnameSamples, prenameSamples)
s = s.replace(lastnameWidth, prenameWidth)
s = s.replace(lastnameHeight, prenameHeight)
s = s.replace(lastnameIOR,prenameIOR)

f = open(exmfile, 'w')
f.write(s)
f.close()


