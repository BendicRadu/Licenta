class GameOverException(Exception):
    pass

class PlayerStarvedException(GameOverException):
    pass

class PlayerQuitException(GameOverException):
    pass
