import sys
from collections import defaultdict, deque

def solve(edges):
   
    g = defaultdict(set)
    for u, v in edges:
        g[u].add(v)
        g[v].add(u)

    gateways = {x for x in g if x.isupper()}
    virus = 'a'
    result = []

    while True:
        # BFS: расстояния от вируса до всех узлов
        dist = {virus: 0}
        q = deque([virus])
        while q:
            node = q.popleft()
            for nei in g[node]:
                if nei not in dist:
                    dist[nei] = dist[node] + 1
                    q.append(nei)

        # Выбор ближайшего шлюза
        reachable = [(dist[g], g) for g in gateways if g in dist]
        if not reachable:
            break
        _, gate = min(reachable)

        # Отключаем коридор шлюз-узел
        disconnect = min(n for n in g[gate] if n.islower())
        result.append(f"{gate}-{disconnect}")
        g[gate].remove(disconnect)
        g[disconnect].remove(gate)

        # Перемещаем вирус на один шаг к выбранному шлюзу
        next_steps = [n for n in g[virus] if dist[n] < dist[gate]]
        if next_steps:
            virus = min(next_steps)

    return result

def main():
    edges = [tuple(line.strip().split('-')) for line in sys.stdin if line.strip()]
    print(*solve(edges), sep='\n')

if __name__ == "__main__":
    main()
