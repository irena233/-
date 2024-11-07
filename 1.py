import tkinter as tk
import random
from collections import deque
import heapq

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = self.generate_maze()
        self.dfs(0, 0)
        self.check()

    def dfs(self, x, y):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.maze[nx][ny] == 1:
                self.maze[x + dx // 2][y + dy // 2] = 0
                self.maze[nx][ny] = 0
                self.dfs(nx, ny)

    def check(self):
        directions2 = [(0, -1), (-1, 0)]
        x, y = self.rows - 1, self.cols - 1
        self.maze[x][y] = 0
        while (
                x - 1 > 0
                and y - 1 > 0
                and self.maze[x - 1][y] == 1
                and self.maze[x][y - 1] == 1
        ):
            dx, dy = directions2[0]
            x = x + dx
            y = y + dy
            self.maze[x][y] = 0
        with open("map.txt", 'w') as f:
            for row in self.maze:
                f.write(" ".join(map(str, row)) + '\n')

    def generate_maze(self):
        qwe = [[1] * self.cols for _ in range(self.rows)]
        return qwe


class MazeMap:
    def __init__(self, master, maze):
        self.master = master
        self.master.title("Maze")
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()
        self.maze = maze
        self.visited = set()
        self.ans = []
        button=tk.Button(root,text='生成地图',command=lambda: self.draws_maze())
        button.pack()
        button1 = tk.Button(root, text='深度优先', command=lambda: self.walk_agent(self.ans))
        button1.pack()
        button2 = tk.Button(root, text='广度优先', command=lambda: self.walk_agent(self.bfs((0,0))))
        button2.pack()
        button3 = tk.Button(root, text='一致代价', command=lambda: self.walk_agent(self.uniform_cost_search((0,0))))
        button3.pack()
        button4 = tk.Button(root, text='A*', command=lambda: self.walk_agent(self.a_star_search((0,0))))
        button4.pack()
        master.bind("<Key>", self.key_input)

    def key_input(self, event):
        oval_place = self.canvas.bbox(self.agent)
        nx, ny, mx, my = oval_place
        nx, ny = int((nx + 1) / 10), int((ny + 1) / 10)
        if event.keysym == "Up":
            if ny - 1 >= 0 and self.maze.maze[ny - 1][nx] == 0:
                self.canvas.move(self.agent, 0, -10)
        elif event.keysym == "Down":
            if ny + 1 < self.maze.cols and self.maze.maze[ny + 1][nx] == 0:
                self.canvas.move(self.agent, 0, 10)
        elif event.keysym == "Left":
            if nx - 1 >= 0 and self.maze.maze[ny][nx - 1] == 0:
                self.canvas.move(self.agent, -10, 0)
        elif event.keysym == "Right":
            if nx + 1 < self.maze.rows and self.maze.maze[ny][nx + 1] == 0:
                self.canvas.move(self.agent, 10, 0)
        else:
            print("未知按键")

    def draw_maze(self, maze):

        cell_size = 10
        for i in range(maze.rows):
            for j in range(maze.cols):
                color = "black" if maze.maze[i][j] == 1 else "white"
                self.canvas.create_rectangle(
                    j * cell_size,
                    i * cell_size,
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    fill=color,
                )
        self.agent = self.canvas.create_oval(0, 0, 10, 10, fill="red")
        self.dfs((0,0),self.visited,self.ans)

    def draws_maze(self):
        self.maze = Maze(50, 50)
        self.draw_maze(self.maze)

    def dfs(self, position, visited, ans):
        x, y = position
        if (x, y) == (self.maze.rows - 1, self.maze.cols - 1):
            return 0
        if not (0 <= x < self.maze.rows and 0 <= y < self.maze.cols) or (x, y) in visited or self.maze.maze[x][y] == 1:
            return 1
        visited.add((x, y))

        # 向下移动
        if x + 1 < self.maze.rows and self.maze.maze[x + 1][y] == 0 and (x + 1, y) not in visited:
            ans.append(1)
            if  not self.dfs((x + 1, y), visited, ans):
                return 0
            ans.append(4)
        # 向上移动
        if x - 1 >= 0 and self.maze.maze[x - 1][y] == 0 and (x - 1, y) not in visited:
            ans.append(4)
            if not self.dfs((x - 1, y), visited, ans):
                return 0
            ans.append(1)
        # 向右移动
        if y + 1 < self.maze.cols and self.maze.maze[x][y + 1] == 0 and (x, y + 1) not in visited:
            ans.append(2)
            if not  self.dfs((x, y + 1), visited, ans):
                return 0
            ans.append(3)
        # 向左移动
        if y - 1 >= 0 and self.maze.maze[x][y - 1] == 0 and (x, y - 1) not in visited:
            ans.append(3)
            if  not self.dfs((x, y - 1), visited, ans):
                return 0
            ans.append(2)
        return 1

    def bfs(self, start):
        queue = deque([(start, [])])  # 队列保存位置和路径
        visited = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 下、上、右、左
        moves = [1, 4, 2, 3]  # 分别代表向下、向上、向右、向左的移动

        while queue:
            (x, y), path = queue.popleft()

            # 如果达到终点，返回路径
            if (x, y) == (self.maze.rows - 1, self.maze.cols - 1):
                return path

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # 尝试每个方向
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols and self.maze.maze[nx][ny] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [moves[i]]))

        return []  # 未找到路径时返回空路径

    def uniform_cost_search(self, start):
        # 方向对应: 下、上、右、左
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = [1, 4, 2, 3]  # 分别代表向下、向上、向右、向左的移动

        # 优先队列初始化，存储 (成本, (x, y), 路径)
        queue = [(0, start, [])]
        visited = set()

        while queue:
            cost, (x, y), path = heapq.heappop(queue)  # 获取当前成本最小的节点

            # 如果已经到达目标，返回路径
            if (x, y) == (self.maze.rows - 1, self.maze.cols - 1):
                return path

            # 如果已经访问过这个节点，跳过
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # 尝试四个方向
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols and self.maze.maze[nx][ny] == 0 and (
                nx, ny) not in visited:
                    # 向队列添加新的节点，成本加1
                    new_cost = cost + 1
                    heapq.heappush(queue, (new_cost, (nx, ny), path + [moves[i]]))

        return []  # 未找到路径时返回空路径

    def greedy_best_first_search(self, start):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = [1, 4, 2, 3]  # 分别代表向下、向上、向右、向左的移动

        # 优先队列初始化，存储 (估计距离, (x, y), 路径)
        queue = [(self.heuristic(start), start, [])]
        visited = set()

        while queue:
            _, (x, y), path = heapq.heappop(queue)  # 选择启发式估计值最小的节点

            # 如果到达目标，返回路径
            if (x, y) == (self.maze.rows - 1, self.maze.cols - 1):
                return path

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # 尝试四个方向
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols and self.maze.maze[nx][ny] == 0 and (
                nx, ny) not in visited:
                    # 向队列添加新节点
                    heapq.heappush(queue, (self.heuristic((nx, ny)), (nx, ny), path + [moves[i]]))

        return []  # 未找到路径时返回空路径
    #启发函数
    def heuristic(self, position):
        # 启发式函数：曼哈顿距离
        x, y = position
        goal_x, goal_y = self.maze.rows - 1, self.maze.cols - 1
        return abs(x - goal_x) + abs(y - goal_y)

    def a_star_search(self, start):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = [1, 4, 2, 3]  # 分别代表向下、向上、向右、向左的移动

        # 优先队列初始化，存储 (f(n), (x, y), path)
        queue = [(self.heuristic(start), 0, start, [])]
        visited = set()

        while queue:
            _, cost, (x, y), path = heapq.heappop(queue)  # 选择f(n)最小的节点

            # 如果到达目标，返回路径
            if (x, y) == (self.maze.rows - 1, self.maze.cols - 1):
                return path

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # 尝试四个方向
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.rows and 0 <= ny < self.maze.cols and self.maze.maze[nx][ny] == 0 and (
                nx, ny) not in visited:
                    new_cost = cost + 1
                    f = new_cost + self.heuristic((nx, ny))  # f(n) = g(n) + h(n)
                    heapq.heappush(queue, (f, new_cost, (nx, ny), path + [moves[i]]))

        return []  # 未找到路径时返回空路径


    def walk_agents(self, ans):
        if not ans:
            return
        lis = ans.pop(0)
        x1, y1, x2, y2 = self.canvas.coords(self.agent)

        # 标记当前路径为红色
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue3", outline="red")

        if lis == 1:    # 向下
            self.canvas.move(self.agent, 0, 10)
        elif lis == 2:  # 向右
            self.canvas.move(self.agent, 10, 0)
        elif lis == 3:  # 向左
            self.canvas.move(self.agent, -10, 0)
        elif lis == 4:  # 向上
            self.canvas.move(self.agent, 0, -10)

        # 延迟后递归调用
        self.master.after(50, lambda: self.walk_agents(ans))


    def walk_agent(self,ans):
        self.canvas.coords(self.agent, 0, 0, 0 + 10, 0 + 10)
        self.draw_maze(self.maze)
        self.walk_agents(ans)
if __name__ == "__main__":
    root = tk.Tk()
    maze = Maze(20, 20)
    MazeMap(root, maze)
    root.mainloop()
