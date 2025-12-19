# Boxes

A library to wrap arround python's curses, offering a lot of functions similar to "high-end" TUI-librarys - all without the steep learning curve.

---
---

## Installing

Just install the pip package:

```bash
pip install boxes-tui
```

Or copy the `src/boxes_tui/` folder into your project's folder.

---
---

## Usage

### Text formating

---

When using the `Label` class (or basically any other thing that displays a text, under the hood it's all using `Label`) you can use the following text formatting options to change things like colour. beeing bold/italic/underlined and similar.

The formating options have to be enclosed by `//§` & `§//` and seperated by `,`.  
As the formatting will be run through python's `.strip()` command, spaces, newline, tabs, etc can be added without consequences. (Most of the following examples have spaces, but you don't *need* any)

```python
options = """//§
            C:red, bold, italic
        §//"""
Label(f'{options}This text is red, bold AND italic!')
```

All formating options only apply up to the next formating option:

```python
Label('//§C:red§//This text is red and //§C:green§//this text is green!//§§// (and this text is back to normal)')
```

Within these options you can set options that apply instead, if the Label is selected:

```python
Label('//§ C:red, bold, //S C:red-reverse, italic S//§//Hello World!')
```

**Note**: This will first remove all of the 'normal' options; if the normal options include `bold`, that doesnt need to mean that the inverted text is also bold, if you use this approach  

**Overview options**:

| Option       | Explanation                                                                                                                                                      | Example                                      |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------- |
| `C:<colour>` | Sets the normal colour of the Text, `<colour>` is a int representing the colour pair or a key from `SHARED_VAS["COLOUR]`. If not set, colour pair 1 will be used | `C:3`, `C:red`                               |
| `//S`, `S//` | Specify the options inside that should be used if the Label is selected                                                                                          | `//S C:red-reverse, bold S//`                |
| `reverse`    | The colour will be inverted. (**Note**: The colours can't be inverted twice (aka back), so this will not change `I`, if it is the default colour but inverted)   | `C:3,reverse` > selected & not look the same |
| `bold`       | This will make the text **bold**                                                                                                                                 | --                                           |
| `italic`     | This will make the text *italic*                                                                                                                                 | --                                           |
| `dim`        | This will dim the colours of the text                                                                                                                            | --                                           |
| `underline`  | This will <ins>underline</ins> the text                                                                                                                          | --                                           |
| `standout`   | This will apply `curses.A_STANDOUT`, wich just seems to invert the colour or something; I'm not shure what this is; look into the curses docs                    | --                                           |

You can also pass in other options as "string-yfied" ints:

```python
Label(f'//§{str(curses.A_BLINK)}§//*Blink!*')
```

---
---

## 

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
| Classes                   | CamelCase      |

### Jupyter

---

This project uses Jupyter (iPython notebooks (.ipynb files)) for some larger modules.  
To convert them to python source code (.py files), simply run `convert.sh` (or execute the `Export All Jupyter Notebooks` VSCode task; that will do the same thing).

> [!Note]
> All changes to the "compiled" python files will be lost upon calling `convert.sh`; always change the notebooks, not the python files!

### AI

---

> [!Note]  
> I am not a fan of so called "vibe-coding".  
> All code in this repo was 100% written by a human (me).  
> AI WAS USED, but only to ask about best-practices or the like; **No code of AI was ever implementet** (or even generated on purpose)  
> (This may not remain accurate if other people commit, I can not check for AI code in pull request with absolute certainty, so I won't even try)  
