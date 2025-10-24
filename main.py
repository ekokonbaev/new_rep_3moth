from db import main_db
import flet as ft


def main(page: ft.Page):
    page.title = "ToDo List"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()

    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completed=completed))

        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()
        
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        return ft.Row([checkbox, task_field, edit_button, save_button])

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))
            task_input.value = ""
            page.update()

    task_input = ft.TextField(label='Введите задачу', expand=True)
    add_button = ft.ElevatedButton("ADD", on_click=add_task)

    def set_filter(filter_value):
        nonlocal filter_type 
        filter_type = filter_value
        load_task()

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter(filter_value='all')),
        ft.ElevatedButton('К выполнения', on_click=lambda e: set_filter(filter_value='uncompleted')),
        ft.ElevatedButton('Выполнено ✅', on_click=lambda e: set_filter(filter_value='completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(ft.Row([task_input, add_button]), filter_buttons, task_list)

    load_task()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)