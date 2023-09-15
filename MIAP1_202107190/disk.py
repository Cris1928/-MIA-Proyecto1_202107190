import main
import os
import mkdisk
class Disk:
    def __init__(self):
        pass

    @staticmethod
    def validarDatos(tokens):
        size = ""
        fit = ""
        unit = ""
        path = ""
        error = None
        for token in tokens:
            tk = token[:token.find('=')]
            token = token[token.find('=') + 1:]
            if main.Scanner.comparar(tk, "fit"):
                if not fit:
                    fit = token.upper()
                else:
                    error = True
                    print("\tMKDISK: parametro f repetido en el comando", tk)
            elif main.Scanner.comparar(tk, "size"):
                if not size:
                    size = token
                else:
                    error = True
                    print("\tMKDISK: parametro SIZE repetido en el comando", tk)
            elif main.Scanner.comparar(tk, "unit"):
                if not unit:
                    unit = token.upper()
                else:
                    error = True
                    print("\tMKDISK: parametro U repetido en el comando", tk)
            elif main.Scanner.comparar(tk, "path"):
                if not path:
                    path = token
                else:
                    error = True
                    print("\tMKDISK: parametro PATH repetido en el comando", tk)
            else:
                error = True
                print("\tMKDISK: no se esperaba el parametro", tk)
                break

        if not fit:
            fit = "FF"
        if not unit:
            unit = "M"
        if error:
            return

        if not path and not size:
            print("\tERROR: Se requiere parametro Path y Size para el comando MKDISK")
        elif not path:
            print("\tERROR: Se requiere parametro Path para el comando MKDISK")
        elif not size:
            print("\tERROR: Se requiere parametro Size para el comando MKDISK")
        elif fit not in ["BF", "FF", "WF"]:
            print("\tERROR: Valores en parametro fit del comando MKDISK no esperados")
        elif unit not in ["K", "M"]:
            print("\tERROR: Valores en parametro unit del comando MKDISK no esperados")
        else:

            diccionario = {"size": size, "fit": fit, "unit": unit, "path": path}
            mkdisk.mkdisk(diccionario)