import os
import disk as disk 
class Scanner:
    def __init__(self): 
        pass 
    @staticmethod
    def NotCaseSensitive(texto):
        return texto.upper()
    
    @staticmethod
    def Comparador(texto1, texto2):
        return texto1.upper() == texto2.upper()
    
    @staticmethod 
    def ParaError(errOps, Mensaje):
        print(f"Error en el comando: {errOps}; Causa:{Mensaje}")
    
    @staticmethod
    def ParaAciertos(OperacionAcertada, Mensaje): 
        print(f"Acierto en el comando {OperacionAcertada}; Causa:{Mensaje}") 
    
    @staticmethod
    def ParaConfirmaciones(Texto):
        Opcion_in = input(f"{Texto} (s/n)")
        return Opcion_in == "S"
    def ParaExecute(self, tokens): 
        path = ""
        for token in tokens:
            tk = token[:token.find("=")]
            token =token[len(tk)+1:]
            if self.Comparador(tk, "path"):
                path = token 
        if not path:
            self.ParaError("Execute", "No se encontro la propiedad path")
            return
        self.execute(path)
    
    def execute(self, path):
        filename =path 
        lineas = []
        with open(filename, "r") as input_file:
            for linea in input_file:
                lineas.append(linea.strip())
        for a in lineas:
            texto = a
            tk = self.ComandoAEjecutar(texto)
            if texto:
                if self.Comparador(texto, "pausa"):
                    print ("*********** PAUSA ***********")
                    input("Presiona enter")
                    continue
                texto = texto[len(tk)+1:]
                tks = self.TokemnSeparado(texto)
                self.funciones(tk,tks)

    def ComandoAEjecutar (self,Line_comand):
        m_token = ""
        Fin = False
        for caracter in Line_comand:
            if Fin:
                if caracter == ' ' or caracter == '-':
                    break
                m_token += caracter
            elif caracter != ' ' and not Fin:
                if caracter == '#':
                    m_token = Line_comand
                    break
                else: 
                    m_token += caracter
                    Fin = True
        return m_token

    def TokemnSeparado (self,texto):
        arregloToken =[]
        if not texto:
            return arregloToken
        texto += ' '
        m_token= ""
        bandera = 0; 

        for caracter in texto: 
            if bandera == 0 and caracter == "-":
                bandera = 1 
            elif bandera == 0 and caracter == "#":
                continue
            elif bandera != 0:
                if bandera == 1:
                    if caracter == "=":
                        bandera = 2
                    elif caracter == " ":
                        continue
                elif bandera == 2:
                    if caracter == '\"':
                        bandera = 3
                        continue
                    else: 
                        bandera = 4
                elif bandera == 3:
                    if caracter == '\"':
                        bandera = 4
                        continue
                elif bandera == 4  and caracter == '\"':
                    arregloToken.clear()
                    continue
                elif bandera == 4 and caracter == ' ':
                    bandera = 0
                    arregloToken.append(m_token)
                    m_token = ""
                    continue
                m_token += caracter     
        return arregloToken

    def inicio (self):
        while True:
            print("SI DESEA TERMINAR EJECUCION INGRESE \"s\"")
            datoing = input("ingrese el comando:  ")
            if datoing.lower()== "s":
                break
            token = self.ComandoAEjecutar(datoing) 
            datoing = datoing[len(token)+1:] 
            tokens =self.TokemnSeparado(datoing)    
            self.funciones(token,tokens)
            input ("enter para continuar")

    def funciones(self, token, arrTokens):
        if token:
            if token.upper() == "MKDISK":
                disk.Disk.Crear()
            elif token.upper() == "REP":
                print( "*********** COMANDO REP  *********")
                disk.Disk.rep()
            elif token.startswith("#"):
                print ("Este es un comentario")
                print (token)
            elif token.upper() == "EXECUTE": ############
                self.ParaExecute(arrTokens)
            else:
                self.ParaError("Analizador",f" No se reconoce el comando \"{token}\"")
    


if __name__ == "__main__":
    scanner = Scanner()
    scanner.inicio()


         
                 


