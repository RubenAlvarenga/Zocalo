# -*- coding: utf-8 -*-
#!/usr/bin/env python
#import psycopg2
import socket
#import sys
#import time
import datetime


class Zocalo:
    """objeto Zocalo recibe la direcion ip desde donde va a operar y el puerto correspondiente"""
    def __init__(self, ipServidor="localhost", puerto=9999):
        self.ipServidor = ipServidor
        self.puerto = puerto
        self.servidor = self.iniciarSocket()
        self.sc = ""
        self.addr = ""

    def iniciarSocket(self):
        servidor = socket.socket()
        servidor.bind((self.ipServidor, self.puerto))
        servidor.listen(1)
        return servidor

    def escucharVariasVeces(self, funcionTren, archivolog):
        """recibe como argumento una funcion en la que se debera definir la respuesta al tren de entrada
        mantiene la coneccion mientras no se reciba la palabra quit"""
        log = open(archivolog, "a+")
        salida = "\n"+str(datetime.datetime.now())+" Escuchando varias.............................. \n"
        log.write(salida)
        log.close()
        self.sc, self.addr = self.servidor.accept()
        print "ESCUCHADO A: ", self.addr
        while True:
            recibido = self.sc.recv(1024)
            if recibido == "quit":
                self.sc.send(recibido)
                self.detenerSocket()
                break
            else:
                r = funcionTren(recibido)
                respuesta = str(r)
                print "Recibido:", recibido
                print "Respuesta:", respuesta
                self.sc.send(respuesta)

    def escucharUnaVez(self, funcionTren, archivolog):
        """recibe como argumento una funcion en la que se debera definir la respuesta al tren de entrada
        mantiene la coneccion hasta el envio de la respuesta"""
        while True:
            log = open(archivolog, "a+")
            salida = "\n"+str(datetime.datetime.now())+" Escuchando...................................................................... \n"
            log.write(salida)
            log.close()
            self.sc, self.addr = self.servidor.accept()
            log = open(archivolog, "a+")
            salida = "\n"+str(datetime.datetime.now())+" Escuchando a "+str(self.addr)
            log.write(salida)
            log.close()
            if self.addr[0] == '192.168.3.106' or self.addr[0] == '192.168.3.10':
                recibido = self.sc.recv(1024)
                if recibido:
                    log = open(archivolog, "a+")
                    salida = "\n"+str(datetime.datetime.now())+" Tren Recibido : "+str(recibido)
                    log.write(salida)
                    log.close()
                    if recibido == "quit":
                        self.sc.send(recibido)
                        self.detenerSocket()
                        break
                    else:
                        r = funcionTren(recibido)
                        respuesta = str(r)
                        log = open(archivolog, "a+")
                        entrada = "\n"+str(datetime.datetime.now())+" Tren Recibido : "+str(recibido)
                        salida = "\n"+str(datetime.datetime.now())+" Tren Respuesta: "+str(respuesta)
                        log.write(entrada)
                        log.write(salida)
                        log.close()
                        self.sc.send(respuesta)
                        self.sc.close()
                        log = open(archivolog, "a+")
                        salida = "\n"+str(datetime.datetime.now())+" Desconectado a: "+str(self.addr)
                        log.write(salida)
                        log.close()
            else:
                salida = "\n"+str(datetime.datetime.now())+" "+str(self.addr)+" No es una Direccion Válida"
                log = open(archivolog, "a+")
                log.write(salida)
                log.close()
                self.sc.close()


    def detenerSocket(self):
        print "socket cerrado"
        self.sc.close()
        self.servidor.close()
