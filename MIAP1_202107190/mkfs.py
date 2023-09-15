from FORMATEO.ext2.ext2 import Superblock, Inode, FolderBlock, FileBlock, PointerBlock, block, Content, Journal
import os
import struct
import time
import random

from fun_users import cargar_usuarios, parse_users, auten_usuarios, get_id_by_group, extract_active_groups,get_group_id
def mkfs(params, mounted_partitions): # obtener el id de la particion
    tipo = params.get('type', 'full').lower() # obtener el tipo de formateo
    id = params.get('id', None) # obtener el id de la particion
    fsext = params.get('fs', 'ext2')
    ext = 2
    if fsext == 'ext3':
        ext = 3
    # verificar que el id exista
    partition = None # inicializar la particion
    for partition_dict in mounted_partitions: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break

    if not partition:
        print(f"Error: la particion {id} no existe.")
        return

    # recuperar los detalles de la particion
    path = partition['path'] # obtener el path
    inicio = partition['inicio'] # obtener el inicio
    size = partition['size']    # obtener el size

    

    
    # crear el superblock
    if tipo == 'full':
        print(f'size de particion: {size}')
        superblock = Superblock(inicio, int(size),ext)
        superblock.ver_bytes_inidices()
        superblock.s_free_inodes_count -= 1 # por el superblock de inodos 
        superblock.s_free_blocks_count -= 1  # por el bitmap de inodos restar 1
        filename = path # obtener el nombre del archivo
        current_directory = os.getcwd() # obtener el directorio actual
        full_path= f'{filename}' # obtener el path completo
        if not os.path.exists(full_path): # si no existe el archivo
            print(f"Error: el archivo {full_path} no existe.") # imprimir error
            return
        with open(full_path, "rb+") as file: # abrir el archivo
            
            bitmapinodos = ['0']*superblock.s_inodes_count # crear el bitmap de inodos
            bitmapbloques = ['0']*superblock.s_blocks_count # crear el bitmap de bloques
            file.seek(inicio) # ir al inicio
            file.write(b'\x00'*size)   # escribir el archivo con ceros
            #crea inodo 0
            i1 = Inode() # crear el inodo
            i1.i_type = '0' # tipo de inodo
            i1.i_block[0] = superblock.s_block_start # el primer bloque es el bitmap de bloques
            #crea bloque 0
            b1 = FolderBlock() # crear el bloque
            b1.b_content[0].b_inodo = superblock.s_inode_start+Inode.SIZE # el primer inodo es el bitmap de inodos
            b1.b_content[0].b_name = 'users.txt' # nombre del archivo
            bitmapbloques[0] = '1' # el bitmap de bloques se actualiza
            bitmapinodos[0] = '1' # el bitmap de inodos se actualiza
            
            
            #crea inodo 1
            i2 = Inode() # crear el inodo
            i2.i_type = '1' # tipo de inodo
            i2.i_block[0] = superblock.s_block_start+block.SIZE # el primer bloque es el bitmap de bloques
            #crea bloque 1
            b2 = FileBlock() # crear el bloque
            b2.b_content = '1,G,root\n1,U,root,root,123\n' # contenido del archivo
            bitmapbloques[1] = '1' # el bitmap de bloques se actualiza
            bitmapinodos[1] = '1' # el bitmap de inodos se actualiza
            
            
            
            file.seek(inicio)
            file.write(superblock.pack())
            if ext == 3:
                jrnl = Journal()
                jrnl.journal_data = str(('mkfs',params))+"\n"
                file.write(jrnl.pack())
            
            for i in range(superblock.s_inodes_count):
                file.write(bitmapinodos[i].encode('utf-8'))
            for i in range(superblock.s_blocks_count):
                file.write(bitmapbloques[i].encode('utf-8'))
            file.seek(superblock.s_inode_start)
            file.write(i1.pack())
            file.write(i2.pack())
            file.seek(superblock.s_block_start)
            file.write(b1.pack())
            file.write(b2.pack())
            print(f"Particion {id} fue formateada exitosamente.") # imprimir mensaje de exito
        

def login(params, mounted_partitions): # obtener el id de la particion
    print("\t \t \t LOGIN") 
    print(params) 
