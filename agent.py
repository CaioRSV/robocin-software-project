from utils.Point import Point
from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Geometry import Geometry


class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False, rbtRadius=None):
        super().__init__(id, yellow)
        self.rbtRadius = rbtRadius

    def decision(self):
        if len(self.targets) == 0:
            return
        
        # for i in self.opponents:
        #     if(i==1):
        #         print(self.opponents[i])
        #         print("")
        #         print('--')
    
        # for i in self.teammates:
        #     if(self.teammates[i].id != self.id):
        #         print(self.teammates[i])
        #         print(self.id)
        #         print("")
        #         print('--')

        # list = []

        # for i in range(self.targets):
        #     res = Navigation.goToPoint(self.robot, self.targets[i])
        #     list.append(res)

        # print(list)

        # Chosing closest target to follow at the moment
        targetDistances = [[self.pos.dist_to(self.targets[i]), self.targets[i]] for i in range(len(self.targets))]
        targetDistances.sort(key=(lambda x: x[0]))
        
        chosenPoint = targetDistances[0][1]

        # Finding the best path (But with same costs for each step in directions)

        d = self.rbtRadius * 5 # stepSize

        # Different possible directions [X,Y]
        directions = [
            [0, d], # ↑
            [d, d], # ↗
            [d, 0], # →
            [d, -d], # ↘
            [0, -d], # ↓
            [-d, -d], # ↙
            [-d, 0], # ←
            [-d, d], # ↑
        ]
        
        # Possible new destinations
        pointStepPositions = list(map(lambda item: Point(item[0]+chosenPoint[0], item[1]+chosenPoint[1]), directions))

        # Sort by distance to the chosenTarget
        pointStepPositions.sort(key=(
            lambda item: item.dist_to(chosenPoint)
        ))

        # print('-----------')
        # print(self.pos)
        # print(chosenPoint)

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, pointStepPositions[0])
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
