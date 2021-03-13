# Chess 

Chess game with AI ( implemented with minimax, with alpha-beta pruning ). This article helped me in creating the AI.  
[https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/](https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/)

For understanding minimax and alpha beta pruning this video was helpful for me.   
[Minimax & Alpha-beta pruning](https://youtu.be/l-hh51ncgDI)

The user could play either online by connecting to the server or with the AI.

To play the game, pygame is needed so install it, if you don't have it.
```
    $ pip install pygame
```
Then simply run game.py.
```
    $ python3 game.py
```

![](assets/g.gif)

## To play the game online.
For Online mode you will have to change some code in "client.py"

1) You have to host "server.py" on some server.
2) Change **self.host** in client.py to the public IP of your server.
3) Open two instances of the game, from anywhere and play.


## Known Issues

* Stalemate
* Castling
* Pawn Promotion
* En Passant

## Dependencies

* [Pygame](https://www.pygame.org/docs/)