from typing import Any, List, Optional, Callable

# todo: write docstrings


BAR_VERTICAL = '│'
BAR_HORIZONTAL = '─'
CORNER_TOP_LEFT = '┌'
CORNER_TOP_RIGHT = '┐'
CORNER_BOTTOM_LEFT = '└'
CORNER_BOTTOM_RIGHT = '┘'
JUNCTION_TOP = '┬'
JUNCTION_LEFT = '├'
JUNCTION_CENTRE = '┼'
JUNCTION_RIGHT = '┤'
JUNCTION_BOTTOM = '┴'


def center_pad(item: Any, column_width: int) -> str:
    """
    :param item: An object that can be represented as a string via `str`.
    :param column_width: The width of the column containing the item, as an int.
    :return: A string padded to column_width + 2 with `str.center`.
    """
    if not isinstance(item, str):
        item = str(item)
    width = column_width + 2
    return item.center(width)


def ljust_pad(item: Any, column_width: int) -> str:
    """
    :param item: An object that can be represented as a string via `str`.
    :param column_width: The width of the column containing the item, as an int.
    :return: A string with one space on the left and the item padded to column_width + 1 with `str.ljust` on the right.
    """
    if not isinstance(item, str):
        item = str(item)
    width = column_width + 1
    return ' ' + item.ljust(width)


def make_border_horizontal(
        column_widths: List[int],
        left_piece: str, right_piece: str, centre_piece: str,
        join_piece: str = BAR_HORIZONTAL
) -> str:
    """
    :param column_widths: List containing the width of each column. Length must be the same as row.
    :param left_piece: The character to add to the left of the border.
    :param right_piece: The character to add to the right of the border.
    :param centre_piece: The character to add between columns.
    :param join_piece: The character that will make up the body of a column.
    :return: A formatted horizontal table border.
    """
    line_components = [left_piece]
    column_bars = [join_piece * (w + 2) for w in column_widths]
    line_components.append(centre_piece.join(column_bars))
    line_components.append(right_piece)

    line = ''.join(line_components)
    return line


def make_row(row: List[Any], column_widths: List[int], padder: Callable[[Any, int], str]) -> str:
    """
    :param row: List containing objects that have a single-line representation (via `str`).
    :param column_widths: List containing the width of each column. Length must be the same as row.
    :param padder: Function to pad text, which takes an object and a width and returns a padded string.
    :return: A formatted table row.
    """
    columns_padded = [padder(item, cwidth) for item, cwidth in zip(row, column_widths)]
    line_components = [''] + columns_padded + ['']
    return BAR_VERTICAL.join(line_components)


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """
    padder = center_pad if centered else ljust_pad

    # get the max width of each column
    columns = list(zip(*rows))
    columns_item_lengths = [[len(str(x)) for x in row] for row in columns]

    column_widths = []
    for i, column in enumerate(columns_item_lengths):
        if labels is not None:
            compare = column + [len(str(labels[i]))]
        else:
            compare = column
        column_widths.append(max(compare))

    # construct table as a list and join it at the end
    table_lines = [make_border_horizontal(column_widths, CORNER_TOP_LEFT, CORNER_TOP_RIGHT, JUNCTION_TOP)]

    if labels is not None:
        table_lines.append(make_row(labels, column_widths, padder))
        table_lines.append(make_border_horizontal(column_widths, JUNCTION_LEFT, JUNCTION_RIGHT, JUNCTION_CENTRE))
    for row in rows:
        table_lines.append(make_row(row, column_widths, padder))

    table_lines.append(make_border_horizontal(column_widths, CORNER_BOTTOM_LEFT, CORNER_BOTTOM_RIGHT, JUNCTION_BOTTOM))

    # join and return table
    table = '\n'.join(table_lines)
    return table


# debug, remove
print(make_table([
        ["Lemon", 18_3285, "Owner"],
        ["Sebastiaan", 18_3285.1, "Owner"],
        ["KutieKatj", 15_000, "Admin"],
        ["Jake", "MoreThanU", "Helper"],
        ["Joe", -12, "Idk Tbh"]
    ]))
print(make_table([
        ["Lemon", 18_3285, "Owner"],
        ["Sebastiaan", 18_3285.1, "Owner"],
        ["KutieKatj", 15_000, "Admin"],
        ["Jake", "MoreThanU", "Helper"],
        ["Joe", -12, "Idk Tbh"]
    ],
    labels=["User", "Messages", "Role"]))
table = make_table(
    rows=[
        ["Lemon"],
        ["Sebastiaan"],
        ["KutieKatj9"],
        ["Jake"],
        ["Not Joe"]
    ]
)
print(table)
table = make_table(
   rows=[
       ["Ducky Yellow", 3],
       ["Ducky Dave", 12],
       ["Ducky Tube", 7],
       ["Ducky Lemon", 1]
   ],
   labels=["Name", "Duckiness"],
   centered=True
)
print(table)
