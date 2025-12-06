# levels.py
"""
Legend:
    # = wall
    . = target
    $ = box
    @ = player
    * = box on target
    + = player on target
    space = floor
"""

LEVEL_1 = [
    "#######",
    "#     #",
    "#  .  #",
    "#  $  #",
    "#  @  #",
    "#     #",
    "#     #",
    "#######"
]

LEVEL_2 = [
    "#######",
    "# . @ #",
    "# ### #",
    "# $   #",
    "#   $ #",
    "# .   #",
    "#     #",
    "#######"
]

LEVEL_3 = [
    "#######",
    "# .   #",
    "# ### #",
    "# $ $ #",
    "#   @ #",
    "#   . #",
    "#  $ .#",
    "#######"
]

LEVEL_4 = [
    "#######",
    "# .  @#",
    "# $#$ #",
    "#  #  #",
    "#   $ #",
    "# .   #",
    "# .$ .#",
    "#######"
]

LEVEL_5 = [
    "######",
    "#. ..#",
    "#  $.#",
    "##  $##",
    " #  $ #",
    " #$## #",
    " # @  #",
    " ######"    
]

LEVEL_TEST_DEADLOCK = [
    "#######",
    "#     #",
    "#  .  #",
    "###   #",
    "#$ @  #",
    "#     #",
    "#     #",
    "#######",
]

LEVELS = {
    "level_1l": LEVEL_1,
    "level_2": LEVEL_2,
    "level_3": LEVEL_3,
    "level_4": LEVEL_4,
    "level_5": LEVEL_5,
    "level_test_deadlock": LEVEL_TEST_DEADLOCK,
}
