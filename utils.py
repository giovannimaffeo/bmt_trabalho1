# Função para processar o arquivo de configuração e retornar as instruções
def process_config(config_file):
    instructions = {}
    with open(config_file, 'r') as f:
        for row in f:
            key, value = row.strip().split('=')
            if key in instructions:
                # Se a chave já existe, adicionar valores a uma lista
                if isinstance(instructions[key], str):
                    instructions[key] = [instructions[key], value]
                else:
                    instructions[key].append(value)
            else:
                # Se a chave não existe, apenas atribuir o valor diretamente
                instructions[key] = value
    return instructions

