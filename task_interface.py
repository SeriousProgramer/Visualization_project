# task_interface.py
from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def get_plot(self, any):
        pass

# #Callback to update the plot area based on the selected task
# @app.callback(
#     Output('task-content', 'children'),
#     [Input('task-selector', 'value')]
# )
# def update_output(selected_task):
#     task = TASKS.get(selected_task)
#     return task.layout() if task else "Please select a task"