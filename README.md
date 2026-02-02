# Boxes

A library to wrap arround python's curses, offering a lot of functions similar to "high-end" TUI-librarys - all without the steep learning curve.

---
---

## Installing

Just install the pip package:

```bash
pip install boxes-tui
```

(Or copy the `src/boxes_tui/` folder into your project's folder.)

## Misc / Trivia / Notes

### Why did I make this?

---

It all started with a simple box - or a *function* to draw a box would be more accurate -  
I had just begun learing python's curses library and was working on my first TUI project. (If you want to see that for some reason: [confessions](https://github.com/IamLegende7/confessions) (it isn't very good))  
While working I realized I needed two functions **a lot**: drawing boxes and making simple menus.

So I thought: why not make a template for my other projects? - short story even shorter: boxes 1.0 was born!

After a while, I came back to it, realised my code was absolute garbage and made a version 2.0: a PyPI library called boxes-tui.  
(If you want to see that code: you can find it [here](https://github.com/IamLegende7/boxes-tui-deprecated))

But I have learned much since then, (mainly that my boxes-tui-2 code was horrible) so I decided to make a version 3.0: the project you are reading the README of right now!

This time, I've learned from other TUI-librarys what I want (and what I don't want) in boxes 3.0.  
I am sure I can make something useful this time!

### Naming convention

---

| Object type               | case           |
| :------------------------ | :------------- |
| Variables, functions, etc | snake_case     |
| Global variables          | SCREAMING_CASE |
| Classes                   | PascalCase     |
