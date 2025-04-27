import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import requests
import tempfile
import shutil
from urllib.parse import urlparse, urljoin

class M3U8Downloader:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.is_downloading = False
        self.download_threads = []
        self.temp_dir = None
        self.total_segments = 0
        self.downloaded_segments = 0
        self.download_lock = threading.Lock()

    def setup_ui(self):
        # 配置窗口基本信息
        self.root.title("M3U8视频下载器")
        self.apply_hdpi_settings()
        self.setup_window_size()

        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=30, pady=30, bg="#f5f5f5")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 设置字体大小
        self.FONT_SIZE = 24
        self.BUTTON_FONT_SIZE = 26

        # 创建标题
        title_label = tk.Label(self.main_frame, text="M3U8视频下载器", 
                              font=("SimHei", self.FONT_SIZE + 8, "bold"),
                              fg="#2c3e50", bg="#f5f5f5", pady=15)
        title_label.grid(row=0, column=0, columnspan=2, sticky="w")

        # URL输入区域
        self.create_url_section()

        # 保存位置选择区域
        self.create_save_path_section()

        # 文件名输入区域
        self.create_filename_section()

        # 视频质量选择区域
        self.create_quality_section()

        # 线程数选择区域
        self.create_thread_section()

        # 进度条
        self.create_progress_section()

        # 下载按钮
        self.create_download_button()

        # 提示信息
        self.create_tip_section()

        # 调整列宽权重
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.configure(bg="#f5f5f5")

    def apply_hdpi_settings(self):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
            scale_factor = self.root.winfo_fpixels('1i') / 72
            self.root.tk.call('tk', 'scaling', scale_factor)
        except Exception:
            pass

    def setup_window_size(self):
        window_width = 900
        window_height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg="#f5f5f5")

    def create_url_section(self):
        url_label = tk.Label(self.main_frame, text="M3U8链接:", 
                            font=("SimHei", self.FONT_SIZE),
                            bg="#f5f5f5", fg="#2c3e50")
        url_label.grid(row=1, column=0, sticky="w", pady=(20, 15))

        url_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        url_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=(20, 15))
        url_frame.columnconfigure(0, weight=1)

        self.url_entry = tk.Entry(url_frame, width=50, 
                                font=("SimHei", self.FONT_SIZE),
                                relief=tk.SOLID, bd=1)
        self.url_entry.grid(row=0, column=0, sticky="ew")
        self.url_entry.insert(0, "https://example.com/video.m3u8")
        self.url_entry.bind("<FocusOut>", self.update_filename_from_url)

        # 为输入框添加时尚的样式
        self.url_entry.configure(highlightthickness=1, highlightbackground="#bdc3c7", highlightcolor="#3498db")

    def update_filename_from_url(self, event=None):
        url = self.url_entry.get().strip()
        if url and "example.com" not in url:  # 避免处理示例URL
            suggested_name = self.extract_filename_from_url(url)
            if suggested_name.endswith(".mp4"):
                suggested_name = suggested_name[:-4]  # 移除.mp4扩展名，因为UI中已有扩展名标签
            self.filename_var.set(suggested_name)

    def create_filename_section(self):
        """创建文件名输入区域"""
        filename_label = tk.Label(
            self.main_frame,
            text="文件名:",
            font=("SimHei", self.FONT_SIZE),
            bg="#f5f5f5",
            fg="#2c3e50",
        )
        
        filename_label.grid(row=3, column=0, sticky="w", pady=(0, 15))

        self.filename_var = tk.StringVar()

        filename_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        filename_frame.grid(row=3, column=1, sticky="ew", padx=10, pady=(0, 15))
        filename_frame.columnconfigure(0, weight=1)

        self.filename_entry = tk.Entry(
            filename_frame,
            textvariable=self.filename_var,
            font=("SimHei", self.FONT_SIZE),
            width=40,
            relief=tk.SOLID,
            bd=1,
        )
        self.filename_entry.grid(row=0, column=0, sticky="ew")
        self.filename_entry.configure(
            highlightthickness=1, highlightbackground="#bdc3c7", highlightcolor="#3498db"
        )

        # 添加.mp4扩展名标签
        ext_label = tk.Label(
            filename_frame,
            text=".mp4",
            font=("SimHei", self.FONT_SIZE),
            bg="#f5f5f5",
            fg="#7f8c8d",
        )
        ext_label.grid(row=0, column=1, padx=(5, 0))

    def create_save_path_section(self):
        save_path_label = tk.Label(self.main_frame, text="保存位置:", 
                                  font=("SimHei", self.FONT_SIZE),
                                  bg="#f5f5f5", fg="#2c3e50")
        save_path_label.grid(row=2, column=0, sticky="w", pady=(0, 15))

        self.save_path_var = tk.StringVar()
        self.save_path_var.set(os.path.join(os.path.expanduser("~"), "Videos"))

        save_path_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        save_path_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=(0, 15))
        save_path_frame.columnconfigure(0, weight=1)

        self.save_path_entry = tk.Entry(save_path_frame, textvariable=self.save_path_var, 
                                      font=("SimHei", self.FONT_SIZE),
                                      width=40, relief=tk.SOLID, bd=1)
        self.save_path_entry.grid(row=0, column=0, sticky="ew")
        self.save_path_entry.configure(highlightthickness=1, highlightbackground="#bdc3c7", highlightcolor="#3498db")

        browse_button = tk.Button(save_path_frame, text="浏览...", 
                                command=self.select_save_path,
                                font=("SimHei", self.FONT_SIZE-2), 
                                bg="#3498db", fg="white", 
                                padx=10, pady=3, 
                                relief=tk.RAISED, bd=0)
        browse_button.grid(row=0, column=1, padx=(5, 0))

        # 添加鼠标悬停效果
        browse_button.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
        browse_button.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))

    def create_quality_section(self):
        quality_label = tk.Label(self.main_frame, text="视频质量:", 
                                font=("SimHei", self.FONT_SIZE),
                                bg="#f5f5f5", fg="#2c3e50")
        quality_label.grid(row=4, column=0, sticky="w", pady=(0, 15))

        self.quality_var = tk.StringVar(value="中等质量 (较小体积)")
        quality_options = ["高质量 (原始大小)", "中等质量 (较小体积)", "低质量 (最小体积)"]

        # 创建一个容器框架
        quality_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        quality_frame.grid(row=4, column=1, sticky="w", padx=10, pady=(0, 15))

        # 使用下拉栏替代单选按钮
        quality_dropdown = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                        values=quality_options, 
                                        font=("SimHei", self.FONT_SIZE-2),
                                        state="readonly", width=25)
        quality_dropdown.grid(row=0, column=0, sticky="w")
        quality_dropdown.set("中等质量 (较小体积)")

        # 修复下拉列表的字体大小问题
        self.root.option_add("*TCombobox*Listbox*Font", ("SimHei", self.FONT_SIZE-2))

        # 设置下拉框样式
        style = ttk.Style()
        style.configure("TCombobox", 
                        foreground="#2c3e50",
                        background="#ffffff",
                        arrowsize=self.FONT_SIZE,
                        padding=5)

        # 确保下拉列表样式与主题一致
        style.map('TCombobox', 
                    fieldbackground=[('readonly', 'white')],
                    selectbackground=[('readonly', '#3498db')],
                    selectforeground=[('readonly', 'white')])

    def create_thread_section(self):
        thread_label = tk.Label(self.main_frame, text="下载线程:", 
                              font=("SimHei", self.FONT_SIZE),
                              bg="#f5f5f5", fg="#2c3e50")
        thread_label.grid(row=5, column=0, sticky="w", pady=(0, 15))

        thread_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        thread_frame.grid(row=5, column=1, sticky="w", padx=10, pady=(0, 15))

        self.thread_var = tk.IntVar(value=16)
        thread_scale = tk.Scale(thread_frame, from_=4, to=32, 
                              orient=tk.HORIZONTAL, length=300,
                              variable=self.thread_var, 
                              font=("SimHei", self.FONT_SIZE-5),
                              bg="#f5f5f5", fg="#2c3e50", 
                              highlightthickness=0, 
                              troughcolor="#bdc3c7", activebackground="#3498db")
        thread_scale.grid(row=0, column=0)

        thread_value = tk.Label(thread_frame, textvariable=self.thread_var, 
                              font=("SimHei", self.FONT_SIZE-2),
                              bg="#f5f5f5", fg="#2c3e50", width=3)
        thread_value.grid(row=0, column=1, padx=(10, 0))

    def create_progress_section(self):
        progress_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        progress_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 20))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, 
                                          length=100, mode="determinate", 
                                          variable=self.progress_var)
        self.progress_bar.grid(row=0, column=0, sticky="ew")

        self.progress_label = tk.Label(progress_frame, text="准备下载...", 
                                     font=("SimHei", self.FONT_SIZE-4),
                                     bg="#f5f5f5", fg="#2c3e50")
        self.progress_label.grid(row=1, column=0, sticky="w", pady=(5, 0))

        # 配置进度条样式
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Horizontal.TProgressbar", 
                      thickness=30, 
                      troughcolor="#f0f0f0",
                      background="#3498db",
                      borderwidth=0)

    def create_download_button(self):
        self.download_button = tk.Button(self.main_frame, text="开始下载", 
                                      command=self.start_download, 
                                      font=("SimHei", self.BUTTON_FONT_SIZE, "bold"), 
                                      bg="#2ecc71", fg="white", 
                                      padx=20, pady=10, 
                                      relief=tk.RAISED, bd=0)
        self.download_button.grid(row=7, column=0, columnspan=2, pady=10)

        # 添加鼠标悬停效果
        self.download_button.bind("<Enter>", lambda e: e.widget.config(bg="#27ae60"))
        self.download_button.bind("<Leave>", lambda e: e.widget.config(bg="#2ecc71"))

    def create_tip_section(self):
        tip_frame = tk.Frame(self.main_frame, bg="#e8f4f8", bd=1, relief=tk.SOLID)
        tip_frame.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(10, 0), padx=5)

        tip_icon = tk.Label(tip_frame, text="ℹ️", font=("SimHei", self.FONT_SIZE), 
                          bg="#e8f4f8", fg="#3498db", padx=10)
        tip_icon.grid(row=0, column=0, sticky="w")

        tip_label = tk.Label(tip_frame, 
                           text="提示: 1. 多线程加速下载  2. 视频质量越低，文件越小，速度越快  3. 确保已安装FFmpeg  4. 自动修复时间轴，保证与Whisper对齐",
                           font=("SimHei", self.FONT_SIZE-6), 
                           bg="#e8f4f8", fg="#34495e",
                           justify=tk.LEFT, wraplength=750, padx=5, pady=10)
        tip_label.grid(row=0, column=1, sticky="w")

    def select_save_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path_var.set(path)

    def start_download(self):
        if self.is_downloading:
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入M3U8链接地址")
            return
        
        save_dir = self.save_path_var.get().strip()
        if not save_dir:
            messagebox.showerror("错误", "请选择保存位置")
            return
        
        # 获取用户指定的文件名，如果为空则添加时间戳
        file_name = self.filename_var.get().strip()
        if not file_name:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{timestamp}_video"
        
        # 确保文件名有.mp4扩展名
        if not file_name.lower().endswith('.mp4'):
            file_name += '.mp4'
        
        save_path = os.path.join(save_dir, file_name)
        
        # 如果文件已存在，询问是否覆盖
        if os.path.exists(save_path):
            if not messagebox.askyesno("文件已存在", f"{file_name} 已存在，是否覆盖?"):
                return
        
        self.is_downloading = True
        self.download_button.config(state=tk.DISABLED, text="下载中...")
        
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        
        # 启动下载线程
        threading.Thread(target=self.download_m3u8, args=(url, save_path)).start()
    def extract_filename_from_url(self, url):
        try:
            # 尝试从URL中提取文件名
            parsed_url = urlparse(url)
            path = parsed_url.path

            # 尝试找到文件名
            match = re.search(r'([^/]+?)(?:\.m3u8|$)', path)
            if match and match.group(1):
                return f"{match.group(1)}.mp4"

            # 如果没有找到合适的文件名，使用domain作为文件名
            domain = parsed_url.netloc.replace(".", "_")
            return f"{domain}_video.mp4"
        except:
            # 出现任何异常，使用默认名称
            import datetime
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"video_{now}.mp4"

    def download_m3u8(self, url, save_path):
        try:
            # 获取M3U8内容
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                self.show_error(f"获取M3U8文件失败: HTTP {response.status_code}")
                return

            content = response.text

            # 检查是否是M3U8文件
            if "#EXTM3U" not in content:
                self.show_error("链接不是有效的M3U8文件")
                return

            # 解析M3U8，获取所有视频片段
            segments = []
            lines = content.splitlines()
            base_url = self.get_base_url(url)

            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # 构建完整的段URL
                if line.startswith("http"):
                    segment_url = line
                else:
                    segment_url = urljoin(base_url, line)

                segments.append(segment_url)

            if not segments:
                # 检查是否是主播放列表
                for line in lines:
                    if line.startswith("#EXT-X-STREAM-INF:"):
                        next_index = lines.index(line) + 1
                        if next_index < len(lines) and not lines[next_index].startswith("#"):
                            sublist_url = lines[next_index].strip()
                            if not sublist_url.startswith("http"):
                                sublist_url = urljoin(base_url, sublist_url)

                            # 递归下载子播放列表
                            self.update_progress("发现主播放列表，获取最高质量视频流...", 0)
                            self.download_m3u8(sublist_url, save_path)
                            return

                self.show_error("未找到视频片段")
                return

            self.total_segments = len(segments)
            self.downloaded_segments = 0

            # 更新UI显示总片段数
            self.update_progress(f"开始下载: 总共 {self.total_segments} 个片段", 0)

            # 创建下载文件的目录
            os.makedirs(os.path.join(self.temp_dir, "segments"), exist_ok=True)

            # 使用多线程下载片段
            num_threads = self.thread_var.get()
            segments_per_thread = max(1, len(segments) // num_threads)

            self.download_threads = []
            for i in range(0, len(segments), segments_per_thread):
                end_idx = min(i + segments_per_thread, len(segments))
                thread_segments = segments[i:end_idx]
                thread = threading.Thread(
                    target=self.download_segments,
                    args=(thread_segments, i)
                )
                self.download_threads.append(thread)
                thread.start()

            # 等待所有线程完成
            for thread in self.download_threads:
                thread.join()

            if not self.is_downloading:
                return  # 下载被取消
            old_method = False
            if old_method:
                # 合并所有片段
                self.update_progress("下载完成，正在合并视频片段...", 100)

                # 创建片段列表文件
                segments_file = os.path.join(self.temp_dir, "segments.txt")
                with open(segments_file, "w") as f:
                    for i in range(self.total_segments):
                        segment_path = os.path.join(self.temp_dir, "segments", f"{i}.ts")
                        if os.path.exists(segment_path):
                            f.write(f"file '{segment_path}'\n")

                # 使用FFmpeg合并片段并转码
                self.convert_video(segments_file, save_path)
            else:
                self.update_progress("下载完成，正在多线程合并视频片段...", 100)

                # 获取所有有效片段路径
                valid_segments = []
                for i in range(self.total_segments):
                    segment_path = os.path.join(self.temp_dir, "segments", f"{i}.ts")
                    if os.path.exists(segment_path):
                        valid_segments.append(segment_path)

                # 使用分治法多线程合并
                self.parallel_merge(valid_segments, save_path)

            # 删除临时文件
            self.cleanup()

            # 更新UI
            self.root.after(0, self.download_complete, save_path)

        except Exception as e:
            self.show_error(f"下载过程中发生错误: {str(e)}")

    def download_segments(self, segments, start_idx):
        for i, url in enumerate(segments):
            if not self.is_downloading:
                return  # 下载被取消

            segment_idx = start_idx + i
            segment_path = os.path.join(self.temp_dir, "segments", f"{segment_idx}.ts")

            # 添加重试机制
            retry_count = 0
            max_retries = 5
            download_success = False

            while retry_count < max_retries and not download_success:
                try:
                    response = requests.get(url, timeout=15)  # 增加超时时间
                    if response.status_code == 200:
                        with open(segment_path, "wb") as f:
                            f.write(response.content)
                        download_success = True
                    else:
                        retry_count += 1
                        if retry_count >= max_retries:
                            print(f"下载片段 {segment_idx} 失败: HTTP {response.status_code}，重试 {retry_count} 次后放弃")
                        else:
                            print(f"下载片段 {segment_idx} 失败: HTTP {response.status_code}，正在重试 ({retry_count}/{max_retries})...")
                            time.sleep(1)  # 重试前等待1秒
                except Exception as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f"下载片段 {segment_idx} 时发生错误: {str(e)}，重试 {retry_count} 次后放弃")
                    else:
                        print(f"下载片段 {segment_idx} 时发生错误: {str(e)}，正在重试 ({retry_count}/{max_retries})...")
                        time.sleep(2)  # 网络错误后等待2秒再重试

            # 更新进度
            if download_success:
                with self.download_lock:
                    self.downloaded_segments += 1
                    # 记录失败的片段
                    if not hasattr(self, 'failed_segments'):
                        self.failed_segments = []
                    
                    progress = (self.downloaded_segments / self.total_segments) * 100
                    self.update_progress(
                        f"下载中: {self.downloaded_segments}/{self.total_segments} 片段", 
                        progress
                    )
            else:
                # 记录失败的片段
                with self.download_lock:
                    if not hasattr(self, 'failed_segments'):
                        self.failed_segments = []
                    self.failed_segments.append(segment_idx)

    def parallel_merge(self, segments, final_output):
        """使用分治法多线程合并视频片段"""
        print("上述片段已下载完成，正在合并...")
        self.update_progress("正在合并视频片段...", 0)
        print("等待3s后开始合并...")
        time.sleep(3)
        try:
            # 如果片段数量太少，直接合并
            if len(segments) <= 8:
                self.direct_merge(segments, final_output, apply_quality_settings=True)
                return

            # 创建中间文件存储目录
            intermediate_dir = os.path.join(self.temp_dir, "intermediate")
            os.makedirs(intermediate_dir, exist_ok=True)

            # 确定第一层合并的分组大小和数量
            # 每组不超过8个片段，以便快速合并
            max_group_size = 16
            groups = []
            for i in range(0, len(segments), max_group_size):
                end = min(i + max_group_size, len(segments))
                groups.append(segments[i:end])

            self.update_progress(f"第1阶段: 并行合并 {len(groups)} 个片段组...", 100)

            # 递归合并，每层减少8倍文件数量
            level = 1
            current_segments = segments

            while len(current_segments) > max_group_size:
                # 分组并行处理
                groups = []
                for i in range(0, len(current_segments), max_group_size):
                    end = min(i + max_group_size, len(current_segments))
                    groups.append(current_segments[i:end])

                next_level_segments = []
                merge_threads = []

                # 创建并启动合并线程
                for i, group in enumerate(groups):
                    output_file = os.path.join(intermediate_dir, f"level_{level}_group_{i}.ts")
                    next_level_segments.append(output_file)

                    thread = threading.Thread(
                        target=self._safe_merge_group,
                        args=(group, output_file, False)  # 中间阶段不应用质量设置，只复制
                    )
                    merge_threads.append(thread)
                    thread.start()

                # 等待所有线程完成
                for thread in merge_threads:
                    thread.join()

                # 准备下一层
                current_segments = [f for f in next_level_segments if os.path.exists(f) and os.path.getsize(f) > 0]
                if not current_segments:
                    raise Exception(f"第{level}层合并失败，没有生成有效的中间文件")

                level += 1
                self.update_progress(f"第{level}阶段: 合并 {len(current_segments)} 个中间文件...", 100)

            # 最终合并并应用质量设置
            self.update_progress(f"最终合并并转码...", 100)
            self._safe_merge_group(current_segments, final_output, True)  # 最终阶段应用质量设置

        except Exception as e:
            self.show_error(f"并行合并视频时发生错误: {str(e)}")

    def _safe_merge_group(self, segments, output_path, apply_quality_settings=False):
        """安全地合并一组片段，处理路径问题"""
        try:
            # 创建临时片段列表文件
            list_file = os.path.join(self.temp_dir, f"list_{threading.get_ident()}_{int(time.time()*1000)}.txt")
            with open(list_file, "w", encoding="utf-8") as f:
                for segment in segments:
                    # 使用正斜杠避免Windows路径问题
                    clean_path = segment.replace('\\', '/')
                    f.write(f"file '{clean_path}'\n")

            # 确定是否应用质量设置或仅复制
            if apply_quality_settings:
                quality = self.quality_var.get()
                if quality == "高质量 (原始大小)":
                    command = [
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
                        "-i", list_file, "-c", "copy", output_path
                    ]
                elif quality == "中等质量 (较小体积)":
                    command = [
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
                        "-i", list_file, "-c:v", "libx264", 
                        "-preset", "medium", "-crf", "23", 
                        "-c:a", "aac", "-b:a", "128k", output_path
                    ]
                else:  # 低质量
                    command = [
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
                        "-i", list_file, "-c:v", "libx264", 
                        "-preset", "faster", "-crf", "28", 
                        "-c:a", "aac", "-b:a", "96k", output_path
                    ]
            else:
                # 中间阶段只复制，不转码
                command = [
                    "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
                    "-i", list_file, "-c", "copy", output_path
                ]

            # 执行命令
            subprocess.run(command, check=True)

            # 删除临时列表文件
            if os.path.exists(list_file):
                os.remove(list_file)

        except Exception as e:
            print(f"合并片段组时出错: {str(e)}")
            # 记录错误但不阻止其他线程

    def direct_merge(self, segment_files, output_path, apply_quality_settings=True):
        """直接合并片段列表到输出文件"""
        self._safe_merge_group(segment_files, output_path, apply_quality_settings)

    def convert_video(self, segments_file, output_path):
        try:
            quality = self.quality_var.get()

            # 根据所选质量设置生成FFmpeg命令
            if quality == "高质量 (原始大小)":
                command = [
                    "ffmpeg", "-f", "concat", "-safe", "0", 
                    "-i", segments_file, "-c", "copy", output_path
                ]
            elif quality == "中等质量 (较小体积)":
                command = [
                    "ffmpeg", "-f", "concat", "-safe", "0", 
                    "-i", segments_file, "-c:v", "libx264", 
                    "-preset", "medium", "-crf", "23", 
                    "-c:a", "aac", "-b:a", "128k", output_path
                ]
            else:  # 低质量
                command = [
                    "ffmpeg", "-f", "concat", "-safe", "0", 
                    "-i", segments_file, "-c:v", "libx264", 
                    "-preset", "faster", "-crf", "28", 
                    "-c:a", "aac", "-b:a", "96k", output_path
                ]

            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            self.show_error(f"视频合并失败: {str(e)}")
        except Exception as e:
            self.show_error(f"视频合并时发生错误: {str(e)}")

    def convert_video(self, segments_file, output_path):
        try:
            quality = self.quality_var.get()

            # 基础命令，添加时间轴修正参数
            base_cmd = [
                "ffmpeg", "-f", "concat", "-safe", "0", 
                "-i", segments_file,
                "-copyts", "-start_at_zero", "-reset_timestamps", "1"  # 修复时间轴
            ]

            # 根据所选质量设置生成FFmpeg命令
            if quality == "高质量 (原始大小)":
                command = base_cmd + ["-c", "copy", output_path]
            elif quality == "中等质量 (较小体积)":
                command = base_cmd + [
                    "-c:v", "libx264", 
                    "-preset", "medium", "-crf", "23", 
                    "-c:a", "aac", "-b:a", "128k",
                    "-af", "asetpts=PTS-STARTPTS",  # 确保音频时间轴从0开始
                    output_path
                ]
            else:  # 低质量
                command = base_cmd + [
                    "-c:v", "libx264", 
                    "-preset", "faster", "-crf", "28", 
                    "-c:a", "aac", "-b:a", "96k",
                    "-af", "asetpts=PTS-STARTPTS",  # 确保音频时间轴从0开始
                    output_path
                ]

            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            self.show_error(f"视频合并失败: {str(e)}")
        except Exception as e:
            self.show_error(f"视频合并时发生错误: {str(e)}")

    def get_base_url(self, url):
        parsed = urlparse(url)
        path_parts = parsed.path.rsplit('/', 1)
        if len(path_parts) > 1:
            base_path = path_parts[0] + '/'
        else:
            base_path = '/'

        return f"{parsed.scheme}://{parsed.netloc}{base_path}"

    def update_progress(self, text, value):
        self.root.after(0, lambda: self._update_progress_ui(text, value))

    def _update_progress_ui(self, text, value):
        self.progress_label.config(text=text)
        self.progress_var.set(value)

    def show_error(self, message):
        self.root.after(0, lambda: self._show_error_ui(message))

    def _show_error_ui(self, message):
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL, text="开始下载")
        self.cleanup()
        messagebox.showerror("错误", message)

    def download_complete(self, save_path):
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL, text="开始下载")
        messagebox.showinfo("下载完成", f"视频已成功下载到:\n{save_path}")
        self.progress_var.set(0)
        self.progress_label.config(text="准备下载...")

    def cleanup(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = M3U8Downloader(root)
    root.mainloop()
