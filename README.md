# React Parameter

React Parameter is a small Python script to **automate and facilitate the creation and updating of contextual variables in <ins>real time</ins> with React** (JSX & TSX).
It scans your `index` file and retrieves all the constant states (with double brackets `[ ]`) then reassembles them by creating a variable called `app` in your file each time you save it (your `index` file must be in your `./src` folder).
Think carefully about setting up your environment so that the context is spread correctly.

## Typescript
If you use Typescript, RP will retrieve the types of your states then create an interface (named `NkContext`) allowing you to keep the type and properties of your states everywhere in your project, it also creates an `NkContextVariant` typing component in order to add custom properties to the `NkContext` by extends. (you will simply need to place a typing of `NkContext` in front of each instactiation of `const app`)
If your state has no type, it will automatically be set to `any`.

## Setup
For the moment it's just a Python script (I plan to make it an NPM library later in order to install it directly in the projects), you can setup it by placing it in your programs folder and doing a alias in your OS to access it from the terminal.
The Python script however takes arguments at launch (`$*` corresponds to the name of your index file with its extension):

Windows: `py "path/to/script" "%cd%" $*`

Linux/MacOS: `python3 "path/to/script" pwd $*`
