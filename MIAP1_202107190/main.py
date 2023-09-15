from mkdisk import mkdisk, fdisk
from rmdisk import rmdisk
from mkfs import mkfs,login,makeuser,makegroup,remuser,remgroup
from mount import mount

from mount import unmount
usuarios_montados = [] #se crea una lista vacia
usuarios = None
part_act=None
#global cont
cont=0



class Scanner:
   
    
    @staticmethod
    def mayusculas(a):
        return a.upper() 
    

    @staticmethod
    def comparar(a, b):
        return a.upper() == b.upper()
        
    @staticmethod
    def confirmar(mensaje):
        respuesta = input(f"{mensaje} (y/n)\n\t").lower()
        return respuesta == "y" 
    
    def comando(self, text):
        tkn = ""
        terminar = False
        for c in text:
            if terminar:
                if c == ' ' or c == '-':
                    break
                tkn += c
            elif c != ' ' and not terminar:
                if c == '#':
                    tkn = text
                    break
                else:
                    tkn += c
                    terminar = True
        return tkn

    def separar_tokens(self, text):
        tokens = []
        diccionario = {}
        if not text:
            return tokens
        text += ' '
        token = ""
        estado = 0
        for c in text:
            if estado == 0 and c == '-':
                estado = 1
            elif estado == 0 and c == '#':
                continue
            elif estado != 0:
                if estado == 1:
                    if c == '=':
                        estado = 2
                    elif c == ' ':
                        continue
                elif estado == 2:
                    if c == '\"':
                        estado = 3
                        continue
                    else:
                        estado = 4
                elif estado == 3:
                    if c == '\"':
                        estado = 4
                        continue
                elif estado == 4 and c == '\"':
                    tokens.clear()
                    continue
                elif estado == 4 and c == ' ':
                    estado = 0
                    tokens.append(token)
                    token = ""
                    continue
                token += c
        for token in tokens:
            tk = token[:token.find("=")]
            token = token[len(tk) + 1:]
            diccionario[tk] = token
        
        return diccionario


    def procesar_comando(self, comando):
        datos = {} 
        comand=0
        if comando.startswith("mkdisk"):
            comand=1
            partes = comando.split()  # Dividir la cadena en palabras
        # print("abajo")
            #print(partes)
            #print("arriba")
             # Diccionario para almacenar los valores
            parametro_actual = None  # Para mantener el parámetro actual
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]  # Eliminar el guion (-) del parámetro
                #   print(parametro_actual)
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand
        elif comando.startswith("rmdisk"):
            comand=2
            partes = comando.split()  # Dividir la cadena en palabras
            parametro_actual = None  # Para mantener el parámetro actual
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]  # Eliminar el guion (-) del parámetro
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand
        elif comando.startswith("rep"):
            comand=3
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand
                    
        elif comando.startswith("fdisk"):
            comand=4
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
         #   print(datos)        
            return datos,comand
        #      elif parametro_actual is not None:
        #         datos[parametro_actual] = palabra
            #        print(parametro_actual)
            #       print("arriba")
            #      parametro_actual = None
        
        elif comando.startswith("mount"):
            comand=5
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
         #   print(datos)        
            return datos,comand
        
        elif comando.startswith("unmount"):
            comand=6
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            #   print(datos)    
            return datos,comand
        
        elif comando.startswith("mosumon"):
            comand=7
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            #   print(datos)    
            return datos,comand
        elif comando.startswith("mkfs"):
            comand=8
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            #   print(datos)    
            return datos,comand

        elif comando.startswith("login"):
            comand=9
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand
        
        elif comando.startswith("logout"):
            comand=10
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand  
        
        elif comando.startswith("mkgrp"):

            comand=11
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand  

        elif comando.startswith("mkusr"):
            comand=12
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand  
        
        elif comando.startswith("rmusr"):
            comand=13
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand  
        elif comando.startswith("execute"):
            comand=14
            partes = comando.split()
            parametro_actual = None
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor
            return datos,comand 

        return None,None
    
    def funcion_excec(self, tokens):
        path = ""
        for token in tokens:
            tk = token[:token.find("=")]
            token = token[len(tk) + 1:]
            if self.comparar(tk, "path"):
                path = token
        if not path:
            print("\tERROR: Se requiere la propiedad path para el comando EXEC") 
            return
        self.excec(path)

    def excec(self, dicc):
        global cont
        filename = dicc.get('path')
        lines = []
        with open(filename, "r") as input_file:
            for line in input_file:
                lines.append(line.strip())
        for i in lines:
            texto = i
            tk = self.comando(texto)
            if texto:
                if self.comparar(texto, "PAUSE"):
                    print("************** FUNCION PAUSE **************")
                    input("Presione enter para continuar...")
                    continue
                texto = texto[len(tk) + 1:]
                tks = self.separar_tokens(texto)

                if tk.startswith("#"):
                    continue
                #print(tk)
                if "size" in tks:
                    tks["size"]=int(tks["size"])
            
                

                print(tks) #diccionario
                if tk.startswith("mkdisk"):
                    
                    mkdisk(tks)
                elif tk.startswith("rmdisk"):
                    rmdisk(tks)
                elif tk.startswith("fdisk"):
                    fdisk(tks)
                elif tk.startswith("mkfs"):
                    mkfs(tks, usuarios_montados)
                elif tk.startswith("mount"):
                    print(cont)
                    mount(tks,usuarios_montados,cont)
                    cont=cont+1
                elif tk.startswith("unmount"):
                    unmount(tks,usuarios_montados)
                elif tk.startswith("login"):
                    usuarios,part_act= login(tks,usuarios_montados)
                elif tk.startswith("logout"):
                    print("logout")
                elif tk.startswith("mkgrp"):
                    makegroup(tks,usuarios_montados,part_act)
                elif tk.startswith("mkusr"):
                    makeuser(tks,usuarios_montados,part_act)
                    




               # print(texto)




    def inicio (self):
        global cont


        while True:
            eliminar=False
            add=False
            print("SI DESEA TERMINAR EJECUCION INGRESE \"s\"")
            datoing = input("ingrese el comando:  ")
            if datoing.lower()== "s":
                break
            coamando,opcion=self.procesar_comando(datoing)
            print(coamando)
            if opcion==1:
                if "path" in coamando and "size" in coamando:
                    #si tiene path y size

                    #si no tiene fit
                    if "fit" not in coamando:
                        coamando["fit"]="FF"
                    if "unit" not in coamando:
                        coamando["unit"]="M"    
                    if "size" in coamando:
                        coamando["size"]=int(coamando["size"])   
                    #mkdisk -size=3000 -unit=K -path=prueba.dk
                    #mkdisk -size=3000 -unit=K -path=\Users\USER\Desktop\MIA_Prueba\p.dk
                    #fdisk -type=P -unit=M -name=Part1 -size=15 -path=prueba.dk
                    #fdisk  -type=P -unit=M -name=Part1 -size=15 -path=\Users\USER\Desktop\MIA_Prueba\p.dk
                    #fdisk -type=P -unit=M -name=Part1 -size=15 -path=\Users\USER\Desktop\MIAP1_202107190\discos\ultim.dk
                    # mount -path=\Users\USER\Desktop\MIA_Prueba\p.dk -name=Part1
        
                    #mkfs -type=full -id=190Disco0
                    #login -user=root -pass=123 -id=190Disco0
                    #mkgrp -name=grupo1 -id=190Disco0
                    mkdisk(coamando)
            elif opcion==4:
                if "size" in coamando:
                    coamando["size"]=int(coamando["size"])   

                fdisk(coamando)
            elif opcion==2:
                rmdisk(coamando)
            elif opcion==8:
                mkfs(coamando, usuarios_montados)
            elif opcion ==5:
                print(cont)
                mount(coamando,usuarios_montados,cont)
                cont=cont+1
            elif opcion ==6:
                unmount(coamando,usuarios_montados)
            elif opcion ==7:
                print("mostrar montados")
                for i in usuarios_montados:
                    print("id",i)
                    for id in i:
                        print("path",i[id]["path"])
                        print("name",i[id]["name"])
                        print("index",i[id]["index"])
                        print("inicio",i[id]["inicio"])
                        print("size",i[id]["size"])
                        print("partition",i[id]["partition"])
                        print("id",i[id]["id"])

            elif opcion ==9:
               usuarios,part_act= login(coamando,usuarios_montados)
             #  print(usuarios)
               print("login")
            elif opcion ==10:
                print("logout")
            elif opcion ==11:
                makegroup(coamando,usuarios_montados,part_act)
            elif opcion ==12:
                makeuser(coamando,usuarios_montados,part_act)
            elif opcion ==14:
                self.excec(coamando)



if __name__ == "__main__":
    scanner = Scanner()
    scanner.inicio()