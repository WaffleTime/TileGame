# TileGame

This is a data-driven, Entity-Component-System (ECS) framework that makes use of entities and components. Entities are essentially a collection of 
components and components hold data for the most part (along with defining methods for rendering and updating if it applies.) However, the entities 
by themselves are incomplete because they aren't technically supposed to define their own behavior in a traditional ECS implementation. Thus, 
systems exist to update entities in batches.

This framework is driven by a state configuration interpreter -- only one configuration file is loaded at a time. These configurations define the
entities, systems and inputs that are to be loaded into the framework at a particular state. Systems are capable of altering the state and triggering
another state configuration to be loaded. Systems are also capable of adding/alterning/removing entities, systems and inputs within the current
state.

The state configurations used by this framework are meant to be directly linked to the components, entity assemblers and systems that are defined in
the game's Python files -- everything except the base framework's files. This essentially means that the framework and the game files will be jumbled
together into a single project, but that is fine for experimenting. In hindsight, I would now separate the base framework files into their own project 
and make them available using pip or some other dependency management tool.

## Component Features:
* Components are classes that inherit the Component class.
* Components can manage their own data and enforce expected usages by defining meaningful methods.
* Components can update themselves each frame -- goes against traditional ECS ideas, but is useful for some things.
* Components can draw themselves to the screen -- goes against traditional ECS ideas, but is useful for some things.

## Systems Features:
* Can access/alter data within dependent components -- which belong to entities.
* Can execute each frame or once.
* Can trigger systems for future execution.
* Can change the state within the global state machine of the game.

## Input Handling:
Two types of inputs are supported: hotspots and key presses. The hotspots are used for button-like interactions and arer handled by a quad tree.
The key presses are able to be defined as a complex sequential string of key presses. So that allows the possibility of a cool Street Fighter-like 
combat system.

# Prerequisites

The latest 32-bit version of Python 2.7 will probably work, but you can fallback to [this](https://www.python.org/downloads/release/python-2715/) version.

# Usage

The distribution phase of this project hasn't been figured out completely since it was just an early experiment. 
Just to make it easy, open a command prompt in the project's root directory and then enter the following:

```
python main.py
```

# Sample

Below is just a sample of the main menu. The really interesting part about this menu is that it is built using the same
components and systems that are used in many of the other parts of the current game. It really was incredible to watch as it evolved.

[sample](https://github.com/jawaff/TileGame/blob/master/images/sample.jpg?raw=true)