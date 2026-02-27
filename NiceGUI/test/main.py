from nicegui import ui
from pathlib import Path

def load_directory():
    items = Path("env").iterdir()
    grid.options["rowData"] = [{"name": i.name, "type": "Folder" if i.is_dir() else "File"} for i in items]
    grid.update()


ui.button("Load directory", on_click=load_directory)
ui.label("Files:")
grid = ui.aggrid({
    "columnDefs": [
        {"headerName": "Name", "field": "name"},
        {"headerName": "Type", "field": "type"},
    ],
    "rowData": [],
})


ui.run(native=True)

