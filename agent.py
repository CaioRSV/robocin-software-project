from utils.Point import Point
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Geometry import Geometry


class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, field=None):
        super().__init__(id, yellow)
        self.field = field
        self.steps = 0;
    
        self.nodes = [];
        self.priorityQueue = [];
        self.visitedNodes = [];


    def decision(self):
        if len(self.targets) == 0:
            return
        
        # Chosing closest target to follow at the moment
        targetDistances = [[self.pos.dist_to(self.targets[i]), self.targets[i]] for i in range(len(self.targets))]
        targetDistances.sort(key=(lambda x: x[0]))
        
        chosenPoint = targetDistances[0][1]

        nodes = []

        gap = self.field.rbt_radius  # Gap arbitrário (para testar, 1 é bom de visualizar)

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
                nodes.append(Point(x, y))
                x += gap
            y += gap

        print('-------');
        print(len(nodes));
        # Applying A*

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
