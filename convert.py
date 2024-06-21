#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Code Vein Mod Converter Tool 1.0 by drchannn
#
##############################################

import sys
import os
import shutil
import subprocess
import traceback

from datetime import datetime


APP_PATH=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])))
TMP_PATH=APP_PATH+"\\tmp"

#INI OPTIONS
CHECK_REQUISITES=1
AUTO_SET_PROFILE=0
PAUSE_STEP=0
PAUSE_FINISH=1
PAK_COMPRESS=0
PROFILE=""

#PROFILES
GAMETAG=""
GAMEPATH=""

############################
def __l(mensaje, noprint=0):
	salida = '>> %s | [%s] '  % (datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), mensaje)
	if (noprint==0): print (salida)
	else: return salida

def __exit(mensaje):
	__l(mensaje)
	input("\n                          Press a key to continue . . .")
	sys.exit()

def __load_ini():
	__l("LOADING OPTIONS")
	global CHECK_REQUISITES,AUTO_SET_PROFILE,PAUSE_STEP,PAUSE_FINISH,PAK_COMPRESS,PROFILE

	if (os.path.isfile(APP_PATH+"\\"+"convert.ini")==False):
			with open(APP_PATH+"\\"+"convert.ini", "w") as ini_file:
				ini_file.write("CHECK_REQUISITES="+str(CHECK_REQUISITES)+"\n")
				ini_file.write("AUTO_SET_PROFILE="+str(AUTO_SET_PROFILE)+"\n")
				ini_file.write("PAUSE_STEP="+str(PAUSE_STEP)+"\n")
				ini_file.write("PAUSE_FINISH="+str(PAUSE_FINISH)+"\n")
				ini_file.write("PAK_COMPRESS="+str(PAK_COMPRESS)+"\n")
	else:
		with open(APP_PATH+"\\"+"convert.ini", "r") as ini_file:
			lineas=ini_file.read()
			for linea in (lineas.split("\n")):
				if (linea[:len("CHECK_REQUISITES=")]=="CHECK_REQUISITES="): CHECK_REQUISITES=int(linea[len("CHECK_REQUISITES="):])
				if (linea[:len("AUTO_SET_PROFILE=")]=="AUTO_SET_PROFILE="): AUTO_SET_PROFILE=int(linea[len("AUTO_SET_PROFILE="):])
				if (linea[:len("PAUSE_STEP=")]=="PAUSE_STEP="): PAUSE_STEP=int(linea[len("PAUSE_STEP="):])
				if (linea[:len("PAUSE_FINISH=")]=="PAUSE_FINISH="): PAUSE_FINISH=int(linea[len("PAUSE_FINISH="):])
				if (linea[:len("PAK_COMPRESS=")]=="PAK_COMPRESS="): PAK_COMPRESS=int(linea[len("PAK_COMPRESS="):])
				if (linea[:len("PROFILE=")]=="PROFILE="): PROFILE=linea[len("PROFILE="):]

def __select_profile():	
	global GAMETAG,GAMEPATH,PROFILE
	
	if(PROFILE==""):
		__l("SET PROFILE TO USE")
		print ("")
		profiles=[]
		spaces="                         "
		with os.scandir(APP_PATH+"\\tools\\profiles") as ficheros:
			for fichero in ficheros: profiles.append(fichero.name)
		
		for i, k in enumerate(profiles):
			print (spaces+"["+str(i)+"] "+k)
		print ("")
		index_profile=input(spaces+"Select profile that u need use: ")

		try:		
			PROFILE=profiles[int(index_profile)]
		except:
			__exit("ERROR: UNKNOW PROFILE")
	
	with open(APP_PATH+"\\tools\\profiles\\"+PROFILE, "r") as ini_file:
		lineas=ini_file.read().split("\n")
		GAMETAG=lineas[0]
		GAMEPATH=lineas[1]
	__l("PROFILE SET TO "+PROFILE)

