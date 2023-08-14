from arcade.gui import UIFlatButton

button_style = {
    "normal": UIFlatButton.UIStyle(
        font_size=19
    ),
    "hover": UIFlatButton.UIStyle(
        font_size=19,
        font_name=("calibri", "arial"),
        font_color=(255, 255, 255, 255),
        bg=(21, 19, 21, 255),
        border=(77, 81, 87, 255),
        border_width=2,
    ),
    "press": UIFlatButton.UIStyle(
        font_size=19,
        font_name=("calibri", "arial"),
        font_color=(0, 0, 0, 255),
        bg=(255, 255, 255, 255),
        border=(255, 255, 255, 255),
        border_width=2,
    ),
    "disabled": UIFlatButton.UIStyle(
        font_size=19,
        font_name=("calibri", "arial"),
        font_color=(211, 211, 211, 255),
        border=(102, 102, 153, 255),
        border_width=2,
    )
}
