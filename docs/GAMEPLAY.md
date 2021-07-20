# Game Mechanics

So you've read through the documentation, setting up every bit and are yearning to head into a game? Not so fast! You have to set up the game's difficulty.

![Cell size prompt](https://media.discordapp.net/attachments/862971677440737340/867071991915479040/unknown.png)

The first prompt is going to be regarding the cell size, this is how big each cell is displayed. This won't affect game difficulty however this does matter depending on how large or small your terminal is set to, the recommended value is `2`.

![Grid width prompt](https://media.discordapp.net/attachments/862971677440737340/867072624630169610/unknown.png)

The game should now prompt you regarding grid width, the larger the value, the larger the grid will be, hence this affects the difficulty of your game. The recommended value is `5`.

![Grid height prompt](https://media.discordapp.net/attachments/862971677440737340/867073449624600656/unknown.png)

This setting is similar to the last one, the recommended value is again `5`.

_Note: As mentioned in the [main page](https://github.com/SystematicError/code-jam/tree/master/README.md) there is a bug that causes an exception when entering a value below `3`_

![Recursive cell prompt](https://media.discordapp.net/attachments/862971677440737340/867073832078409788/unknown.png)

Now for the juicy part, recursive cells. These greatly affect the difficulty of the game and is what truly makes Boxed enjoyable. The mechanics of this special cell is mentioned later on in this page. The recommended value for this is `3`

Now that you have entered all the given configs, time to head into the actual game!

![Boxed depth 0](https://media.discordapp.net/attachments/862971677440737340/867074652413493308/unknown.png)

Here you can see lots of small boxes, these are called `Cells`. There are 3 types of cells: `Start / End`, `Standard` and `Recursive`. These are represented with the following colors:

**Start / End** - Red

**Standard** - White

**Recursive** - Orange / Yellow


You may also notice small openings on the sides of these, the aim of the game is to build a smooth flowing chain of openings from one of the red cell to the other one. These red cells cannot be twisted.

![Cell selection](https://media.discordapp.net/attachments/862971677440737340/867075877723963402/unknown.png)

Speaking of twistable cells you may have noticed that some cells have a thick bold highlight over them, this represents your current selection. If you were to press `Space` you would twist this current cell. The white cells or standard cells can be twisted like this.

![Unconnected cell](https://media.discordapp.net/attachments/862971677440737340/867076934809944124/unknown.png)

_This is what 2 unconnected cells look like_

![Connected cell](https://media.discordapp.net/attachments/862971677440737340/867077123411935232/unknown.png)

_This is what 2 connected cells look like_

If you chose `0` recursive cells, then all you need to do to win the game is form a chain of connections between the two start / end cells. Depending on how lucky you were, you may be able to instantly finish it!

On the other hand, if you have any recursive cells then the game gets more interesting.

![Recursive cell](https://media.discordapp.net/attachments/862971677440737340/867078136515395635/unknown.png)

In order to rotate these cells, you must first do a mini game of Boxed, inside it!

![Boxed depth 1](https://media.discordapp.net/attachments/862971677440737340/867078484924956692/unknown.png)

This is what the inside of a recursive cell looks like, it may or may not contain even more recursive cells inside it; your current depth level can be tracked by the statistic in the bottom.

_Note: If you are inside a recursive cell and you want to go back by 1 depth: press `S`. Make sure not to press it while the depth level is `0` or else you will stop the game._

After you finish these recursive cells you can continue with the main puzzle and finish it.

![Victory screen](https://media.discordapp.net/attachments/862971677440737340/867079578471235594/unknown.png)

Wow you finished the game? You will be congratulated by your very own medal! Why not try to increase the number of recursive cells and/or grid dimensions and give another it another shot?

If you have read so far, please consider giving [this project](https://github.com/SystematicError/code-jam) a star if you liked it :)