#uusuario, la contraseña debe venir en parámetros, si no, devolverá el error
    try:
        user = params['user'] # obtener el usuario
        password = params['pass'] # obtener la contraseña
        id = params['id'] # obtener el id de la particion
        
    except:
        print("Error: Se necesita el usuario y la contraseña.") # imprimir error
        return None, None # retornar error
    
    partition = None # inicializar la particion

   
    for partition_dict in mounted_partitions: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break

    if not partition:
        print(f"Error: La particion con id {id} no existe.") 
        return

    # recuperar los detalles de la particion
    path = partition['path'] # obtener el path
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    current_directory = os.getcwd() # obtener el directorio actual
    full_path= f'{filename}' # obtener el path completo
    if not os.path.exists(full_path): # si no existe el archivo
        print(f"Error: el fule {full_path} no existe.") # imprimir error
        return 
    with open(full_path, "rb+") as file: # abrir el archivo
        file.seek(inicio) # ir al inicio
        superblock = Superblock.unpack(file.read(Superblock.SIZE)) # leer el superblock
        #print("ESTE ES EL SUPERBLOCK EN EL LOGIN__________________")
        #print(superblock)
        file.seek(superblock.s_inode_start) # ir al inicio de los inodos
        inodo = Inode.unpack(file.read(Inode.SIZE)) # leer el inodo
        siguiente = inodo.i_block[0] # obtener el primer bloque
        file.seek(siguiente) # ir al primer bloque
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE)) # leer el bloque
        siguiente = folder.b_content[0].b_inodo # obtener el primer inodo
        file.seek(siguiente) # ir al primer inodo
        inodo = Inode.unpack(file.read(Inode.SIZE)) # leer el inodo
        texto = "" # inicializar el texto
        for n in inodo.i_block: # recorrer los bloques
            if n != -1: # si el bloque no esta vacio
                siguiente = n # obtener el siguiente bloque
                file.seek(siguiente) # ir al siguiente bloque
                fileblock = FileBlock.unpack(file.read(FileBlock.SIZE)) # leer el bloque
                texto += fileblock.b_content.rstrip('\x00') # agregar el contenido al texto
   
        usuarios = parse_users(texto) # obtener los usuarios
        users= auten_usuarios(usuarios, user, password) # obtener el usuario si esta autenticado
        print("ESTE ES EL USUARIO EN EL LOGIN__________________") # imprimir mensaje
        print(users) # imprimir usuario
        return users,id
        
def makeuser(params, mounted_partitions,id): # obtener el id de la particion
    print("EJECUTANDO MKUSER*")
    #print(params)
    if id == None: # si el id es nulo
        print("Error: Se necesita el id.")
        return
    try: 
        user = params['user']
        password = params['pass']
        group = params['grp']
    except:
        print("Error: El usuario, contraseña y grupo son obligatorios.")
        return
    partition = None # inicializar la particion
    for partition_dict in mounted_partitions: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break

    if not partition:
        print(f"Error: La particion con id  {id} no existe.")
        return
    # Recuperar detalles de la partición.
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    current_directory = os.getcwd()
    full_path= f'{filename}'
    if not os.path.exists(full_path):
        print(f"Error: El file {full_path} no existe.")
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        siguiente = folder.b_content[0].b_inodo
        file.seek(siguiente)
        ubicacion_inodo_users = siguiente
        inodo = Inode.unpack(file.read(Inode.SIZE))
        primerbloque = -1
        cont = 0
        texto = ""
        for i,item in enumerate(inodo.i_block[:12]):
            if item != -1 and i == 0:
                primerbloque = item
            if item != -1:
                cont = i+1
                siguiente = item
                file.seek(siguiente)
                fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
                texto += fileblock.b_content.rstrip('\x00')
        indice_a_borrar = (primerbloque- superblock.s_block_start)//64   
        grupos = parse_users(texto)
        
   
        group_exists = False  # Initially, we assume the group does not exist
        for n in grupos:
            #print (n)
            #print(user)
            if user in n:
                print("Error: El usuario ya existe.")
                return
        #
        grupos22 = extract_active_groups(texto)
        group_exists2 = False  # Initially, we assume the group does not exist
        for n2 in grupos22:
            # Check if the group exists in current item
            if n2['groupname'] == group:
                group_exists2 = True
                break

        if group_exists2==False:
            print(f"Error: El grupo {group} no existe.")
            return
        #

             
        
            
        #print("ESTE ES EL USUARIO QUE SE VA A CREAR")
        id = get_group_id(group,grupos22 )
        #texto+='2,G,usuarios\n2,U,usuarios,user1,usuario\n'
        texto += f'{id},U,{group},{user},{password}\n'
        length = len(texto)
        fileblocks = length//64
        if length%64 != 0:
            fileblocks += 1
        bitmap_bloques_inicio = superblock.s_bm_block_start
        cantidad_bloques = superblock.s_blocks_count
        FORMAT = f'{cantidad_bloques}s'
        SIZE = struct.calcsize(FORMAT)
        file.seek(bitmap_bloques_inicio)
        bitmap_bloques = struct.unpack(FORMAT, file.read(SIZE))
        bitmap=bitmap_bloques[0].decode('utf-8')
        #print(bitmap)
                    
        if fileblocks<=12:
            bitmap = bitmap[:indice_a_borrar] + '0'*cont + bitmap[indice_a_borrar+cont:]
            index = bitmap.find('0'*fileblocks)
            #print(bitmap)
            a = bitmap[:index] + '1'*fileblocks + bitmap[index+fileblocks:]
            #print(a)
            chunks = [texto[i:i+64] for i in range(0, len(texto), 64)]
            for i,n in enumerate(chunks):
                new_fileblock = FileBlock()
                new_fileblock.b_content = n
                inodo.i_block[i] = primerbloque+i*64
                file.seek(primerbloque+i*64)
                file.write(new_fileblock.pack())
            #rewriteinode
            file.seek(ubicacion_inodo_users)
            file.write(inodo.pack())
            #rewrite bitmap
            file.seek(bitmap_bloques_inicio)
            file.write(a.encode('utf-8'))
            return
                        

                                        