def __save_default_profile(clear=0):
	#__l("SAVE DEFAULT PROFILE")
	with open(APP_PATH+"\\"+"convert.ini", "w") as ini_file:
		ini_file.write("CHECK_REQUISITES="+str(CHECK_REQUISITES)+"\n")
		ini_file.write("AUTO_SET_PROFILE="+str(AUTO_SET_PROFILE)+"\n")
		ini_file.write("PAUSE_STEP="+str(PAUSE_STEP)+"\n")
		ini_file.write("PAUSE_FINISH="+str(PAUSE_FINISH)+"\n")
		ini_file.write("PAK_COMPRESS="+str(PAK_COMPRESS)+"\n")
		if (clear==0): ini_file.write("PROFILE="+str(PROFILE)+"\n")
	
def __get_ps4_pak_filename(pak_file):
	pc_pak=pak_file
	if(pc_pak.find(":")==-1): pc_pak=APP_PATH+"\\"+pc_pak
	if (pc_pak[-6:-4].lower()=="_p"): ps4_pak=pc_pak[:-6]+"-ps4_0_p.pak"
	else: ps4_pak=pc_pak[:-4]+"-ps4_0_p.pak"
	return ps4_pak

def __check_requisites():
	__l("CHECKING REQUISITES")

	if (os.path.isfile(APP_PATH+"\\tools\\unrealpak\\UnrealPak.exe")==False):
		__exit("ERROR MISSING UNREALPAK")

	if (os.path.isfile(APP_PATH+"\\tools\\umodel\\umodel.exe")==False) or \
	(os.path.isfile(APP_PATH+"\\tools\\umodel\\umodel_64.exe")==False) or \
	(os.path.isfile(APP_PATH+"\\tools\\umodel\\SDL2.dll")==False) or \
	(os.path.isfile(APP_PATH+"\\tools\\umodel\\SDL2_64.dll")==False):
		__exit("ERROR MISSING UMODEL")

	if (os.path.isfile(APP_PATH+"\\tools\\orbis-image2gnf\\orbis-image2gnf.exe")==False) or \
	(os.path.isfile(APP_PATH+"\\tools\\orbis-image2gnf\\libSceTextureTool.dll")==False) or \
	(os.path.isfile(APP_PATH+"\\tools\\orbis-image2gnf\\libSceGpuAddress.dll")==False) or \
	(os.path.isfile(APP_PATH+"\\tools\\orbis-image2gnf\\libSceGnm.dll")==False):
		__exit("ERROR MISSING ORBIS-IMAGE2GNF")
############################



############################
def cleaning_paths():
	__l("CLEANING TMP PATH")
	if (os.path.isdir(APP_PATH+"\\tmp")==True): shutil.rmtree(APP_PATH+"\\tmp")


