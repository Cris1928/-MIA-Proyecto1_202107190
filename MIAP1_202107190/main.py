from mkdisk import mkdisk, rmdisk, fdisk
class Scanner:

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

        return None,None

    def inicio (self):

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
                    #mkdisk -size=3000 -unit=K -path=\Users\USER\Desktop\MIAP1_202107190\discos\prueba.dk
                    #mkdisk -size=3000 -unit=K -path=\Users\USER\Desktop\MIA_Prueba\p.dk
                    #fdisk -type=P -unit=M -name=Part1 -size=15 -path=\Users\USER\Desktop\MIA_Prueba\p.dk
                    #fdisk -delete=Full -name=Part_1 -path=\Users\USER\Desktop\MIAP1_202107190\discos\prueba.dk
                    #fdisk -type=P -unit=M -name=Part1 -size=15 -path=\Users\USER\Desktop\MIAP1_202107190\discos\ultim.dk
                    # mount -path=\Users\USER\Desktop\MIAP1_202107190\discos\prueba.dk -name=Part_1
                    #
                    mkdisk(coamando)
            elif opcion==4:
                if "size" in coamando:
                    coamando["size"]=int(coamando["size"])   

                fdisk(coamando)



if __name__ == "__main__":
    scanner = Scanner()
    scanner.inicio()