#write a storu about                     
def makegroup(params, mounted_partitions,id):
    if id == None:
        print("Error: La identificación es requerida.")
        return
    try: 
        group = params['name']
    except:
        print("Error: El usuario, contraseña y grupo son obligatorios.")
        return
    partition = None
    for partition_dict in mounted_partitions: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break
    if not partition:
        print(f"Error: La particion con {id} no existe.")
        return
    # Retrieve partition details.
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    current_directory = os.getcwd()
    full_path= f'{filename}'
    if not os.path.exists(full_path):
        print(f"Error: El file {full_path} no existe.")
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        siguiente = folder.b_content[0].b_inodo
        file.seek(siguiente)
        ubicacion_inodo_users = siguiente
        inodo = Inode.unpack(file.read(Inode.SIZE))
        primerbloque = -1
        cont = 0
        texto = ""
        for i,item in enumerate(inodo.i_block[:12]):
            if item != -1 and i == 0:
                primerbloque = item
            if item != -1:
                cont = i+1
                siguiente = item
                file.seek(siguiente)
                fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
                texto += fileblock.b_content.rstrip('\x00')
        indice_a_borrar = (primerbloque- superblock.s_block_start)//64   
        grupos = extract_active_groups(texto)
        group_exists = False  # Initially, we assume the group does not exist
        for n in grupos:
            # Check if the group exists in current item
            if n['groupname'] == group:
                group_exists = True
                break

        if group_exists==True:
            print(f"Error: El grupo {group} ya existe.")
            return

        print("ESTE ES EL GRUPO QUE SE VA A CREAR")
        print(group)
        print(grupos)
        max_id = max(g['id'] for g in grupos)
        
        # The next available ID will be max_id + 1
        next_id = max_id + 1
        print(next_id)
        texto += f'{next_id},G,{group}\n'
        print(texto)
        length = len(texto)
        fileblocks = length//64
        if length%64 != 0:
            fileblocks += 1
        bitmap_bloques_inicio = superblock.s_bm_block_start
        cantidad_bloques = superblock.s_blocks_count
        FORMAT = f'{cantidad_bloques}s'
        SIZE = struct.calcsize(FORMAT)
        file.seek(bitmap_bloques_inicio)
        bitmap_bloques = struct.unpack(FORMAT, file.read(SIZE))
        bitmap=bitmap_bloques[0].decode('utf-8')
        #print(bitmap)
                    
        if fileblocks<=12:
            bitmap = bitmap[:indice_a_borrar] + '0'*cont + bitmap[indice_a_borrar+cont:]
            index = bitmap.find('0'*fileblocks)
            #print(bitmap)
            a = bitmap[:index] + '1'*fileblocks + bitmap[index+fileblocks:]
            #print(a)
            chunks = [texto[i:i+64] for i in range(0, len(texto), 64)]
            for i,n in enumerate(chunks):
                new_fileblock = FileBlock()
                new_fileblock.b_content = n
                inodo.i_block[i] = primerbloque+i*64
                file.seek(primerbloque+i*64)
                file.write(new_fileblock.pack())
            #rewriteinode
            file.seek(ubicacion_inodo_users)
            file.write(inodo.pack())
            #rewrite bitmap
            file.seek(bitmap_bloques_inicio)
            file.write(a.encode('utf-8'))
            return
        
        
        
