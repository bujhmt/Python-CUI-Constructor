https://github.com/bujhmt/utils for suggestions and corrections

version: 1.1.0

# How to start?

1) Add module to your code:

    > import cui

2) Create an instance of the class:

    > menu = cui.CUI() [default title for root - "Main menu"]

    > menu = cui.CUI("{custom title}")

3) Create field:

    > menu.addField("{custom field title}", lambda: {custom function  e.g. add smth to db})

    > menu.addField("{custom field title}") [for simple members or collections]

4) Create Menu

    > menu.addMenu({"title"})

    ##### when you create a new menu, all your new [addField] and [addMenu] calls will refer to this menu
    ##### Calling [finishMenu()] method will terminate this menu and return you to the previous menu.
    
5) Finish Menu

    > menu.finishMenu() [terminate this menu and return you to the previous menu]

6) Using:
    
    > menu.run()

    > Use English {W} and {S} to move up and down in the menu, press {ENTER} to select the highlighted item

# Cross-platform capability

> Linux: +

> Windows: +


