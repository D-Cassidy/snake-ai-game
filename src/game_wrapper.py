import utils

class SnakeGameWrapper:
    def __init__(self, game):
        self.game = game

    def reset(self):
        """Resets the game and returns the initial state"""
        self.game.reset()
        return self.get_state()
    
    def get_state(self):
        """Retruns the current game state"""
        snake_head = self.game.snake.body[0]
        # snake_body = self.game.snake.body[1:]
        food_position = self.game.food.position
        state = (snake_head, food_position)
        return state
    
    def take_action(self, action):
        """Applies chosen action to the game and returns next_state and reward"""
        # Apply action
        if action == 'up':
            self.game.snake.change_direction(utils.UP)
        elif action == 'down':
            self.game.snake.change_direction(utils.DOWN)
        elif action == 'left':
            self.game.snake.change_direction(utils.LEFT)
        elif action == 'right':
            self.game.snake.change_direction(utils.RIGHT)

        old_dist = utils.manhattan_distance(self.game.snake.body[0], self.game.food.position)
        old_score = self.game.score
        self.game.update()
        next_state = self.get_state()

        # Define reward
        reward = 0          # default penalty to encourage efficiency
        if self.game.score > old_score:
            reward = 50     # positive reward for food 
        elif self.game.game_over:
            reward = -100    # negative reward for losing
        else:               # reward for getting closer to food
            new_dist = utils.manhattan_distance(self.game.snake.body[0], self.game.food.position)
            if new_dist < old_dist:
                reward += 2
            elif new_dist > old_dist:
                reward -= 1

        done = self.game.game_over
        return next_state, reward, done