def remgroup(params, mounted_partitions,id):
    print("--------------------EJECUTANDO EL REMGROUP------------------")
    if id == None:
        print("Error: The id is required.")
        return
    try: 
        group = params['name']
    except:
        print("Error: El usuario, contraseña y grupo son obligatorios.")
        return
    partition = None
    for partition_dict in mounted_partitions: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break
    if not partition:
        print(f"Error: La partición con id {id} no existe.")
        return
    # Retrieve partition details.
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    current_directory = os.getcwd()
    full_path= f'{filename}'
    if not os.path.exists(full_path):
        print(f"Error: El file {full_path} no existe.")
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        siguiente = folder.b_content[0].b_inodo
        file.seek(siguiente)
        ubicacion_inodo_users = siguiente
        inodo = Inode.unpack(file.read(Inode.SIZE))
        primerbloque = -1
        cont = 0
        texto = ""
        for i,item in enumerate(inodo.i_block[:12]):
            if item != -1 and i == 0:
                primerbloque = item
            if item != -1:
                cont = i+1
                siguiente = item
                file.seek(siguiente)
                fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
                texto += fileblock.b_content.rstrip('\x00')
        indice_a_borrar = (primerbloque- superblock.s_block_start)//64   
        grupos = extract_active_groups(texto)
        group_exists = False  # Initially, we assume the group does not exist
        for n in grupos:
            # Check if the group exists in current item
            if n['groupname'] == group:
                group_exists = True
                break

        if group_exists==False:
            print(f"Error: El grupo {group} no existe.")
            return
        arreglo = texto.split('\n')
        lineas = []
        for i,n in enumerate(arreglo):
            if n == '':
                continue
            linea = n.split(',')
            if linea[1] == 'G' and linea[2] == group:
                linea[0] = '0'
            lineas.append(','.join(linea))
            print(lineas)
        texto = '\n'.join(lineas)
        texto+='\n'
        print(texto)
        #print(texto.split('\n'))
        length = len(texto)
        fileblocks = length//64
        if length%64 != 0:
            fileblocks += 1
        bitmap_bloques_inicio = superblock.s_bm_block_start
        cantidad_bloques = superblock.s_blocks_count
        FORMAT = f'{cantidad_bloques}s'
        SIZE = struct.calcsize(FORMAT)
        file.seek(bitmap_bloques_inicio)
        bitmap_bloques = struct.unpack(FORMAT, file.read(SIZE))
        bitmap=bitmap_bloques[0].decode('utf-8')
        #print(bitmap)
                    
        if fileblocks<=12:
            bitmap = bitmap[:indice_a_borrar] + '0'*cont + bitmap[indice_a_borrar+cont:]
            index = bitmap.find('0'*fileblocks)
            #print(bitmap)
            a = bitmap[:index] + '1'*fileblocks + bitmap[index+fileblocks:]
            #print(a)
            chunks = [texto[i:i+64] for i in range(0, len(texto), 64)]
            for i,n in enumerate(chunks):
                new_fileblock = FileBlock()
                new_fileblock.b_content = n
                inodo.i_block[i] = primerbloque+i*64
                file.seek(primerbloque+i*64)
                file.write(new_fileblock.pack())
            #rewriteinode
            file.seek(ubicacion_inodo_users)
            file.write(inodo.pack())
            #rewrite bitmap
            file.seek(bitmap_bloques_inicio)
            file.write(a.encode('utf-8'))
            return

