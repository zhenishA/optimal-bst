class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def optimal_bst(keys, freq):
    """
    Optimal Binary Search Tree oluşturur
    
    Args:
        keys: Anahtarlar listesi (sıralı)
        freq: Her anahtarın frekansı
    
    Returns:
        Minimum maliyet ve kök matrisi
    """
    n = len(keys)
    cost = [[0] * n for _ in range(n)]
    root = [[0] * n for _ in range(n)]
    
    # Tek düğümlü ağaçlar
    for i in range(n):
        cost[i][i] = freq[i]
        root[i][i] = i
    
    # Alt ağaç uzunluklarını dene
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            
            # Frekans toplamı
            freq_sum = sum(freq[i:j+1])
            
            # Her düğümü kök olarak dene
            for r in range(i, j + 1):
                left = cost[i][r-1] if r > i else 0
                right = cost[r+1][j] if r < j else 0
                c = left + right + freq_sum
                
                if c < cost[i][j]:
                    cost[i][j] = c
                    root[i][j] = r
    
    return cost[0][n-1], root

def construct_obst(keys, root, i, j):
    """
    Kök matrisinden ağacı oluşturur
    
    Args:
        keys: Anahtarlar listesi
        root: Kök matrisi
        i, j: Alt ağaç aralığı
    
    Returns:
        Ağacın kök düğümü
    """
    if i > j:
        return None
    
    r = root[i][j]
    node = Node(keys[r])
    node.left = construct_obst(keys, root, i, r - 1)
    node.right = construct_obst(keys, root, r + 1, j)
    return node

def inorder(node, depth=0):
    """Ağacı inorder dolaşır ve yazdırır"""
    if node:
        inorder(node.right, depth + 1)
        print('  ' * depth + f'→ {node.key}')
        inorder(node.left, depth + 1)

def calculate_cost(node, freq_dict, depth=1):
    """Ağacın toplam maliyetini hesaplar"""
    if not node:
        return 0
    
    cost = freq_dict.get(node.key, 0) * depth
    cost += calculate_cost(node.left, freq_dict, depth + 1)
    cost += calculate_cost(node.right, freq_dict, depth + 1)
    return cost

# Test
if __name__ == "__main__":
    # Örnek 1
    print("=== Örnek 1 ===")
    keys = [10, 20, 30]
    freq = [1, 1, 10]
    
    min_cost, root_matrix = optimal_bst(keys, freq)
    tree = construct_obst(keys, root_matrix, 0, len(keys) - 1)
    
    print(f"Anahtarlar: {keys}")
    print(f"Frekanslar: {freq}")
    print(f"Minimum maliyet: {min_cost}")
    print("\nOptimal Ağaç:")
    inorder(tree)
    
    # Örnek 2
    print("\n=== Örnek 2 ===")
    keys = ['A', 'B', 'C', 'D']
    freq = [5, 10, 3, 2]
    
    min_cost, root_matrix = optimal_bst(keys, freq)
    tree = construct_obst(keys, root_matrix, 0, len(keys) - 1)
    
    print(f"Anahtarlar: {keys}")
    print(f"Frekanslar: {freq}")
    print(f"Minimum maliyet: {min_cost}")
    print("\nOptimal Ağaç:")
    inorder(tree)
    
    # Maliyet doğrulama
    freq_dict = {keys[i]: freq[i] for i in range(len(keys))}
    actual_cost = calculate_cost(tree, freq_dict)
    print(f"\nDoğrulama - Hesaplanan maliyet: {actual_cost}")
