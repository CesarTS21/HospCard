#! /usr/bin/env python

from appJar import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import sys
from mfrc522 import SimpleMFRC522


cred = credentials.Certificate('/home/pi/HospCard/cred.json')

firebase_admin.initialize_app(cred, {
 'databaseURL': 'https://hospcard-2b99a.firebaseio.com/'
})

reader = SimpleMFRC522()

def launch(win):
    if win == "Informacion":
	program.showSubWindow("_Informacion")
    elif win == "Instrucciones":
	program.showSubWindow("_Instrucciones")
    elif win == "Cerrar":
	act = program.okBox("Advertencia.", "Seguro que desea salir del programa?")
	if act == True:
		quit()
	    
       
	
def _Escanear(res):
    if res == "Escanear":
	program.infoBox("Mensaje", "Coloque la tarjeta en el Escaner.")
	try:
	    id, scan1 = reader.read()
	    program.showSubWindow('loading.')
	    program.setMeter("pro", 10, text=None)
	    program.setLabel("Id", "ID:" + scan1.strip())
	    rNom = db.reference('Pacientes/'+ scan1.strip() +'/Nombre')
	    rEd = db.reference('Pacientes/'+ scan1.strip() +'/Edad')
	    rGen = db.reference('Pacientes/'+ scan1.strip()+'/Genero')
	    rMun = db.reference('Pacientes/'+ scan1.strip() +'/Municipio')
	    rNac = db.reference('Pacientes/'+ scan1.strip() +'/Nacionalidad')
	    rTSa = db.reference('Pacientes/'+ scan1.strip() +'/Tipo_de_sangre')
	    rAl1 = db.reference('Pacientes/'+ scan1.strip() +'/Alergia1')
	    rAl2 = db.reference('Pacientes/'+ scan1.strip() +'/Alergia2')
	    rAl3 = db.reference('Pacientes/'+ scan1.strip() +'/Alergia3')
	    program.setMeter("pro", 30, text=None)
	    rEmf1 = db.reference('Pacientes/'+ scan1.strip() +'/Emfermedad1')
	    rEmf2 = db.reference('Pacientes/'+ scan1.strip() +'/Emfermedad2')
	    rEmf3 = db.reference('Pacientes/'+ scan1.strip() +'/Emfermedad3')
	    rEmf4 = db.reference('Pacientes/'+ scan1.strip() +'/Emfermedad4')
	    rEmf5 = db.reference('Pacientes/'+ scan1.strip() +'/Emfermedad5')
	    
	    program.setMeter("pro", 50, text=None)
	    program.setLabel("Nombre:", rNom.get())
	    program.setLabel("Genero:", rGen.get())
	    program.setLabel("Edad:" ,rEd.get())
	    program.setLabel("Municipio:", rMun.get())
	    program.setLabel("Nacionalidad:", rNac.get())
	    program.setLabel("Tipo_de_sangre:", rTSa.get())
	    program.setLabel("Alergia1:", rAl1.get())
	    program.setLabel("Alergia2:", rAl2.get())
	    program.setLabel("Alergia3:", rAl3.get())
	    program.setMeter("pro", 80, text=None)
	    program.setLabel("Emfermedad1:", rEmf1.get())
	    program.setLabel("Emfermedad2:", rEmf2.get())
	    program.setLabel("Emfermedad3:", rEmf3.get())
	    program.setLabel("Emfermedad4:", rEmf4.get())
	    program.setLabel("Emfermedad5:", rEmf5.get())
	    program.setMeter("pro", 100, text=None)
	finally:
	    GPIO.cleanup()
	    program.hideSubWindow("loading.")
	    #program.removeMeter("pro")
    elif res == "Limpiar":
	program.setLabel("Nombre:", "__________________________")
	program.setLabel("Edad:" , "_____")
	program.setLabel("Genero:", "_______")
	program.setLabel("Municipio:", "_____________")
	program.setLabel("Nacionalidad:", "________________")
	program.setLabel("Tipo_de_sangre:", "_______")
	program.setLabel("Alergia1:", "__________")
	program.setLabel("Alergia2:", "__________")
	program.setLabel("Alergia3:", "__________")
	program.setLabel("Emfermedad1:", "____________")
	program.setLabel("Emfermedad2:", "____________")
	program.setLabel("Emfermedad3:", "____________")
	program.setLabel("Emfermedad4:", "____________")
	program.setLabel("Emfermedad5:", "____________")
	    

