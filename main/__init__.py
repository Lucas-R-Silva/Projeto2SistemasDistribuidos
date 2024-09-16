from DHTNode import DHTNode

# Criar nós na rede
node1 = DHTNode("127.0.0.1", 5000)
node2 = DHTNode("127.0.0.1", 5001)
node3 = DHTNode("127.0.0.1", 5002)
#node4 = DHTNode("127.0.0.1", 5003)
#node5 = DHTNode("127.0.0.1", 5004)

# O nó 1 cria a rede
node1.join([])

# Nó 2 e Nó 3 tentam se conectar
node2.join([node1])
node3.join([node1])
#node4.join([node1])
#node5.join([node1])

# Verificar a estrutura da rede
print(f"Nó 1: {node1.predecessor}, {node1}, {node1.successor}")
print(f"Nó 2: {node2.predecessor}, {node2}, {node2.successor}")
print(f"Nó 3: {node3.predecessor}, {node3}, {node3.successor}")
#print(f"Nó 4: {node4.predecessor}, {node4}, {node4.successor}")
#print(f"Nó 5: {node5.predecessor}, {node5}, {node5.successor}")

# Nó 2 sai da rede
node2.leave()

# Verificar a estrutura após a saída
print(f"Nó 1: {node1.predecessor}, {node1}, {node1.successor}")
print(f"Nó 3: {node3.predecessor}, {node3}, {node3.successor}")
