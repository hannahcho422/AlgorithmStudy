from collections import deque


# 입력
n, r, c, direction = map(int, input().split())

# 1번부터 시작하는 좌표를 그대로 사용하기 위해 가장자리에 1을 추가
board = [[1] * (n + 1)]

for _ in range(n):
    board.append([1] + list(map(int, input().split())))


# 방향 번호
# 1: 상, 2: 하, 3: 좌, 4: 우
dr = [0, -1, 1, 0, 0]
dc = [0, 0, 0, -1, 1]


# 현재 방향별 인접 탐험 우선순위
# 직진 → 좌회전 → 우회전 → 180도 회전
adjacent_order = [
    [],
    [1, 3, 4, 2],  # 상
    [2, 4, 3, 1],  # 하
    [3, 2, 1, 4],  # 좌
    [4, 1, 2, 3]   # 우
]


# 2단계에서 최단 경로를 선택하는 방향 우선순위
# 좌 → 하 → 우 → 상
path_order = [3, 2, 4, 1]


# 좌표 변화량을 방향 번호로 변환
direction_of = {
    (-1, 0): 1,
    (1, 0): 2,
    (0, -1): 3,
    (0, 1): 4
}


# 고래가 실제로 방문한 칸
visited = [[False] * (n + 1) for _ in range(n + 1)]


# 전체 바다 칸의 개수
total_sea = 0

for row in range(1, n + 1):
    for col in range(1, n + 1):
        if board[row][col] == 0:
            total_sea += 1


# 시작 위치 처리
visited[r][c] = True
visited_count = 1

answer = [(r, c)]


def find_nearest_path(start_r, start_c):
    """
    현재 위치에서 가장 가까운 미방문 바다까지의 경로를 반환한다.

    1. BFS를 레벨 단위로 진행해 가장 가까운 미방문 바다를 찾는다.
    2. 같은 거리 후보 중 행과 열이 가장 작은 칸을 선택한다.
    3. parent 배열을 이용해 선택한 칸까지의 경로를 복원한다.
    """

    queue = deque([(start_r, start_c)])

    # BFS 중복 방문 방지용 배열
    seen = [[False] * (n + 1) for _ in range(n + 1)]

    # 경로 복원용 배열
    parent = [[None] * (n + 1) for _ in range(n + 1)]

    seen[start_r][start_c] = True

    target = None

    while queue:
        # 현재 거리의 모든 칸을 저장
        current_layer = []

        for _ in range(len(queue)):
            current_layer.append(queue.popleft())

        # 현재 거리에서 아직 실제로 방문하지 않은 바다 찾기
        candidates = []

        for current_r, current_c in current_layer:
            if not visited[current_r][current_c]:
                candidates.append((current_r, current_c))

        # 같은 거리의 후보가 존재한다면
        if candidates:
            # 행이 작은 칸, 열이 작은 칸 선택
            target = min(candidates)
            break

        # 현재 거리에서 후보가 없다면 다음 거리 탐색
        for current_r, current_c in current_layer:
            # 좌 → 하 → 우 → 상 순으로 탐색
            for next_direction in path_order:
                next_r = current_r + dr[next_direction]
                next_c = current_c + dc[next_direction]

                if not (1 <= next_r <= n and 1 <= next_c <= n):
                    continue

                if board[next_r][next_c] == 1:
                    continue

                if seen[next_r][next_c]:
                    continue

                seen[next_r][next_c] = True
                parent[next_r][next_c] = (current_r, current_c)

                queue.append((next_r, next_c))

    # 목표 지점에서 시작 지점까지 역추적
    target_r, target_c = target
    path = []

    while (target_r, target_c) != (start_r, start_c):
        path.append((target_r, target_c))
        target_r, target_c = parent[target_r][target_c]

    # 시작점 → 목표점 순서로 변경
    path.reverse()

    return path


while visited_count < total_sea:
    moved = False

    # 1단계: 인접 탐험
    for next_direction in adjacent_order[direction]:
        next_r = r + dr[next_direction]
        next_c = c + dc[next_direction]

        if not (1 <= next_r <= n and 1 <= next_c <= n):
            continue

        if board[next_r][next_c] == 1:
            continue

        if visited[next_r][next_c]:
            continue

        # 이동
        r = next_r
        c = next_c
        direction = next_direction

        visited[r][c] = True
        visited_count += 1
        answer.append((r, c))

        moved = True
        break

    # 인접 미방문 칸으로 이동했다면 다시 1단계 진행
    if moved:
        continue

    # 2단계: 가장 가까운 미방문 바다까지 이동
    path = find_nearest_path(r, c)

    for next_r, next_c in path:
        # 실제 이동 방향 계산
        row_difference = next_r - r
        col_difference = next_c - c

        direction = direction_of[(row_difference, col_difference)]

        r = next_r
        c = next_c

        # 처음 방문한 칸만 정답에 추가
        if not visited[r][c]:
            visited[r][c] = True
            visited_count += 1
            answer.append((r, c))


# 출력
print("\n".join(
    str(row) + " " + str(col)
    for row, col in answer
))