def _Registrar(des):
    if des == "Registrar":
	RId = program.getEntry("ID")
	RNombre = program.getEntry("Nombre")
	REdad = program.getEntry("Edad")
	RGenero = program.getOptionBox(".")
	RMunicipio = program.getOptionBox("-")
	RNacionalidad = program.getEntry("Nacionalidad")
	RTipoSangre = program.getOptionBox("*")
	RAl1 = program.getEntry("Alergia1")
	RAl2 = program.getEntry("Alergia2")
	RAl3 = program.getEntry("Alergia3")
	REmf1 = program.getEntry("Emfermedad1")
	REmf2 = program.getEntry("Emfermedad2")
	REmf3 = program.getEntry("Emfermedad3")
	REmf4 = program.getEntry("Emfermedad4")
	REmf5 = program.getEntry("Emfermedad5")
	
	db.reference('Pacientes').update({
	    RId: {
		'Nombre': RNombre,
		'Edad': REdad,
		'Genero': RGenero,
		'Municipio': RMunicipio,
		'Nacionalidad': RNacionalidad,
		'Tipo_de_sangre': RTipoSangre,
		'Alergia1': RAl1,
		'Alergia2': RAl2,
		'Alergia3': RAl3,
		'Emfermedad1': REmf1,
		'Emfermedad2': REmf2,
		'Emfermedad3': REmf3,
		'Emfermedad4': REmf4,
		'Emfermedad5': REmf5
	    }
	})
	
	program.infoBox("Mensaje", "Registro completado.")
    elif des == "Limpiar.":
	program.setEntry("ID", "")
	program.setEntry("Nombre", "")
	program.setEntry("Edad", "")
	program.setEntry("Nacionalidad", "")
	program.setEntry("Alergia1", "")
	program.setEntry("Alergia2", "")
	program.setEntry("Alergia3", "")
	program.setEntry("Emfermedad1", "")
	program.setEntry("Emfermedad2", "")
	program.setEntry("Emfermedad3", "")
	program.setEntry("Emfermedad4", "")
	program.setEntry("Emfermedad5", "")
	
def _Grabar(ans):
     if ans == "Grabar":
	program.infoBox("Msg", "Coloque la tarjeta en el Escaner para grabarla.")
	try:
	    texto = program.getEntry("Codigo: ")
	    reader.write(texto)
	    program.infoBox("Msg2", "El codigo "+texto+" se ha grabado en la tarjeta.") 
	finally:
	    GPIO.cleanup()
     elif ans == "limpiar":
	program.setEntry("Codigo: ", "")

program = gui("HospCard", "800x520")

#program.showSplash("Cargado el progrma...", fill='blue', stripe='black',
#    fg='white', font=20)
program.setImageLocation("/home/pi/HospCard/Fondos")
program.startSubWindow("loading.")
program.setSize(300, 150)
program.addLabel("t1", " Cargando... ")
program.addMeter("pro")
program.setMeterFill("pro", "blue")
program.stopSubWindow()

program.startSubWindow("_Informacion")
program.setSize(600, 500)
program.addLabel("g1", " Informacion acerca del programa. ")
program.addLabel("g2", """
		Este es un software de analis y escaneo de                   .
		datos su pirncipal funcion es facilitar y 
		agilisar los tiempo de registro y generacion 
		de diagnotico oportuno en los hospitales, 
		ademas, permite la generacion de una base 
		de infomracion de padecimientos y alegias 
		que tiene los pacientes lo cual aumenta la 
		infomacion recompilada y permite mejorar 
		la atencion medica bindada a los pacientes.  
    
		Es uso de este software esta orientado a las       
		clinicas mediaca y las recepciones hopitalarias,  
		esta creado para ser facil de usar y cuneta        
		con servicios en la Web, que implementan           
		tecnologias de IT en el area de atencion medica.
		""")  
program.setBg("white")
program.stopSubWindow()

program.startSubWindow("_Instrucciones")
program.addLabel("r2", """
		1. Realice el alta del paciente capturando			.
		toda la informacion solicitada.
		2. Grabe el codigo unico de identificacion 
		en la tarjeta
		3. Encane la tarjeta para asegurarse de que 
		la informacion esta en la nube
		
		Ahora el paciente ya cuenta con su usuario 
		activo para usarlo el servicio en su 
		proxima cita.
		""")  
program.setSize(500, 400)


#program.setBgImage("ime.jpeg")
program.addLabel("r1", " Indicaciones de uso del programa. ")
program.stopSubWindow()

program.startTabbedFrame("Vista")
program.setTabbedFrameTabExpand("Vista", expand=True)
program.startTab("Inicio")
#program.setBgImage("fondo_1.jpeg")
#program.setBg("white")

program.addLabel("l1", "Bienvenido al sistema HospCard.")
program.setLabelBg("l1", "light blue")
program.setLabelFg("l1", "white")
program.getLabelWidget("l1").config(font=("Sans Serif", "22", "bold"))
program.setFont(16)
#program.addImage("Hello", "ime.jpeg")
program.addLabel("l2", "- Acciones -")
program.setLabelFg("l2", "#65C749")
program.getLabelWidget("l2").config(font=("Sans Serif", "28", "bold"))
program.addButtons(["Informacion", "Instrucciones", "Cerrar"],launch)
program.addLabel("l3", "")
program.setLabelBg("l3","light blue")

program.stopTab()

program.startTab("Escanear")
program.setBg("#6895FE")
program.addLabel("A", "Informacion del paciente.")
program.setLabelBg("A", "#EDEFF3")
program.getLabelWidget("A").config(font=("Sans Serif", "20", "bold"))
program.addLabel("Id","ID:______________ ")
program.setLabelBg("Id","light blue")
program.startLabelFrame("Datos del paciente")
program.setLabelFrameBg("Datos del paciente","white")
program.setSticky("ew")

