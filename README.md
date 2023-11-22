# React Parameter

React Parameter is a small Python script to automate and facilitate the creation of contextual variables with React (JSX & TSX).
It scans your index file and retrieves all the constant states (with double brackets `[ ]`) then brings them together by creating a variable called `app` in your file.
Think carefully about setting up your environment so that the context is spread correctly.

## Typescript
If you use Typescript, RP will retrieve the types of your states then create an interface (named `NkContext`) allowing you to keep the type and properties of your states everywhere in your project (you will simply need to place a typing of `NkContext` in front of each instactiation of `const app`)
If your state has no type, it will automatically be set to `any`.
