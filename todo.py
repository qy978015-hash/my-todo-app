"""待办事项桌面应用（tkinter 版）"""

import json
import os
import tkinter as tk
from tkinter import messagebox

# 数据文件路径（和 exe 同目录，确保打包后数据持久化）
DATA_FILE = os.path.join(os.path.dirname(sys.executable), "todo.json")


def load_tasks():
    """从文件加载待办事项"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    """保存待办事项到文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


class TodoApp:
    def __init__(self):
        self.tasks = load_tasks()

        # 创建主窗口
        self.win = tk.Tk()
        self.win.title("我的待办事项 v2")
        self.win.geometry("480x520")

        # === 输入区 ===
        frame_input = tk.Frame(self.win)
        frame_input.pack(pady=12)

        tk.Label(frame_input, text="待办内容：").pack(side=tk.LEFT)
        self.entry = tk.Entry(frame_input, width=30, font=("微软雅黑", 11))
        self.entry.pack(side=tk.LEFT, padx=6)
        self.entry.bind("<Return>", lambda e: self.add_task())  # 回车键添加
        tk.Button(frame_input, text="添加", command=self.add_task,
                  bg="#4CAF50", fg="white", width=8).pack(side=tk.LEFT)

        # === 列表区 ===
        frame_list = tk.Frame(self.win)
        frame_list.pack(fill=tk.BOTH, expand=True, padx=16)

        self.listbox = tk.Listbox(frame_list, font=("微软雅黑", 12),
                                  selectbackground="#E8E8E8",
                                  activestyle="none")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 滚动条
        scrollbar = tk.Scrollbar(frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # === 按钮区 ===
        frame_btns = tk.Frame(self.win)
        frame_btns.pack(pady=10)

        tk.Button(frame_btns, text="标记完成", command=self.done_task,
                  bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=4)
        tk.Button(frame_btns, text="删除", command=self.delete_task,
                  bg="#F44336", fg="white", width=10).pack(side=tk.LEFT, padx=4)

        # 刷新列表显示
        self.refresh_list()

    def refresh_list(self):
        """刷新列表显示"""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            # 已完成的任务前面加 [v]，未完成的加 [ ]
            prefix = "✅ " if task["done"] else "⬜ "
            self.listbox.insert(tk.END, prefix + task["text"])
            # 已完成的任务文字变灰
            if task["done"]:
                self.listbox.itemconfig(tk.END, fg="gray")
            else:
                self.listbox.itemconfig(tk.END, fg="black")

    def add_task(self):
        """添加待办事项"""
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("提示", "请输入待办内容")
            return
        self.tasks.append({"text": text, "done": False})
        save_tasks(self.tasks)
        self.entry.delete(0, tk.END)  # 清空输入框
        self.refresh_list()

    def done_task(self):
        """标记选中项为已完成"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("提示", "请先选中一个待办事项")
            return
        idx = selected[0]
        if self.tasks[idx]["done"]:
            messagebox.showinfo("提示", "这个事项已经完成了")
            return
        self.tasks[idx]["done"] = True
        save_tasks(self.tasks)
        self.refresh_list()

    def delete_task(self):
        """删除选中项"""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("提示", "请先选中一个待办事项")
            return
        idx = selected[0]
        if messagebox.askyesno("确认", f"确定要删除「{self.tasks[idx]['text']}」吗？"):
            self.tasks.pop(idx)
            save_tasks(self.tasks)
            self.refresh_list()

    def run(self):
        """启动窗口"""
        self.win.mainloop()


if __name__ == "__main__":
    app = TodoApp()
    app.run()
