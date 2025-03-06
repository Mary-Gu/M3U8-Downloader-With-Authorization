import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time

def animate_loading(status_label, is_downloading):
    """动态显示下载指示器，点数在1-3个之间变化"""
    dots = 1
    while is_downloading[0]:
        status_label.config(text=f"下载中{'.' * dots}")
        dots = (dots % 3) + 1
        time.sleep(0.5)
    status_label.config(text="")

def download_video():
    m3u8_url = url_entry.get().strip()
    if not m3u8_url:
        messagebox.showerror("错误", "请输入M3U8链接地址。")
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4文件", "*.mp4")])
    if not save_path:
        return
    
    # 禁用下载按钮，避免重复点击
    download_button.config(state=tk.DISABLED)
    
    # 创建一个标志来控制动画线程
    is_downloading = [True]
    
    # 启动动画线程
    animation_thread = threading.Thread(
        target=animate_loading,
        args=(status_label, is_downloading)
    )
    animation_thread.daemon = True
    animation_thread.start()
    
    # 获取选定的质量设置
    quality = quality_var.get()
    
    # 在单独的线程中执行下载
    def download_task():
        try:
            # 根据选定的质量设置生成适当的ffmpeg命令
            if quality == "高质量 (原始大小)":
                # 直接复制，不重新编码
                command = f'ffmpeg -i "{m3u8_url}" -c copy -bsf:a aac_adtstoasc "{save_path}"'
            elif quality == "中等质量 (较小体积)":
                # 使用h264编码，中等比特率
                command = f'ffmpeg -i "{m3u8_url}" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k "{save_path}"'
            else:  # 低质量 (最小体积)
                # 使用h264编码，低比特率
                command = f'ffmpeg -i "{m3u8_url}" -c:v libx264 -preset faster -crf 28 -c:a aac -b:a 96k "{save_path}"'
            
            # 执行命令
            subprocess.run(command, shell=True, check=True)
            
            is_downloading[0] = False
            root.after(0, lambda: messagebox.showinfo("成功", "视频下载完成！"))
        except subprocess.CalledProcessError:
            is_downloading[0] = False
            root.after(0, lambda: messagebox.showerror("错误", "下载视频失败。请确保已安装FFmpeg且链接正确。"))
        finally:
            # 恢复下载按钮状态
            root.after(0, lambda: download_button.config(state=tk.NORMAL))
    
    download_thread = threading.Thread(target=download_task)
    download_thread.daemon = True
    download_thread.start()

# 创建GUI窗口
root = tk.Tk()
root.title("M3U8视频下载器")

# 高DPI适配设置
try:
    # Windows系统下的高DPI适配
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
    # 设置缩放因子
    scale_factor = root.winfo_fpixels('1i') / 72
    root.tk.call('tk', 'scaling', scale_factor)
except Exception:
    pass

# 设置窗口大小和位置
window_width = 850
window_height = 380
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# 创建主框架并应用内边距
main_frame = tk.Frame(root, padx=25, pady=25)
main_frame.pack(fill=tk.BOTH, expand=True)

# 增大字体大小
FONT_SIZE = 24
BUTTON_FONT_SIZE = 26

# URL输入区域
url_label = tk.Label(main_frame, text="M3U8链接:", font=("SimHei", FONT_SIZE))
url_label.grid(row=0, column=0, sticky="w", pady=(0, 15))

url_entry = tk.Entry(main_frame, width=50, font=("SimHei", FONT_SIZE))
url_entry.grid(row=0, column=1, padx=10, pady=(0, 15), sticky="ew")
url_entry.insert(0, "https://example.com/video.m3u8?parse1=1&parse2=2etc")

# 视频质量选择
quality_label = tk.Label(main_frame, text="视频质量:", font=("SimHei", FONT_SIZE))
quality_label.grid(row=1, column=0, sticky="w", pady=(0, 15))

quality_var = tk.StringVar(value="中等质量 (较小体积)")
quality_options = ["高质量 (原始大小)", "中等质量 (较小体积)", "低质量 (最小体积)"]
quality_dropdown = ttk.Combobox(main_frame, textvariable=quality_var, 
                               values=quality_options, font=("SimHei", FONT_SIZE),
                               state="readonly", width=20)
quality_dropdown.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 15))
# 修复下拉列表的字体大小问题
root.option_add("*TCombobox*Listbox*Font", ("SimHei", FONT_SIZE))
# 尝试直接设置下拉列表样式
combostyle = ttk.Style()
combostyle.theme_create(
    "combostyle",
    parent="alt",
    settings={
        "TCombobox": {
            "configure": {
                "selectbackground": "#4a6984",
                "fieldbackground": "white",
                "background": "white",
                "foreground": "black",
                "arrowsize": 20,
                "font": ("SimHei", FONT_SIZE),
            }
        }
    },
)
combostyle.theme_use("combostyle")
# 状态标签
status_label = tk.Label(main_frame, text="", font=("SimHei", FONT_SIZE), fg="blue")
status_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 15))

# 下载按钮
download_button = tk.Button(main_frame, text="开始下载", command=download_video, 
                           font=("SimHei", BUTTON_FONT_SIZE, "bold"), 
                           bg="#4CAF50", fg="white", 
                           padx=15, pady=8)
download_button.grid(row=2, column=0, columnspan=2, pady=15)

# 调整列宽权重以便调整窗口大小时能正确伸缩
main_frame.columnconfigure(1, weight=1)

# 设置ttk样式以匹配更大的字体
style = ttk.Style()
style.configure("TCombobox", font=("SimHei", FONT_SIZE))
style.configure("TCombobox.Listbox", font=("SimHei", FONT_SIZE))

# 提示信息
tip_label = tk.Label(main_frame, text="提示: 视频质量越低，文件体积越小，下载和转换速度越快", 
                    font=("SimHei", FONT_SIZE-2), fg="gray")
tip_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(5, 0))

root.mainloop()
