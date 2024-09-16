import hashlib

class DHTNode:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.id = self.generate_id(ip, port)
        self.predecessor = None
        self.successor = self  # Inicialmente o nó aponta para si mesmo

    def generate_id(self, ip, port):
        """Gera o identificador hash baseado no IP e na porta"""
        node_info = f"{ip}:{port}"
        return int(hashlib.sha1(node_info.encode()).hexdigest(), 16) % (2 ** 32)  # 160 bits

    def set_successor(self, node):
        self.successor = node

    def set_predecessor(self, node):
        self.predecessor = node

    def __repr__(self):
        return f"Nó({self.id}, {self.ip}:{self.port})"

    def join(self, known_nodes):
        """Tenta se juntar à rede de DHT. Se não encontrar outros nós conhecidos, cria uma nova rede."""
        if not known_nodes:
            # Se não houver nós conhecidos, o nó se torna o primeiro nó da rede
            print(f"{self} é o primeiro nó da rede.")
            self.set_successor(self)
            self.set_predecessor(self)
        else:
            # Conecte-se a um nó conhecido e envie uma mensagem JOIN
            for node in known_nodes:
                print(f"{self} tenta conectar-se ao nó {node}")
                node.handle_join(self)
                break


    def handle_join(self, new_node):
        """Recebe uma mensagem JOIN de um nó novo e processa sua entrada."""
        # Caso especial: a rede tem apenas um nó
        if self.successor == self and self.predecessor == self:
            # O novo nó se torna o sucessor e predecessor do nó atual
            new_node.set_successor(self)
            new_node.set_predecessor(self)
            self.set_successor(new_node)
            self.set_predecessor(new_node)
            print(f"{new_node} conectou-se à rede. Agora {self} é o predecessor e sucessor de {new_node}.")
        
        else:
            # Verificar se o nó atual é o menor nó
            is_smallest_node = self.predecessor.id > self.id
            
            # Verificar se o nó atual é o maior nó
            is_largest_node = self.successor.id < self.id

            # Caso 1: o novo nó tem o menor ID de todos
            if new_node.id < self.id and is_smallest_node and self.id < self.successor.id:
                # O novo nó se conecta antes do menor nó
                new_node.set_successor(self)
                new_node.set_predecessor(self.predecessor)
                self.predecessor.set_successor(new_node)
                self.set_predecessor(new_node)
                print(f"{new_node} conectou-se como o menor nó da rede. Entre {new_node.predecessor} e {self}.")
                return

            # Caso 2: o novo nó tem o maior ID de todos
            elif new_node.id > self.id and is_largest_node and self.id > self.predecessor.id:
                # O novo nó se conecta após o maior nó
                new_node.set_predecessor(self)
                new_node.set_successor(self.successor)
                self.successor.set_predecessor(new_node)
                self.set_successor(new_node)
                print(f"{new_node} conectou-se como o maior nó da rede. Entre {self} e {new_node.successor}.")
                return
            
            # Caso geral: o novo nó se conecta entre dois nós existentes
            elif new_node.id > self.predecessor.id and new_node.id < self.id:
                # O novo nó se conecta entre o predecessor e o nó atual (self)
                
                # 1. Atualiza o sucessor e o predecessor do novo nó
                new_node.set_successor(self)  # O sucessor do novo nó é o nó atual (self)
                new_node.set_predecessor(self.predecessor)  # O predecessor do novo nó é o predecessor do nó atual
                
                # 2. Atualiza o sucessor do predecessor para apontar para o novo nó
                self.predecessor.set_successor(new_node)
                
                # 3. Atualiza o predecessor do nó atual (self) para apontar para o novo nó
                self.set_predecessor(new_node)
                
                # Mensagem de sucesso para depuração
                print(f"{new_node} conectou-se entre {new_node.predecessor} e {new_node.successor}.")

            
            else:
                # Se o novo nó não se encaixa neste nó, encaminha para o sucessor
                print(f"{self} encaminha JOIN para o sucessor {self.successor}.")
                self.successor.handle_join(new_node)



    def leave(self):
        """Remove o nó da rede e ajusta os ponteiros de predecessor e sucessor."""
        if self.predecessor and self.successor:
            print(f"{self} está saindo da rede.")
            self.predecessor.set_successor(self.successor)
            self.successor.set_predecessor(self.predecessor)
            print(f"O predecessor de {self.successor} agora é {self.predecessor}.")
            print(f"O sucessor de {self.predecessor} agora é {self.successor}.")
        else:
            print(f"{self} não pode sair da rede, pois não está conectado.")

    def handle_node_gone(self, gone_node):
        """Trata a saída de um nó da rede."""
        if gone_node == self.successor:
            print(f"{gone_node} saiu, atualizando sucessor para {gone_node.successor}.")
            self.set_successor(gone_node.successor)
        elif gone_node == self.predecessor:
            print(f"{gone_node} saiu, atualizando predecessor para {gone_node.predecessor}.")
            self.set_predecessor(gone_node.predecessor)