def extract_content_pak(pak_file):
	__l("EXTRACTING FILES FROM PAK")
	os.makedirs(APP_PATH+"\\tmp", exist_ok=True)
	os.makedirs(APP_PATH+"\\tmp\\pak", exist_ok=True)

	pak_filename = pak_file.split("\\")[-1]
	shutil.copy(pak_file, TMP_PATH+"\\pak\\"+pak_filename)

	umodel_exe = "%s\\tools\\umodel\\umodel.exe" % (APP_PATH)
	umodel_extract_cmd=[umodel_exe,"-game="+GAMETAG,"-path="+TMP_PATH+"\\pak","-save","*"]
	sp = subprocess.run(umodel_extract_cmd, capture_output=True, text=True, cwd=TMP_PATH+"\\pak")
	if (os.path.isdir(TMP_PATH+"\\pak\\UmodelSaved")==False): 
		__save_default_profile(1)
		__exit("ERROR: ON SAVE FILES FROM PAK")
	shutil.copytree(TMP_PATH+"\\pak\\UmodelSaved", TMP_PATH+"\\ps4", dirs_exist_ok=True)
	shutil.copytree(TMP_PATH+"\\pak\\UmodelSaved", TMP_PATH+"\\pc", dirs_exist_ok=True)
	shutil.rmtree(TMP_PATH+"\\pak\\UmodelSaved")

	umodel_export_cmd=[umodel_exe,"-game="+GAMETAG,"-path="+TMP_PATH+"\\pak","-notgacomp","-export","*"]
	sp = subprocess.run(umodel_export_cmd, capture_output=True, text=True, cwd=TMP_PATH+"\\pak")
	if (os.path.isdir(TMP_PATH+"\\pak\\UmodelExport")==False):
		__save_default_profile(1)
		__exit("ERROR: ON EXPORT TGA FROM PAK")
	umodel_export_cmd=[umodel_exe,"-game="+GAMETAG,"-path="+TMP_PATH+"\\pak","-dds","-export","*"]
	sp = subprocess.run(umodel_export_cmd, capture_output=True, text=True, cwd=TMP_PATH+"\\pak")
	if (os.path.isdir(TMP_PATH+"\\pak\\UmodelExport")==False): 
		__save_default_profile(1)
		__exit("ERROR: ON EXPORT DDS FROM PAK")
	shutil.copytree(TMP_PATH+"\\pak\\UmodelExport", TMP_PATH+"\\pc", dirs_exist_ok=True)
	shutil.rmtree(TMP_PATH+"\\pak")


def get_files_to_process():
	__l("GETTING FILES TO PROCESS")
	aux_listado=[]
	for directorio_actual, subdirectorios, archivos in os.walk(TMP_PATH+"\\pc"):
		for k in archivos:
			if(k[-4:]==".tga"):
				pc_path = directorio_actual
				ps4_path = directorio_actual[:len(TMP_PATH)]+"\\ps4"+directorio_actual[len(TMP_PATH)+3:]
				fichero_sin_ext=(("%s\\%s" % (directorio_actual, k))[:-4])[len(directorio_actual)+1:]

				aux_obj={}
				aux_obj["fichero"]=fichero_sin_ext
				aux_obj["path_pc"]=pc_path
				aux_obj["path_ps4"]=ps4_path
				aux_obj["tga"]=0
				aux_obj["dds"]=0
				aux_obj["uasset"]=0
				aux_obj["uexp"]=0
				aux_obj["ubulk"]=0

				if (os.path.isfile(pc_path+"\\"+fichero_sin_ext+".tga")):
					aux_obj["tga"]=1
				if (os.path.isfile(pc_path+"\\"+fichero_sin_ext+".dds")):
					aux_obj["dds"]=1
				if (os.path.isfile(pc_path+"\\"+fichero_sin_ext+".uasset")):
					aux_obj["uasset"]=1
				if (os.path.isfile(pc_path+"\\"+fichero_sin_ext+".uexp")):
					aux_obj["uexp"]=1
				if (os.path.isfile(pc_path+"\\"+fichero_sin_ext+".ubulk")):
					aux_obj["ubulk"]=1

				aux_listado.append(aux_obj)
	return aux_listado


