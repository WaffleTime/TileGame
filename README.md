TileGame
========
This is a data-driven game that makes use of entities and components. Entities are essentially a collection of components and components hold data for the most part (along with defining methods for rendering and updating if it applies.)

That by itself is very nice for reuse-oriented software engineering, but doesn't explain how entities are able to interact with one another. For that there is a thing I call "systems" that are function that will receive a dictionary of entities as a parameter. From there the system functions are able to access/alter the data within the components of the entities that were received. These systems can be defined to be executed continuously each frame or they can be executed once. And systems can tell the game to add other systems to the queue of active systems (which is very important.) Systems also must return a string that can either be NULL or the name of the state that is to be transitioned to (that's how scenes are switched to and from.)

Aside from entities, components and systems there are also different types of inputs that are defined. There are hotspots and there are key presses. The hotspots are used for buttons and handled by a quad tree. And the key presses are able to be defined as a complex sequential string of key presses. So that allows the possibility of a cool Street Fighter-like combat system.

You might think how these different things are able to work in a data-driven manner. But the answer is pretty simple actually. There are XML files for each different scene in the game -- multiple files helps so much with maintainability -- that define entities, systems and inputs that are to be loaded into that scene. The XML file allows initial data to be given to the components that are chosen for each entity. And the systems are defined with the names/type of the entity that they are to deal with.

There's a long way to go before the game I'm making with this will be done, but I'm pretty happy about the method that I've actually gotten to work so far. It has gone through a lot of refactoring and has even been completely rewritten at one point.
