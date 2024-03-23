
def read_params(path_to_file, params_file):
    with open(path_to_file + params_file, 'r') as file:
        # Читаем содержимое файла
        content = file.read()
        
        # Разделяем содержимое файла на строки
        lines = content.split('\n')
        
        # Очищаем строки от лишних символов
        lines = [line.strip() for line in lines if line.strip()]
        
        # Преобразуем строки в элементы списка типа str
        params = list(map(str, lines))
    file.close
    return params