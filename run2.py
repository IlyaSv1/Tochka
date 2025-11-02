import sys
from collections import defaultdict, deque

def solve(edges):
    """
    Решение задачи об изоляции вируса.

    Args:
        edges: список кортежей (узел1, узел2) — все соединения в сети

    Returns:
        Список строк "Шлюз-узел", порядок отключения коридоров
    """
    g = defaultdict(set)
    for u, v in edges:
        g[u].add(v)
        g[v].add(u)

    gateways = {x for x in g if x.isupper()}

    virus, result = 'a', []

    while True:
        # BFS: вычисляем расстояния от вируса до всех доступных узлов
        dist = {virus: 0}
        q = deque([virus])
        while q:
            node = q.popleft()
            for nei in g[node]:
                if nei not in dist:
                    dist[nei] = dist[node] + 1
                    q.append(nei)

        # выбираем ближайший шлюз
        reachable = ((dist[gw], gw) for gw in gateways if gw in dist)
        try:
            _, gate = min(reachable)
        except ValueError:  # если шлюзов больше не осталось
            break

        # выбираем шлюз-узел для отключения
        node = min(u for u in g[gate] if u.islower())
        result.append(f"{gate}-{node}")

        g[gate].remove(node)
        g[node].remove(gate)

        # перемещаем вирус на один шаг к ближайшему шлюзу
        virus = min(n for n in g[virus] if dist[n] < dist[gate])

    return result

def main():
    edges = [tuple(line.strip().split('-')) for line in sys.stdin if line.strip()]

    print(*solve(edges), sep='\n')

if __name__ == "__main__":
    main()
