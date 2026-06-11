"""Tkinter-based clipboard adapter for table copy/paste."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk


class ExcelAdapter:
    """Enable Excel-compatible copy/paste on a ttk.Treeview."""

    def __init__(self, treeview: ttk.Treeview) -> None:
        self.j_table1: ttk.Treeview = treeview
        self.rowstring: str = ""
        self.value: str = ""
        treeview.bind("<Control-c>", self._on_copy)
        treeview.bind("<Control-v>", self._on_paste)

    def getJTable(self) -> ttk.Treeview:
        return self.j_table1

    def setJTable(self, treeview: ttk.Treeview) -> None:
        self.j_table1 = treeview

    def actionPerformed(self, action_command: str) -> None:
        if action_command == "Copy":
            self._copy_selection()
        if action_command == "Paste":
            self._paste_selection()

    def _on_copy(self, event: tk.Event) -> str:
        self._copy_selection()
        return "break"

    def _on_paste(self, event: tk.Event) -> str:
        self._paste_selection()
        return "break"

    def _copy_selection(self) -> None:
        selected = self.j_table1.selection()
        if not selected:
            return
        rows = sorted({self.j_table1.index(item) for item in selected})
        cols = sorted(
            {
                int(self.j_table1.heading(col)["text"].replace("#", "")) - 1
                if col.startswith("#")
                else list(self.j_table1["columns"]).index(col)
                for item in selected
                for col in self.j_table1.item(item)["values"]
            },
            key=lambda x: x,
        )
        col_ids = list(self.j_table1["columns"])
        if not rows or not col_ids:
            return
        if not (
            rows[-1] - rows[0] + 1 == len(rows)
            and len(col_ids) == len(set(col_ids))
        ):
            messagebox.showerror("Invalid Copy Selection", "Invalid Copy Selection")
            return
        lines: list[str] = []
        for row_idx in rows:
            item_id = self.j_table1.get_children()[row_idx]
            values = self.j_table1.item(item_id)["values"]
            lines.append("\t".join(str(v) for v in values))
        text = "\n".join(lines)
        root = self.j_table1.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(text)

    def _paste_selection(self) -> None:
        root = self.j_table1.winfo_toplevel()
        try:
            trstring = root.clipboard_get()
        except tk.TclError:
            return
        selected = self.j_table1.selection()
        if not selected:
            return
        start_row = self.j_table1.index(selected[0])
        start_col = 0
        children = self.j_table1.get_children()
        for i, line in enumerate(trstring.split("\n")):
            if not line:
                continue
            row_idx = start_row + i
            if row_idx >= len(children):
                break
            item_id = children[row_idx]
            values = list(self.j_table1.item(item_id)["values"])
            for j, cell in enumerate(line.split("\t")):
                col_idx = start_col + j
                if col_idx < len(values):
                    values[col_idx] = cell
            self.j_table1.item(item_id, values=values)
