https://github.com/bujhmt/utils for suggestions and corrections

version: 1.0.0

#How to start?#

1) Add module to your code:

    > import CUI

2) Create an instance of the class:

    > cui = CUI() [default title for root - "Main menu"]
        or
    > cui = CUI("{custom title}")

3) Create field:

    > cui.addField("{custom field title}", lambda: {custom function  e.g. add smth to db})
        or
    > cui.addField("{custom field title}") [for simple members or collections]

4) Create Menu

    > cui.addMenu({"title"})

    !when you create a new menu, all your new [addField] and [addMenu] calls will refer to this menu
    !Calling [cui.finishMenu()] method will terminate this menu and return you to the previous menu.

5) Using:
    
    > cui.run()

    > Use English {W} and {S} to move up and down in the menu, press {ENTER} to select the highlighted item

#Cross-platform capability#

> Linux: +
> Windows: ?