#Esta funcion necesitaria una mejor opcion para determinar la posicion del formato
#en vez de buscar PF_ [50 46 5F]
def get_info_uexp(fichero):
	offset_header=-1
	with open(fichero, "rb") as ff:
		contenido_binario = ff.read()
		for offset, byte in enumerate(contenido_binario):
			if (hex(contenido_binario[offset])=="0x50"):
				if (hex(contenido_binario[offset+1])=="0x46" and hex(contenido_binario[offset+2])=="0x5f"):
					offset_header = offset
					
					
				'''	
					if (hex(contenido_binario[offset+3])=="0x44" and hex(contenido_binario[offset+4])=="0x58" and hex(contenido_binario[offset+5])=="0x54"):
						formato_dds = chr(contenido_binario[offset+3])+chr(contenido_binario[offset+4])+chr(contenido_binario[offset+5])+chr(contenido_binario[offset+6])
						formato_dds = formato_dds.upper()
						print (formato_dds)
						size_header = offset+3+len(formato_dds)+33
						offset_header = offset
						checked=1
						break
					elif (hex(contenido_binario[offset+3])=="0x42" and hex(contenido_binario[offset+4])=="0x43"):
						formato_dds = chr(contenido_binario[offset+3])+chr(contenido_binario[offset+4])+chr(contenido_binario[offset+5])
						formato_dds = formato_dds.upper()
						size_header = offset+3+len(formato_dds)+33
						offset_header = offset
						checked=1
						break
				'''	
	
	
	if(offset_header>-1):
		long_dds_formato=0
		formato_dds=""
		with open(fichero, "rb") as ff:
			ff.seek(offset_header)
			contenido_binario = ff.read(1)
			while contenido_binario != b'\x00':
				formato_dds=formato_dds+chr(contenido_binario[0])
				contenido_binario = ff.read(1)
		formato_dds = formato_dds.upper()	
		size_header = offset+len(formato_dds)+33
	
	with open(fichero, "rb") as ff:
		ff.seek(offset_header+len(formato_dds)+5) #using pf_ or bc_
		contenido_binario = ff.read(4)
		num_mipmaps = int.from_bytes(contenido_binario, byteorder='little')
	
	return size_header,formato_dds,num_mipmaps,offset_header


def convert_dds():
	__l("CONVERTING DDS FILES")
	orbisimage_exe = "%s\\tools\\orbis-image2gnf\\orbis-image2gnf.exe" % (APP_PATH)

	for i, k in enumerate(listado_ficheros):
		print (f"\t\t\t  {i+1} - {len(listado_ficheros)}", end="\r")

		if (listado_ficheros[i]['tga']==1):
			
			fichero_actual=listado_ficheros[i]['path_pc']+"\\"+listado_ficheros[i]['fichero']

			# alguna vez los ficheros de imagen van en subcarpetas 
			# cuando esto pasa esos ficheros no se procesan
			if (os.path.isfile(fichero_actual+".uexp")==False): 
				input(__l("WARNING: MISSING UEXP FILE ["+listado_ficheros[i]['fichero']+"] - THIS FILE CAN BE CONVERTED - Press a key to continue . . .",1))
			else:
				size_header,formato_dds,num_mipmaps,offset_header=get_info_uexp(fichero_actual+".uexp")
				if (formato_dds=="PF_DXT1"):
					formato_ps4 = "Bc1UNormSrgb"
				elif (formato_dds=="PF_DXT5"):
					formato_ps4 = "Bc3UNormSrgb"
				elif (formato_dds=="PF_BC5"):
					formato_ps4 = "Bc5UNorm"
				elif (formato_dds=="PF_BC7"):
					formato_ps4 = "Bc7UNorm"
				elif (formato_dds=="PF_B8G8R8A8"):
					formato_ps4 = "B8G8R8X8UNormSrgb"
					input(__l("WARNING: Please send me this file [PF_B8G8R8A8] - Press a key to continue . . .",1))
					#print (fichero_actual)
					#print (formato_dds)
					formato_ps4 = "skip"
				else:
					__exit("ERROR: UNKNOW FORMAT ["+formato_dds+"] - "+fichero_actual+".uexp")
			
				if (formato_ps4!="skip"):			
					orbis_cmd=[orbisimage_exe,"-m",str(num_mipmaps),"-f",formato_ps4,"-i",listado_ficheros[i]['path_pc']+"\\"+listado_ficheros[i]['fichero']+".tga","-o",listado_ficheros[i]['path_pc']+"\\"+listado_ficheros[i]['fichero']+".dds_PS4"]
					sp = subprocess.run(orbis_cmd, capture_output=True, text=True)
					if (sp.returncode!=0):
						print (sp.stdout)
						print (sp.stderr)
						__exit("ERROR CONVERTING DDS FILES- "+fichero_actual+".uexp")


