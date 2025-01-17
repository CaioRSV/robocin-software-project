from utils.Point import Point
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Geometry import Geometry


class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, field=None):
        super().__init__(id, yellow)
        self.field = field
        self.steps = 0;
    
        self.nodes = []; # [Point, f(n), ParentNode]
        self.priorityQueue = [[Point(99,99), 100, None]];
        self.visitedNodes = [];


    def decision(self):
        if len(self.targets) == 0:
            return 
        
        # Chosing closest target to follow at the moment
        targetDistances = [[self.pos.dist_to(self.targets[i]), self.targets[i]] for i in range(len(self.targets))]
        targetDistances.sort(key=(lambda x: x[0]))
        
        chosenPoint = Point(targetDistances[0][1].x, targetDistances[0][1].y)

        self.nodes = [] # Point, f(n), Parent

        gap =  self.field.rbt_radius or 0.05  # Gap arbitrário (para testar, 1 é bom de visualizar)

        height = self.field.length  # For example, 4.0
        width = self.field.width    # For example, 6.0

        # Bordas
        min_y = -height / 2
        max_y = height / 2
        min_x = -width / 2
        max_x = width / 2

        y = min_y
        while y <= max_y:
            x = min_x
            while x <= max_x:
                self.nodes.append(Point(x, y))
                x += gap
            y += gap

        print('-------');
        #print(len(self.nodes));


        # Applying A*

        # Determinando node POSITION 
        planePos = Point(0,0) # Pronto mais próximo aproximado no plano de onde o self.pos está
        curDist = width

        for x in self.nodes:
            if (x.dist_to(self.pos) < curDist):
                curDist = x.dist_to(self.pos)
                planePos = x

        # Determinando node TARGET
        targetPos = Point(0,0)
        curDist = width

        for y in self.nodes:
            if (y.dist_to(chosenPoint) < curDist):
                curDist = y.dist_to(chosenPoint)
                targetPos = y
        
        currentNode = [planePos, 0, None]
        targetNode = [targetPos, 0, None] 

        self.priorityQueue.append(currentNode) # Point, f(0), Parent

        print(f"Pos: {planePos} | Target: {targetPos}")

        def RecursiveStep(currentNode, targetNode):
            if(len(self.priorityQueue) == 0): 
                print('PRIORITY QUEUE VAZIA')
                return
            
            neighbourMatrix = [
                [0, gap], # Right
                [gap, 0], # Top 
                [0, -gap], # Left
                [0, -gap], # Bottom
                [gap, gap], # Top-Right
                [-gap, -gap], # Left-Bottom
                [-gap, gap], # Left-Top
                [gap, -gap], # Right-Bottom
            ]
            
            neighbourPoints = list(map(lambda item: [Point(currentNode[0].x + item[0], currentNode[0].y + item[1])], neighbourMatrix))

            # print(f"Nodes: {len(self.nodes)} | Gap: {gap}")
            # print(f"Posição no plano de nodes: {currentNode[0]}")
                    
            # Popping currentNode from the Priority Queue
            self.priorityQueue = [i for i in self.priorityQueue if i!=currentNode]

            # Visited Nodes Handling
            newVisitedNodes = []

            for i in self.visitedNodes: # Substitutes if less f(n) and if is already there
                if(currentNode[0] == i[0] and currentNode[1] < i[1]):
                    newVisitedNodes.append(currentNode)
                else:
                    newVisitedNodes.append(i)

            if (currentNode not in newVisitedNodes): # Adds if not in the visited nodes yet
                newVisitedNodes.append(currentNode)

            self.visitedNodes = newVisitedNodes

            # Adding all neighbours to the priorityQueue
            neighbourNodes = []
            for i in neighbourPoints:
                for n in self.nodes:
                    if (i[0].x == n.x and i[0].y == n.y):
                        curPoint = Point(n.x, n.y)
                        neighbourNodes.append([curPoint, curPoint.dist_to(targetNode[0]), currentNode])
            
            for i in neighbourNodes:
                self.priorityQueue.append(i)

            # Choosing next node based on less f(n)
            nextNode = min(self.priorityQueue, key= lambda x: x[1])

            # Target checking
            if(nextNode[0] == targetNode[0]):
                self.visitedNodes.append(nextNode)
                return nextNode
            else:
                RecursiveStep(nextNode, targetNode)

        if (self.steps < 1) :
            print(len(self.priorityQueue))
            print(RecursiveStep(currentNode, targetNode))
            print('---')
        # if(self.steps < 25):
        #     self.steps += 1
        # else:
        #     print(self.steps)
        #     self.steps = 0        

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, chosenPoint)
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
