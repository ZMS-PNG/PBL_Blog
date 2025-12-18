"""
Gunicorn 配置文件
Gunicorn Configuration File

用于生产环境部署的 Gunicorn WSGI 服务器配置
"""
import multiprocessing
import os

# 服务器绑定地址
bind = os.getenv('GUNICORN_BIND', '127.0.0.1:8000')

# 工作进程数（推荐：CPU核心数 * 2 + 1）
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# 工作模式
# sync: 同步工作模式（默认）
# gevent: 异步工作模式（需要安装 gevent）
# eventlet: 异步工作模式（需要安装 eventlet）
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')

# 每个工作进程的线程数
threads = int(os.getenv('GUNICORN_THREADS', 1))

# 工作进程超时时间（秒）
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))

# 优雅重启超时时间（秒）
graceful_timeout = int(os.getenv('GUNICORN_GRACEFUL_TIMEOUT', 30))

# 保持连接时间（秒）
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 5))

# 最大请求数（防止内存泄漏）
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 50))

# 日志配置
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '/var/log/blog-system/gunicorn-access.log')
errorlog = os.getenv('GUNICORN_ERROR_LOG', '/var/log/blog-system/gunicorn-error.log')
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')

# 访问日志格式
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程名称
proc_name = 'blog-system'

# 守护进程模式（systemd 管理时应设为 False）
daemon = False

# 进程 PID 文件
pidfile = os.getenv('GUNICORN_PID_FILE', '/var/run/blog-system/gunicorn.pid')

# 用户和组（如果以 root 启动，会切换到此用户）
# user = 'www-data'
# group = 'www-data'

# 临时目录
# tmp_upload_dir = '/tmp'

# 预加载应用（可以减少内存使用，但重启时会中断服务）
preload_app = False

# 工作进程重启前的最大请求数
# worker_connections = 1000

# SSL 配置（如果需要）
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# 回调函数
def on_starting(server):
    """服务器启动时的回调"""
    print("Gunicorn server is starting...")

def on_reload(server):
    """服务器重载时的回调"""
    print("Gunicorn server is reloading...")

def when_ready(server):
    """服务器准备就绪时的回调"""
    print("Gunicorn server is ready. Spawning workers...")

def pre_fork(server, worker):
    """工作进程 fork 前的回调"""
    pass

def post_fork(server, worker):
    """工作进程 fork 后的回调"""
    print(f"Worker spawned (pid: {worker.pid})")

def pre_exec(server):
    """执行前的回调"""
    print("Forked child, re-executing.")

def worker_int(worker):
    """工作进程接收到 INT 或 QUIT 信号时的回调"""
    print(f"Worker received INT or QUIT signal (pid: {worker.pid})")

def worker_abort(worker):
    """工作进程异常退出时的回调"""
    print(f"Worker received SIGABRT signal (pid: {worker.pid})")