def inject_dds():
	__l("INJECT DDS FILES")
	for i, k in enumerate(listado_ficheros):
		print (f"\t\t\t  {i+1} - {len(listado_ficheros)}", end="\r")
		fichero_actual=listado_ficheros[i]['path_pc']+"\\"+listado_ficheros[i]['fichero']
		
		if (os.path.isfile(fichero_actual+".dds_PS4")==True):

			if (os.path.isfile(fichero_actual+".ubulk")==True):

				shutil.copy(fichero_actual+".uasset", fichero_actual+".uasset_PS4")
				shutil.copy(fichero_actual+".uexp", fichero_actual+".uexp_PS4")

				with open(fichero_actual+".ubulk_PS4", "wb") as f_ubulk_ps4:
					with open(fichero_actual+".dds_PS4", "rb") as f_dds_ps4:
						f_dds_ps4.seek(256)
						f_ubulk_ps4.write(f_dds_ps4.read())

			else:
				if (os.path.isfile(fichero_actual+".uexp")==True):

					shutil.copy(fichero_actual+".uasset", fichero_actual+".uasset_PS4")

					size_header=get_info_uexp(fichero_actual+".uexp")[0]
					with open(fichero_actual+".uexp_PS4", "wb") as f_uesp_ps4:
						with open(fichero_actual+".uexp", "rb") as f_uesp:
							f_uesp_ps4.write(f_uesp.read(size_header))
							with open(fichero_actual+".dds_PS4", "rb") as f_dds_ps4:
								f_dds_ps4.seek(256)
								f_uesp_ps4.write(f_dds_ps4.read())
							f_uesp.seek(-20,2)
							f_uesp_ps4.write(f_uesp.read())


def patch_offsets():
	__l("PATCHING OFFSETS")

	for i, k in enumerate(listado_ficheros):
		print (f"\t\t\t  {i+1} - {len(listado_ficheros)}", end="\r")

		fichero_actual=listado_ficheros[i]['path_pc']+"\\"+listado_ficheros[i]['fichero']
		if (os.path.isfile(fichero_actual+".dds_PS4")==True):

			size_uasset=os.stat(fichero_actual+".uasset_PS4").st_size
			size_uexp=os.stat(fichero_actual+".uexp_PS4").st_size

			if (listado_ficheros[i]['ubulk']==0):
				if (os.path.isfile(fichero_actual+".uasset_PS4")==True):

					with open(fichero_actual+".uasset_PS4", 'r+b') as ff:
						ff.seek(169)
						new_value=size_uasset+size_uexp-4
						ff.write(new_value.to_bytes(4, byteorder='little'))
						ff.seek(-92,2)
						new_value=size_uexp-4
						ff.write(new_value.to_bytes(4, byteorder='little'))

				if (os.path.isfile(fichero_actual+".uexp_PS4")==True):

					size_header,formato_dds,num_mipmaps,offset_header=get_info_uexp(fichero_actual+".uexp")

					with open(fichero_actual+".uexp_PS4", 'r+b') as ff:
						ff.seek(offset_header-20)
						new_value=size_uasset+size_uexp-4-8
						ff.write(new_value.to_bytes(4, byteorder='little'))

						with open(fichero_actual+".dds_PS4", "rb") as ff_dds:
							ff_dds.seek(44)
							new_value = int.from_bytes(ff_dds.read(4), byteorder='little')

						ff.seek(offset_header+len(formato_dds)+17)
						ff.write(new_value.to_bytes(4, byteorder='little'))
						ff.write(new_value.to_bytes(4, byteorder='little'))


