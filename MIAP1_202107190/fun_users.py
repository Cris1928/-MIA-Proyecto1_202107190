def cargar_usuarios(content):
   #Carga de usuarios y grupos desde el contenido de una cadena en una estructura de diccionario.
    lines = content.split("\n") #separa por salto de linea
    

    data_structure = {} #se crea un diccionario vacio
    for line in lines: #se recorre cada linea
        if line == '': #si la linea esta vacia se salta
            continue #se salta
        parts = line.strip().split(",") #se separa por comas
        if parts[1] == 'G':  # Group
            if parts[0] != '0': #si el id es diferente de 0
                data_structure[parts[2]] = {} #se crea un diccionario vacio
        else:  # Ususuario
            if parts[0] != '0': #si el id es diferente de 0
                group_name = parts[2] #se guarda el nombre del grupo
                user_data = { #se crea un diccionario con los datos del usuario
                    'id': parts[0],
                    'username': parts[3],
                    'password': parts[4]
                }
                if group_name in data_structure: #si el nombre del grupo esta en el diccionario
                    data_structure[group_name][parts[3]] = user_data #se agrega el usuario al grupo
                else:
                    data_structure[group_name] = {parts[3]: user_data} #se crea el grupo y se agrega el usuario
 
    return data_structure
def parse_users(texto): #se crea una funcion para parsear los usuarios
    lines = texto.split('\n') #se separa por salto de linea

    users_list = [] #se crea una lista vacia
    
    # Almacenamiento temporal para grupos
    groups = {} #se crea un diccionario vacio
    grupo_actual = '' #se crea una variable vacia
    for line in lines: #se recorre cada linea
        parts = line.split(',') #se separa por comas
        
        # Group
        if len(parts) == 3 and parts[1] == 'G'and parts[0]!='0': #si la longitud de la linea es igual a 3 y el id es diferente de 0
            groups[parts[2]] = parts[0] #se agrega el grupo al diccionario
            grupo_actual = parts[2] #se guarda el nombre del grupo
        
        # User
        elif len(parts) == 5 and parts[1] == 'U' and parts[0]!='0': #si la longitud de la linea es igual a 5 y el id es diferente de 0
            if grupo_actual == parts[2]: #si el grupo actual es igual al grupo de la linea
                user_data = { #se crea un diccionario con los datos del usuario
                    parts[3]: {
                        'id': parts[0],
                        'username': parts[3],
                        'password': parts[4],
                        'group': parts[2]
                    }
                }
                users_list.append(user_data)
            
    return users_list


def auten_usuarios(usuarios, user, password): #se crea una funcion para obtener el usuario si esta autenticado
    print(f'buscando a {user} con password {password} en {usuarios}') #se imprime en consola
    for user_data in usuarios: #se recorre cada usuario
        if user in user_data: #si el usuario esta en el diccionario
            # Usuario encontrado
            if user_data[user]['password'] == password:
                # contraseña correcta
                return user_data[user]
    # Usuario no encontrado o la contraseña no coincide
    return None

def get_id_by_group(grupos, group): #se crea una funcion para obtener el id por grupo
    for item in grupos: #se recorre cada grupo
        user_data = item[next(iter(item))] #se guarda el primer elemento del grupo
        if user_data['group'] == group: #si el grupo es igual al grupo de la linea
            return user_data['id'] #se retorna el id
    return None  # If the group was not found


def extract_active_groups(text): #se crea una funcion para extraer los grupos activos
    lines = text.split("\n") #se separa por salto de linea
    groups = [] #se crea una lista vacia
    print(lines) #se imprime en consola
    for line in lines: #se recorre cada linea
        if line == '': #si la linea esta vacia se salta
            continue #se salta
        parts = line.split(",") #se separa por comas
        # verificar si es un grupo
        if parts[1] == 'G' and parts[0] != '0': #si el id es diferente de 0
            groups.append({'groupname': parts[2], 'id': int(parts[0])}) #se agrega el grupo a la lista

    return groups
def get_group_id(group_name, groups): #se crea una funcion para obtener el id del grupo
    for group in groups: #se recorre cada grupo
        if group['groupname'] == group_name: #si el nombre del grupo es igual al nombre del grupo de la linea
            return group['id'] #se retorna el id
    return None
