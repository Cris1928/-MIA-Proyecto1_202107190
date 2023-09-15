import os
def rmdisk(params): #aqui se elimina el disco
    filename = params.get('path') #aqui se obtiene el nombre del disco

    # se verifica que el parametro obligatorio este
    if not filename: #si no esta
        print("-El parámetro de ruta es obligatorio.!") #se imprime el error
        return #se retorna

    # se obtiene la ruta completa del archivo
    current_directory = os.getcwd() #aqui se obtiene el directorio actual
    full_path = f'{filename}' #aqui se obtiene la ruta completa del archivo

    # si el archivo no existe, se imprime el error
    if not os.path.exists(full_path):
        print(f"Error: The file {full_path} does not exist.")
        return

    # Preguntar si esta seguro de eliminar el disco
    response = input(f"deseas eliminar el  {full_path}? (s/n): ").strip().lower() #aqui se pregunta si se desea eliminar el disco

    if response == 's': #si la respuesta es si
        os.remove(full_path) #se elimina el disco
        print(f"Disk {full_path} eliminado.") #se imprime el mensaje de exito
    elif response == 'n': #si la respuesta es no
        print("disco no eliminado") #se imprime el mensaje de no eliminado
    else:
        print("opcion invalida.") #se imprime el mensaje de opcion invalida