def replace_files():
	__l("REEPLACING CONVERTED FILES")

	for i, k in enumerate(listado_ficheros):
		print (f"\t\t\t  {i+1} - {len(listado_ficheros)}", end="\r")
		fichero_actual_pc=listado_ficheros[i]['path_pc']+"\\"+listado_ficheros[i]['fichero']
		fichero_actual_ps4=listado_ficheros[i]['path_ps4']+"\\"+listado_ficheros[i]['fichero']

		if (os.path.isfile(fichero_actual_pc+".uasset_PS4")==True):
			shutil.copy(fichero_actual_pc+".uasset_PS4", fichero_actual_ps4+".uasset")

		if (os.path.isfile(fichero_actual_pc+".uexp_PS4")==True):
			shutil.copy(fichero_actual_pc+".uexp_PS4", fichero_actual_ps4+".uexp")

		if (os.path.isfile(fichero_actual_pc+".ubulk_PS4")==True):
			shutil.copy(fichero_actual_pc+".ubulk_PS4", fichero_actual_ps4+".ubulk")


def create_pak(pak_file):
	__l("CREATING PAK FILE")

	unrealpak_exe = "%s\\tools\\unrealpak\\UnrealPak.exe" % (APP_PATH)
	unrealpak_path = "%s\\tools\\unrealpak\\path2.txt" % (APP_PATH)
	pak_files = TMP_PATH+"\\ps4\\Game\\*"

	with open(unrealpak_path, "w") as out_file:
		out_file.write("\""+pak_files+"\"   \"../../../"+GAMEPATH+"/Content/\"")

	if (PAK_COMPRESS==1):
		unrealpak_create_cmd=[unrealpak_exe,pak_file,"-Create="+unrealpak_path,"-compress"]
	else:
		unrealpak_create_cmd=[unrealpak_exe,pak_file,"-Create="+unrealpak_path]
	sp = subprocess.run(unrealpak_create_cmd, capture_output=True, text=True)
############################



######### MAIN ###########
if __name__ == '__main__':

	if(len(sys.argv)==2):
		os.system('cls')
		print ("\n\n")
		__l("START PAK PC TO PS4 MOD CONVERTER")

		if(os.path.isfile(sys.argv[1])==False): __exit("ERROR OPPENING PAK FILE")
		ps4_pak_filename=__get_ps4_pak_filename(sys.argv[1])
		
		if (os.path.isdir(APP_PATH+"\\tools")==False): os.makedirs(APP_PATH+"\\tools", exist_ok=True)
		if (os.path.isdir(APP_PATH+"\\tools\\profiles")==False): os.makedirs(APP_PATH+"\\tools\\profiles", exist_ok=True)
		if (os.path.isdir(APP_PATH+"\\tools\\unrealpak")==False): os.makedirs(APP_PATH+"\\tools\\unrealpak", exist_ok=True)
		if (os.path.isdir(APP_PATH+"\\tools\\umodel")==False): os.makedirs(APP_PATH+"\\tools\\umodel", exist_ok=True)
		if (os.path.isdir(APP_PATH+"\\tools\\orbis-image2gnf")==False): os.makedirs(APP_PATH+"\\tools\\orbis-image2gnf", exist_ok=True)

		__load_ini()
		
		if(CHECK_REQUISITES==1): __check_requisites()
		
		__select_profile()
		if(AUTO_SET_PROFILE==1): __save_default_profile()
			
		cleaning_paths()
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		extract_content_pak(sys.argv[1])
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		listado_ficheros=get_files_to_process()
		if(len(listado_ficheros)==0): __exit("ERROR NO IMAGE FILES TO CONVERT")
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		convert_dds()
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		inject_dds()
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		patch_offsets()
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		replace_files()
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		create_pak(ps4_pak_filename)
		if(PAUSE_STEP==1): input(__l("PAUSE - Press a key to continue . . .",1))

		__l("CLEANING TRASH")
		if (os.path.isdir(APP_PATH+"\\tmp")==True): shutil.rmtree(APP_PATH+"\\tmp")

		if(PAUSE_FINISH==1): input(__l("FINISH PAK PC TO PS4 MOD CONVERTER] - Press a key to continue . . .",1))
	else:
		print ("\n  CodeVein PAK PC to PS4\n   >> Use: %s fichero_pak" % (os.path.basename(__file__)))
######### MAIN ###########
