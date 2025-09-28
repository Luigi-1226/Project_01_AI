from searchPlus import Problem

class MundoLagarta(Problem):
    """Estado = (head, frozenset(body), effort)
      - head = (x,y)
      - body = conjunto imutável de células com 'o' + cabeças anteriores
      - effort = inteiro em [0,3]
      Mundo estático na instância: paredes, dimensões, posição da maçã."""
    
    def __init__(self, mundo=grid):
        self.M, self.N, self.walls, self.apple, head, body = self._parse_grid(mundo)
        initialState = (head, frozenset(body), 0)
        super().__init__(initialState)

    def actions(self, state):
        head, body, effort = state
        x, y = head
    
        if not self._head_supported_for_gravity(head, body):
            dest = (x, y - 1)
            if self._in_bounds(dest) and self._is_free_or_apple(dest, body):
                return ['B']
            return []
        
        actions = []
        moves = {'B': (0, -1), 'C': (0, 1), 'D': (1, 0), 'E': (-1, 0)}

        for a, (dx, dy) in moves.items():
            dest = (x + dx, y + dy)

            if not self._in_bounds(dest):
                continue
            if not self._is_free_or_apple(dest, body):
                continue
            if a == 'C' and effort >= 3:
                continue
            if effort > 0 and a in ('E', 'D') and not self._support(dest, body):
                continue

            actions.append(a)

        return sorted(actions)
    
    def result(self, state, action):
        head, body, effort = state
        if action not in ('B', 'C', 'D', 'E'):
            return state 

        dx, dy = {
            'B': (0, -1),
            'C': (0,  1),
            'D': (1,  0),
            'E': (-1, 0),
        }[action]

        new_head = (head[0] + dx, head[1] + dy)
        new_body = set(body)
        new_body.add(head)
        new_body = frozenset(new_body)

        if action == 'C':
            new_effort = min(3, effort + 1)
        else:
            if self._support(new_head, new_body):   
                new_effort = 0
            else:
                new_effort = effort

        return (new_head, new_body, new_effort)
    
    def display(self, state):
        head, body, _ = state
        grid = [['.' for _ in range(self.M)] for _ in range(self.N)]
        for (x, y) in self.walls:
            grid[self.N - 1 - y][x] = '='
        if head != self.apple:
            ax, ay = self.apple
            grid[self.N - 1 - ay][ax] = 'x'
        for (x, y) in body:
            if (x, y) not in self.walls:
                grid[self.N - 1 - y][x] = 'o'
        hx, hy = head
        grid[self.N - 1 - hy][hx] = '@'
        return '\n'.join(' '.join(row) for row in grid) + '\n'

    def goal_test(self, state):
        head, _, _ = state
        return head == self.apple
    
    def executa(self, state, actions_list, verbose=False):
        cost = 0
        for a in actions_list:
            seg = self.result(state, a)
            cost = self.path_cost(cost, state, a, seg)
            state = seg
            obj = self.goal_test(state)
            if verbose:
                print('Ação:', a)
                print(self.display(state), end='')
                print('Custo Total:', cost)
                print('Atingido o objetivo?', obj)
                print()
            if obj:
                break
        return (state, cost, obj)


    # ---------------- auxiliares ----------------
    def _parse_grid(self, grid):
        linhas = [linha.strip() for linha in grid.strip('\n').splitlines()]
        cells = [linha.split() for linha in linhas]

        N = len(cells)
        M = len(cells[0])
        walls = set()
        body = set()
        head = None
        apple = None

        for i, row in enumerate(cells):
            y = N - 1 - i  # (0,0) no canto inferior esquerdo
            for x, s in enumerate(row):
                if s == '=': walls.add((x, y))
                elif s == 'o': body.add((x, y))
                elif s == '@': head = (x, y)
                elif s == 'x': apple = (x, y)

        return M, N, walls, apple, head, body
    
    def _in_bounds(self, cell):
        x, y = cell
        return 0 <= x < self.M and 0 <= y < self.N
    
    def _is_free_or_apple(self, cell, body):
        if cell == self.apple:
            return True
        return (cell not in self.walls) and (cell not in body)
    
    def _support(self, cell, body):
        x, y = cell
        below = (x, y - 1)
        return (below in body) or (below in self.walls)
    
    def _head_supported_for_gravity(self, head, body):
        return self._support(head, body)
