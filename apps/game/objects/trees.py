from apps.game.objects.characters import Object
from survive.settings import BASE_DIR


class Tree(Object):
    pass

class Pine(Tree):
    image_path = BASE_DIR+"/static/images/trees/pine_tree/pine_tree.png"

class Pine2(Tree):
    image_path = BASE_DIR+"/static/images/trees/pine_tree/pine_tree-2.png"

class Pine3(Tree):
    image_path = BASE_DIR+"/static/images/trees/pine_tree/pine_tree-3.png"

class Birch(Tree):
    image_path = BASE_DIR+ "/static/images/trees/birch_tree/birch_tree.png"

class Birch2(Tree):
    image_path = BASE_DIR+ "/static/images/trees/birch_tree/birch_tree-2.png"

class Birch3(Tree):
    image_path = BASE_DIR+ "/static/images/trees/birch_tree/birch_tree-3.png"

class Oak(Tree):
    image_path = BASE_DIR + "/static/images/trees/oak_tree/oak_tree.png"

class Oak2(Tree):
    image_path = BASE_DIR + "/static/images/trees/oak_tree/oak_tree-2.png"

class Oak3(Tree):
    image_path = BASE_DIR + "/static/images/trees/oak_tree/oak_tree-3.png"

class Tropical(Tree):
    image_path = BASE_DIR+ "/static/images/trees/tropical_tree/tropical_tree.png"

class Tropical2(Tree):
    image_path = BASE_DIR+ "/static/images/trees/tropical_tree/tropical_tree-2.png"

class Tropical3(Tree):
    image_path = BASE_DIR+ "/static/images/trees/tropical_tree/tropical_tree-3.png"