def remuser(params, mounted_partitions,id):   
    print("--------------------EJECUTANDO EL MAKEUSER------------------")
    #print(params)
    if id == None:
        print("Error: El id es requerido")
        return
    try: 
        user = params['user']
    except:
        print("Error: Es necesario el valor de usuario.")
        return
    partition = None
    for partition_dict in mounted_partitions: # recorrer las particiones montadas
        l=list(partition_dict.values())[0]["id"]
 
        if id == l: # si el id esta en el diccionario
            #obtenemos la particion
            partition = list(partition_dict.values())[0]
            
            break
    if not partition:
        print(f"Error: La particion con id: {id}, no existe.")
        return
    # Retrieve partition details.
    path = partition['path']
    inicio = partition['inicio']
    size = partition['size']
    filename = path
    current_directory = os.getcwd()
    full_path= f'{filename}'
    if not os.path.exists(full_path):
        print(f"Error: El file {full_path} no existe.")
        return
    with open(full_path, "rb+") as file:
        file.seek(inicio)
        superblock = Superblock.unpack(file.read(Superblock.SIZE))
        file.seek(superblock.s_inode_start)
        inodo = Inode.unpack(file.read(Inode.SIZE))
        siguiente = inodo.i_block[0]
        file.seek(siguiente)
        folder = FolderBlock.unpack(file.read(FolderBlock.SIZE))
        siguiente = folder.b_content[0].b_inodo
        file.seek(siguiente)
        ubicacion_inodo_users = siguiente
        inodo = Inode.unpack(file.read(Inode.SIZE))
        primerbloque = -1
        cont = 0
        texto = ""
        for i,item in enumerate(inodo.i_block[:12]):
            if item != -1 and i == 0:
                primerbloque = item
            if item != -1:
                cont = i+1
                siguiente = item
                file.seek(siguiente)
                fileblock = FileBlock.unpack(file.read(FileBlock.SIZE))
                texto += fileblock.b_content.rstrip('\x00')
        indice_a_borrar = (primerbloque- superblock.s_block_start)//64   
        grupos = parse_users(texto)

        group_exists = False  # Initially, we assume the group does not exist
        bandera = False
        for n in grupos:
            if user in n:
                bandera = True
                break
        if bandera == False:
            print(f"Error: El usuario no existe.")
            return
        arreglo = texto.split('\n')
        lineas = []
        for i,n in enumerate(arreglo):
            if n == '':
                continue
            linea = n.split(',')
            if linea[1] == 'U' and linea[3] == user:
                linea[0] = '0'
            lineas.append(','.join(linea))
            #print(lineas)
        texto = '\n'.join(lineas)
        texto+='\n'
        #print(texto)
        #print(texto.split('\n'))
        length = len(texto)
        fileblocks = length//64
        if length%64 != 0:
            fileblocks += 1
        bitmap_bloques_inicio = superblock.s_bm_block_start
        cantidad_bloques = superblock.s_blocks_count
        FORMAT = f'{cantidad_bloques}s'
        SIZE = struct.calcsize(FORMAT)
        file.seek(bitmap_bloques_inicio)
        bitmap_bloques = struct.unpack(FORMAT, file.read(SIZE))
        bitmap=bitmap_bloques[0].decode('utf-8')
        #print(bitmap)
                    
        if fileblocks<=12:
            bitmap = bitmap[:indice_a_borrar] + '0'*cont + bitmap[indice_a_borrar+cont:]
            index = bitmap.find('0'*fileblocks)
            #print(bitmap)
            a = bitmap[:index] + '1'*fileblocks + bitmap[index+fileblocks:]
            #print(a)
            chunks = [texto[i:i+64] for i in range(0, len(texto), 64)]
            for i,n in enumerate(chunks):
                new_fileblock = FileBlock()
                new_fileblock.b_content = n
                inodo.i_block[i] = primerbloque+i*64
                file.seek(primerbloque+i*64)
                file.write(new_fileblock.pack())
            #rewriteinode
            file.seek(ubicacion_inodo_users)
            file.write(inodo.pack())
            #rewrite bitmap
            file.seek(bitmap_bloques_inicio)
            file.write(a.encode('utf-8'))
            #print(a)
            return