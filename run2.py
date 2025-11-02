import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    gateways = sorted([n for n in graph if n.isupper()])
    virus_pos = "a"
    result = []

    def bfs(start):
        dist = {start: 0}
        prev = {start: None}
        q = deque([start])
        while q:
            cur = q.popleft()
            for nei in sorted(graph[cur]):
                if nei not in dist:
                    dist[nei] = dist[cur] + 1
                    prev[nei] = cur
                    q.append(nei)
        return dist, prev

    while True:
        dist, prev = bfs(virus_pos)
        reachable = [(dist[g], g) for g in gateways if g in dist]
        if not reachable:
            break

        reachable.sort()
        min_d = reachable[0][0]
        candidate_gateways = [g for d, g in reachable if d == min_d]
        target_gateway = min(candidate_gateways)

        # если вирус соседствует со шлюзом — отрубаем
        for g in gateways:
            if g in graph[virus_pos]:
                result.append(f"{g}-{virus_pos}")
                graph[g].discard(virus_pos)
                graph[virus_pos].discard(g)
                break
        else:
            # выбираем первый возможный разрыв шлюз-узел
            candidates = []
            for g in gateways:
                for n in sorted(graph[g]):
                    if n.islower():
                        candidates.append((g, n))
            candidates.sort()

            for g, n in candidates:
                graph[g].discard(n)
                graph[n].discard(g)
                new_dist, _ = bfs(virus_pos)
                if not any(gw in new_dist and new_dist[gw] == 1 for gw in gateways):
                    result.append(f"{g}-{n}")
                    break
                else:
                    graph[g].add(n)
                    graph[n].add(g)

        # обновляем позицию вируса
        dist, prev = bfs(virus_pos)
        reachable = [(dist[g], g) for g in gateways if g in dist]
        if reachable:
            reachable.sort()
            _, tg = reachable[0]
            path = []
            cur = tg
            while cur != virus_pos:
                path.append(cur)
                cur = prev[cur]
            path.reverse()
            virus_pos = path[0] if path else virus_pos
        else:
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            a, _, b = line.partition('-')
            edges.append((a, b))
    for edge in solve(edges):
        print(edge)


if __name__ == "__main__":
    main()
