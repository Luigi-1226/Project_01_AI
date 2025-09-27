from searchPlus import Problem

class MundoLagarta(Problem):
    """Estado = (head, frozenset(body), effort)
      - head = (x,y)
      - body = conjunto imutável de células com 'o' + cabeças anteriores
      - effort = inteiro em [0,3]
      Mundo estático na instância: paredes, dimensões, posição da maçã."""
    
    def __init__(self, mundo=grid):
        self.M, self.N, self.walls, self.apple, head, body = self._parse_grid(mundo)
        body = frozenset(body) 
        initialState = (head, body, 0)
        super().__init__(initialState) 

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
            y= N-1-i # coordenada y (0,0) no canto inferior esquerdo

            for x, s in enumerate(row):
                if s == '=': walls.add((x,y))
                elif s == 'o': body.add((x,y))
                elif s == '@': head = (x,y)
                elif s == 'x': apple = (x,y)

        return M, N, walls, apple, head, body
    
    def _in_bounds(self, cell):
        x,y = cell
        return 0 <= x < self.M and 0 <= y < self.N
    
 

    def goal_test(self, state):
        head, _, _ = state
        return head == self.apple
    
