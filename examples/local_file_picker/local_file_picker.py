from pathlib import Path
from typing import Optional

from nicegui import ui


class local_file_picker(ui.dialog):

    def __init__(self, directory: str, *,
                 upper_limit: Optional[str] = None, multiple: bool = False, show_hidden_files: bool = False) -> None:
        """Local File Picker

        This is a simple file picker that allows you to select a file from the local filesystem where NiceGUI is running.

        :param directory: The directory to start in.
        :param upper_limit: The directory to stop at. If not specified, the upper limit is the same as the starting directory.
        :param multiple: Whether to allow multiple files to be selected.
        :param show_hidden_files: Whether to show hidden files.
        """
        super().__init__()

        self.path = Path(directory).expanduser()
        self.upper_limit = Path(upper_limit if upper_limit else directory).expanduser()
        self.show_hidden_files = show_hidden_files

        with self, ui.card():
            self.table = ui.table({
                'columnDefs': [{'field': 'name', 'headerName': 'File'}],
                'rowSelection': 'multiple' if multiple else 'single',
            }, html_columns=[0]).classes('w-96').on('cellDoubleClicked', self.handle_double_click)
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self._handle_ok)
        self.update_table()

    def update_table(self) -> None:
        paths = list(self.path.glob('*'))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith('.')]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.table.options['rowData'] = [
            {
                'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
                'path': str(p),
            } for p in paths
        ]
        if self.path != self.upper_limit:
            self.table.options['rowData'].insert(0, {
                'name': '📁 <strong>..</strong>',
                'path': str(self.path.parent),
            })
        self.table.update()

    async def handle_double_click(self, msg: dict) -> None:
        self.path = Path(msg['args']['data']['path'])
        if self.path.is_dir():
            self.update_table()
        else:
            self.submit([str(self.path)])

    async def _handle_ok(self):
        rows = await ui.run_javascript(f'getElement({self.table.id}).gridOptions.api.getSelectedRows()')
        self.submit([r['path'] for r in rows])