program.addLabel("A0", "Nombre:", 0, 0)
program.addLabel("Nombre:", "__________________________", 0, 1, 3)
program.addLabel("A1", "Edad:", 1, 0)
program.addLabel("Edad:", "_____", 1, 1)
program.addLabel("A2", "Genero:", 2, 0)
program.addLabel("Genero:", "_______", 2, 1)
program.addLabel("A3", "Municipio:", 3, 0)
program.addLabel("Municipio:","_____________", 3, 1)
program.addLabel("A4", "Nacionalidad:", 4, 0)
program.addLabel("Nacionalidad:","________________", 4, 1)
program.addLabel("A5", "Tipo de sagre:", 5, 0)
program.addLabel("Tipo_de_sangre:", "_______", 5, 1)

program.addLabel("A6", "Alergia 1:", 1, 3)
program.addLabel("Alergia1:", "__________", 1, 4)
program.addLabel("A7", "Alergia 2:", 2, 3)
program.addLabel("Alergia2:", "__________", 2, 4)
program.addLabel("A8", "Alergia 3:", 3, 3)
program.addLabel("Alergia3:", "__________", 3, 4)
program.addLabel("A9", "Emfermedad 1:", 4, 3)
program.addLabel("Emfermedad1:", "____________", 4, 4)
program.addLabel("A10", "Emfermedad 2:", 5, 3)
program.addLabel("Emfermedad2:", "____________", 5, 4)
program.addLabel("A11", "Emfermedad 3:", 6, 3)
program.addLabel("Emfermedad3:", "____________", 6, 4)
program.addLabel("A12", "Emfermedad 4:", 7, 3)
program.addLabel("Emfermedad4:", "____________", 7, 4)
program.addLabel("A13", "Emfermedad 5:", 8, 3)
program.addLabel("Emfermedad5:", "____________", 8, 4)
program.stopLabelFrame()

program.addButtons(["Escanear", "Limpiar"], _Escanear, colspan=4)
program.stopTab()


program.startTab("Registrar")
program.setBg("#6895FE")
program.addLabel("B", "Generar registro de paciente.")
program.setLabelBg("B","#EDEFF3")
program.startLabelFrame("Informacion")
program.setLabelFrameBg("Informacion", "white")
program.setSticky("ew")

program.addLabel("B0", "ID", 0, 0)
program.addEntry("ID", 0, 1)
program.addLabel("B1", "Nombre", 1, 0)
program.addEntry("Nombre", 1, 1)
program.addLabel("B2", "Edad", 2, 0)
program.addEntry("Edad", 2, 1)
program.addLabel("B3", "Genero", 3, 0)
program.addLabelOptionBox(".", ["- Seleccion -", "Masculino", "Femenino"
    ],3 ,1)
program.addLabel("B4", "Municipio", 4, 0)
program.addLabelOptionBox("-", ["- Municipios -", "Aguascalientes", "Baja California", "Baja California Sur",
    "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Durango", "Estado de Mexico",
    "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacan", "Morelos", "Nayarit",
    "Nuevo Leon", "Oaxaca", "Puebla", "Queretaro", "Quintana Roo", "San Luis Potosi", "Sinaloa",
    "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"
    ], 4, 1)
program.addLabel("B5", "Nacionalidad", 5, 0)
program.addEntry("Nacionalidad", 5, 1)
program.addLabel("B6", "Tipo de Sangre", 6, 0)
#program.addEntry("Tipo_de_sangre", 5, 1)
program.addLabelOptionBox("*", ["- Tipo -", "O+", "O-",
    "A+", "A-", "B+", "B-", "AB+", "AB-"
    ], 6, 1)
program.stopLabelFrame()

program.startLabelFrame("Padecimientos")
program.setLabelFrameBg("Padecimientos", "white")
program.setSticky("w")
program.addLabel("B7", "Alergias:", 7, 0)
program.addEntry("Alergia1", 8, 0)
program.addEntry("Alergia2", 8, 1)
program.addEntry("Alergia3", 8, 2)
program.addLabel("B8", "Emfermedades:", 9, 0)
program.addEntry("Emfermedad1", 10, 0)
program.addEntry("Emfermedad2", 10, 1)
program.addEntry("Emfermedad3", 10, 2)
program.addEntry("Emfermedad4", 11, 0)
program.addEntry("Emfermedad5", 11, 1)
program.stopLabelFrame()

program.addButtons(["Registrar", "Limpiar."], _Registrar)
program.stopTab()


program.startTab("Grabar Tarjeta")
program.setBg("#6895FE")
program.addLabel("D1", "Grabado de tarjeta de paciente", 0)
program.setLabelBg("D1", "#EDEFF3")
program.addLabel("D2", "Ingrese el codigo del paciente.", 1)
program.setLabelBg("D2","light blue")
program.addLabelEntry("Codigo: ", 2, 0)
program.addButtons(["Grabar", "limpiar"], _Grabar)

program.stopTab()
program.stopTabbedFrame()

program.go()
