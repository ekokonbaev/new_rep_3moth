from db import main_db


import flet as ft

def main(page: ft.Page):
    page.title = "ToDo List"
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column()

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_tasks():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))
        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        def save_task(_):
            main_db.update_task(task_id, task_field.value)
            task_field.read_only = True
            edit_button.icon = ft.Icons.EDIT
            edit_button.on_click = edit_task
            page.update()

        def edit_task(_):
            task_field.read_only = False
            edit_button.icon = ft.Icons.SAVE
            edit_button.on_click = save_task
            page.update()

        def delete_task(_):
            main_db.delete_task(task_id)
            load_task()

        #delete all
        def delete_all_task(_):
            main_db.delete_all_task(task_id)
            load_task    

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=edit_task)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task)
        row = ft.Row([task_field, edit_button, delete_button])
        return row


    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            task_input.value = ""
            page.update()


    task_input = ft.TextField(label='Введите задачу', expand=True)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task)

    def delete_all_tasks(_):
        tasks = main_db.get_tasks()
        for task_id, _ in tasks:
            main_db.delete_task(task_id)
        load_task()

    delete_all_button = ft.ElevatedButton("Удалить все", on_click=delete_all_tasks)

    page.add(
        ft.Row([task_input, add_button, delete_all_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        task_list
    )

    load_task()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)