import sys
from collections import defaultdict, deque

def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса.
    
    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    # Строим граф
    g = defaultdict(set)
    for u, v in edges:
        g[u].add(v)
        g[v].add(u)

    # Шлюзы
    gateways = {x for x in g if x.isupper()}
    virus = 'a'
    result = []

    while True:
        # BFS: расстояния от текущей позиции вируса до всех узлов
        dist = {virus: 0}
        q = deque([virus])
        while q:
            node = q.popleft()
            for nei in g[node]:
                if nei not in dist:
                    dist[nei] = dist[node] + 1
                    q.append(nei)

        # Выбираем ближайший шлюз
        reachable = [(dist[g], g) for g in gateways if g in dist]
        if not reachable:
            break
        _, gate = min(reachable)

        # Выбираем коридор шлюз-узел для отключения
        disconnect = min(n for n in g[gate] if n.islower())
        result.append(f"{gate}-{disconnect}")

        # Удаляем коридор из графа
        g[gate].remove(disconnect)
        g[disconnect].remove(gate)

        # Перемещаем вирус на один шаг к выбранному шлюзу
        next_steps = sorted(n for n in g[virus] if dist[n] < dist[gate])
        if next_steps:
            virus = next_steps[0]

    return result

def main():
    edges = [tuple(line.strip().split('-')) for line in sys.stdin if line.strip()]
    print(*solve(edges), sep='\n')

if __name__ == "__main__":
    main()
