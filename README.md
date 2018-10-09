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

# Execution

The distribution phase of this project hasn't been figured out completely since it was just an early experiment. 
In order to execute the framework (just to make it easy), open a command prompt in the project's root directory and then enter the following:

```
python main.py
```

# Sample

Below is just a sample of the main menu. The really interesting part about this menu is that it is built using the same
components and systems that are used in many of the other parts of the current game. It really was incredible to watch as it evolved.

![sample](https://github.com/jawaff/TileGame/blob/master/images/sample.jpg?raw=true)

# Using the Framework

## State Configurations

The current state configuration files are located under the "StateData" directory of this project. Each subdirectory therein should be thought of as a 
macro state. Each state configuration file within those subdirectories should be thought of as a substate of the containing macro state. The framework is
currently hardcoded to start with the ["Menu", "Intro"] state (which will be defined by the StateData/Menu/Intro.xml state configuration file). All other
state configuration files are loaded when a system triggers a change of state.

Currently state changes are being handled by a "State" component, a "Change_State" system and some sort of system/input trigger. The "State" component that is 
being transitioned to needs to be owned by some entity -- the State component is mutable. In order to transition to another state, the "Change_State" system
must be triggered and it must consume an entity containing the target state.

The beforementioned state changes can be defined just like in the following state configuration sample. In the below example, we see that the "Predined1" button
has a "State" component for the state ["Menu", "MainMenu"]. We can also see that a hotspot input references the "Change_State" system and the "Predefined1" button within
the "OnReleased" section. All of this means that the ["Menu", "MainMenu"] state will be transitioned to after the hotspot input's "OnReleased" event has been triggered.

```xml
	<Entity name='Predefined1' type='Button'>
		<assembleFunc>Assemble_Button</assembleFunc>
		<drawPriority>1</drawPriority>
		<Attributes>
			<x>400</x>
			<y>300</y>
			<width>150</width>
			<height>50</height>
			<text>Main Menu</text>
			<Font name='Asman'>ASMAN.ttf</Font>
		</Attributes>
		<Component name='State'>
			<componentID>0</componentID>
			<state>Menu,MainMenu</state>
		</Component>
	</Entity>
	<Input type='hotspot'>
		<x>400</x>
		<y>300</y>
		<width>150</width>
		<height>50</height>
		<OnReleased>
			<system>Change_State</system>
			<entity>
				<entityType>Button</entityType>
				<entitytName>Predefined1</entitytName>
				<componentName>state</componentName>
			</entity>
		</OnReleased>
	</Input>
```

## Entities

The state configuration files allow for a list of components or an "assembler" to be used for creating entities. An "assembler" (follows the factory 
design pattern) is used to assemble the components necessary for a particular type of entity. These assemblers are defined under the Entities/ directory 
of this project and they assume some dictionary of attributes that will eventually initialize the data within the produced entity's components. 
It's possible to add extra components to the entity that is produced by an asembler or just make a list of components. 

Here is one example of a state configuration that references a button assembler and an extra State component:

```xml
	<Entity name='Predefined1' type='Button'>
		<assembleFunc>Assemble_Button</assembleFunc>
		<drawPriority>1</drawPriority>
		<Attributes>
			<x>400</x>
			<y>300</y>
			<width>150</width>
			<height>50</height>
			<text>Main Menu</text>
			<Font name='Asman'>ASMAN.ttf</Font>
		</Attributes>
		<Component name='State'>
			<componentID>0</componentID>
			<state>Menu,MainMenu</state>
		</Component>
	</Entity>
```

The actual button assembler looks like this:

```python
def Assemble_Button(sEntityName, sEntityType, iDrawPriority, attribDict):
    """This assembles a box with text in it! And sets up some other
    components that'll store important information we might need later."""
    entity = Entity(sEntityName, sEntityType, iDrawPriority, {})

    entity._Add_Component(getClass("Box")({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height']}))
    entity._Add_Component(getClass("Text_Line")({'componentID': '0', 'x': attribDict['x'], 'y': attribDict['y'], 'width': attribDict['width'], 'height': attribDict['height'], 'text': attribDict['text'], 'font': attribDict['Font']["Asman"]}))
    entity._Add_Component(getClass("Flag")({'componentID': '0', 'flag': False}))

    return entity
```

## Components

The components are what are drawn to the screen and what hold information about what is going on in the game. A component could be for an animated sprite,
a collision shape, a shape or even a collection of other components. Components are defined in the Components/ directory. All components have the option to
be renderable and updatable -- the components must define the render and udpate behavior.

Here is a simple Box component example:

```python
class Box(Component):
    def __init__(self, dData):
        Component.__init__(self, "BOX:%s"%(dData['componentID']), False, 1)
        self._box = sf.RectangleShape((int(dData['width']),int(dData['height'])))
        self._box.position = (int(dData['x']),int(dData['y']))
        self._box.fill_color = sf.Color.WHITE
        self._box.outline_color = sf.Color.RED
        self._box.outline_thickness = 3.0

    def _Set_Color(self, fillColor, outlineColor):
        self._box.fill_color = fillColor
        self._box.outline_color = outlineColor

    def _Get_Color(self):
        return self._box.fill_color

    def _Switch_Color(self):
        tmpColor = self._box.fill_color
        self._box.fill_color = self._box.outline_color
        self._box.outline_color = tmpColor

    def _Get_Box(self):
        return self._box

    def _Render(self, renderWindow):
        renderWindow.draw(self._box)
```

## Systems

This project was kind of abandoned during its evolution. Currently systems all live under a single class in the Systems.py file. 
My intention was to make each system function loaded from its own file within a directory (much like how assembler functions work).
Below is one example of a system function that simply returns the contents of a State component. Every system has the option to 
return either None or a new state that will be transitioned to.

```python
def Change_State(dEntities):
    """This will be able to be used by Inputs of various kinds as well as any other place in the Entity_Managers (or the other systems, but I don't want much of it.)
    It's objective is to make the Entity_Manager._Input_Update() method return a new lNextState variable for the main. And this variable will be able to change the state of the
    game to any other state!"""
    print dEntities['state']._Get_Component('STATE:0')._Get_State()
    #This will access the entity that is connected to the 'state' key and we then get the State component from it and call its _Get_State() method to get a string containing the two states (1st and 2nd level) for the next state to be.
    return dEntities['state']._Get_Component('STATE:0')._Get_State()       #The split breaks a string into chunks in-between a given character and puts those chunks into a list (which is what we want to return.)
```

## Inputs

### Hotspots

A hotspot input is simply an invisible square that triggers events based on the location of the mouse. If the mouse has entered
the hotspot, then the OnSelected event is triggered and the OnDeSelected event is triggered after the mouse has moved off of the hotspot.
Similarly if the mouse clicks on the hotspot, then the OnPressed and OnReleased events will be triggered accordingly. These events are able
to optionally be tied to a system. In those cases, the system is executed after the event has beeen triggered.

```xml
	<Input type='hotspot'>
		<x>400</x>
		<y>300</y>
		<width>150</width>
		<height>50</height>
		<OnSelected>
			<system>Oscillate_Box_Colors</system>
			<entity>
				<entityType>Button</entityType>
				<entitytName>Predefined1</entitytName>
				<componentName>box</componentName>
			</entity>
		</OnSelected>
		<OnDeselected>
			<system>Oscillate_Box_Colors</system>
			<entity>
				<entityType>Button</entityType>
				<entitytName>Predefined1</entitytName>
				<componentName>box</componentName>
			</entity>
		</OnDeselected>
		<OnPressed>
			<system>Play_Sound</system>
			<entity>
				<entityType>Sound</entityType>
				<entitytName>ButtonPress</entitytName>
				<componentName>press_sound</componentName>
			</entity>
		</OnPressed>
		<OnReleased>
			<system>Change_State</system>
			<entity>
				<entityType>Button</entityType>
				<entitytName>Predefined1</entitytName>
				<componentName>state</componentName>
			</entity>
		</OnReleased>
	</Input>
```

### Key

A key input refers to mouse buttons and keyboard keys. Additionally, combinations of key presses are able to be defined 
-- which supports the street fighter use case. When the defined combination of key presses is witnessed by the framework, 
some system will be triggered for execution. Key combinations support both sequential (key codes separated by '/') and 
simultaneous presses (key codes separated by '.'). The input key "/24/24/24." is triggered when the 'x' key code is sequentially
pressed three times. The input key "/24.25.26." is triggered when the 'x', 'y' and 'z' key codes are all pressed down before
any of them are released.

Refer to [this](https://www.sfml-dev.org/documentation/2.5.0/classsf_1_1Keyboard.php) page for the possible input key codes. 
Below is an example from a state configuration:

```xml
	<Input type='key'>
		<key>/23.24.25.</key>
		<OnReleased>
			<system>Change_State</system>
			<entity>
				<entityType>KeyPress</entityType>
				<entitytName>Custom1</entitytName>
				<componentName>state</componentName>
			</entity>
		</OnReleased>
	</Input>
```