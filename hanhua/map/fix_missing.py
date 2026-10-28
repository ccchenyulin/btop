#!/usr/bin/env python3
"""补齐 btop 汉化的 15 处漏译（2026-10-25 检查发现）

漏译来源分类：
  1. 信号/优先级对话框的"| 说明"修饰（6 条）—— 用 Locale::get() 包起来 + 加词典
  2. 帮助页 1 条（Expand/collapse the selected process' children.）
  3. 配置说明 2 条（Aggregate child's resources / Prepend exclude=）
  4. 信号操作错误 4 条（Unsupported signal! 等）
  5. 终端太小 2 条
  6. CLI 1 条（v1.4.8 新增）

策略：
  - A 类：已经用 Locale::get(desc) 的，只需补词典条目 → 加进 btop_locale.cpp
  - B 类：硬编码的，需要包 Locale::get() + 加词典
"""
import re
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENU = os.path.join(REPO, 'src/btop_menu.cpp')
LOCALE = os.path.join(REPO, 'src/btop_locale.cpp')
CLI = os.path.join(REPO, 'src/btop_cli.cpp')

# ============ 词典条目（英文 key → 中文）============
NEW_ENTRIES = {
    # 组1：信号/优先级对话框修饰
    " | To choose signal.": " | 选择信号",
    " | Enter manually.": " | 手动输入",
    " | To send signal.": " | 发送信号",
    " | To change value.": " | 调整数值",
    " | To change value by 5.": " | 数值 ±5",
    " | To set nice value.": " | 设定 nice 值",
    # 组2：帮助页
    "Expand/collapse the selected process' children.": "展开/折叠所选进程的子进程。",
    # 组3：配置说明
    "Aggregate child's resources in parent.": "把子进程的资源计入父进程。",
    "Prepend \\033[3mexclude=\\033[23m to only show disks ": "在开头加 \\033[3mexclude=\\033[23m 可只显示磁盘 ",
    # 组4：信号错误
    "Unsupported signal!": "不支持的信号！",
    "Insufficient permissions to send signal!": "权限不足，无法发送信号！",
    "Process not found!": "进程不存在！",
    "Unknown error! (errno: ": "未知错误！（errno: ",
    # 组5：终端太小
    "Terminal size too small to": "终端尺寸太小，无法",
    "display menu or box!": "显示菜单或面板！",
    # 组6：CLI
    "Config file can't be a directory": "配置文件不能是目录",
    # 组7：对话框标题与输入提示（2026-10-25 二次检查发现）
    "Send signal to PID ": "向 PID 发送信号 ",
    "Renice PID ": "调整优先级 PID ",
    "Enter signal number: ": "输入信号编号：",
    "Enter nice value: ": "输入 nice 值：",
}

# ============ 需要「包 Locale::get()」的硬编码处 ============
# (文件, 原文本, 新文本)
WRAP_CHANGES = [
    # 组1：信号/优先级对话框（这些是 out += ... + " | xxx." 形式）
    (MENU,
     'Theme::c("main_fg") + Fx::ub + " | To choose signal.";',
     'Theme::c("main_fg") + Fx::ub + Locale::get(" | To choose signal.");'),
    (MENU,
     'Theme::c("main_fg") + Fx::ub + " | Enter manually.";',
     'Theme::c("main_fg") + Fx::ub + Locale::get(" | Enter manually.");', 2),
    (MENU,
     'Theme::c("main_fg") + Fx::ub + " | To send signal.";',
     'Theme::c("main_fg") + Fx::ub + Locale::get(" | To send signal.");'),
    (MENU,
     'Theme::c("main_fg") + Fx::ub + " | To change value.";',
     'Theme::c("main_fg") + Fx::ub + Locale::get(" | To change value.");'),
    (MENU,
     'Theme::c("main_fg") + Fx::ub + " | To change value by 5.";',
     'Theme::c("main_fg") + Fx::ub + Locale::get(" | To change value by 5.");'),
    (MENU,
     'Theme::c("main_fg") + Fx::ub + " | To set nice value.";',
     'Theme::c("main_fg") + Fx::ub + Locale::get(" | To set nice value.");'),
    # 组4：信号错误
    (MENU,
     'cont_vec.push_back("Unsupported signal!" + Fx::reset);',
     'cont_vec.push_back(Locale::get("Unsupported signal!") + Fx::reset);'),
    (MENU,
     'cont_vec.push_back("Insufficient permissions to send signal!" + Fx::reset);',
     'cont_vec.push_back(Locale::get("Insufficient permissions to send signal!") + Fx::reset);'),
    (MENU,
     'cont_vec.push_back("Process not found!" + Fx::reset);',
     'cont_vec.push_back(Locale::get("Process not found!") + Fx::reset);'),
    (MENU,
     'cont_vec.push_back("Unknown error! (errno: " + to_string(signalKillRet) + \')\' + Fx::reset);',
     'cont_vec.push_back(Locale::get("Unknown error! (errno: ") + to_string(signalKillRet) + \')\' + Fx::reset);'),
    # 组5：终端太小
    (MENU,
     '"Terminal size too small to" + Fx::reset,',
     'Locale::get("Terminal size too small to") + Fx::reset,'),
    (MENU,
     '"display menu or box!" + Fx::reset };',
     'Locale::get("display menu or box!") + Fx::reset };'),
    # 组6：CLI
    (CLI,
     'error("Config file can\'t be a directory");',
     'error(Locale::get("Config file can\'t be a directory"));'),
    # 组7：对话框标题与输入提示
    (MENU,
     'cjust("Send signal to PID " + to_string(s_pid.value())',
     'cjust(Locale::get("Send signal to PID ") + to_string(s_pid.value())'),
    (MENU,
     'cjust("Renice PID " + to_string(s_pid.value())',
     'cjust(Locale::get("Renice PID ") + to_string(s_pid.value())'),
    (MENU,
     'rjust("Enter signal number: ", 48)',
     'rjust(Locale::get("Enter signal number: "), 48, true)'),
    (MENU,
     'rjust("Enter nice value: ", 30)',
     'rjust(Locale::get("Enter nice value: "), 30, true)'),
]


def add_dict_entries(dry=True):
    """在 btop_locale.cpp 的加载函数末尾追加新条目"""
    s = open(LOCALE, encoding='utf-8').read()

    # 找出还没有的条目
    todo = {k: v for k, v in NEW_ENTRIES.items()
            if f'translations["{k}"]' not in s}
    if not todo:
        print("  ✅ 词典条目已全部存在")
        return 0

    # 在 load 函数结束前插入（找最后一个 translations[...] = ...; 之后）
    lines = s.split('\n')
    last = -1
    for i, ln in enumerate(lines):
        if re.match(r'\s*translations\[".*"\] = ', ln):
            last = i
    assert last >= 0, "找不到词典条目插入点"

    # 处理多行条目的结尾（找该条目的分号行）
    while last < len(lines) and not lines[last].rstrip().endswith(';'):
        last += 1

    ins = ['',
           '\t//* 2026-10-25 补齐的漏译条目（对话框修饰/帮助页/配置说明/错误消息）']
    for k, v in todo.items():
        # 转义
        ke = k.replace('\\', '\\\\').replace('"', '\\"')
        ve = v.replace('\\', '\\\\').replace('"', '\\"')
        ins.append(f'\ttranslations["{ke}"] = "{ve}";')

    lines[last + 1:last + 1] = ins
    if not dry:
        open(LOCALE, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f"  {'[DRY] ' if dry else ''}词典新增 {len(todo)} 条")
    for k in todo:
        print(f"    {k!r}")
    return len(todo)


def apply_wraps(dry=True):
    """给硬编码处包 Locale::get()"""
    n = 0
    cache = {}
    for item in WRAP_CHANGES:
        path, old, new = item[0], item[1], item[2]
        expect = item[3] if len(item) > 3 else 1
        if path not in cache:
            cache[path] = open(path, encoding='utf-8').read()
        s = cache[path]
        c = s.count(old)
        if c == expect:
            cache[path] = s.replace(old, new)
            n += c
            print(f"  ✅ {os.path.basename(path)} ({c} 处): {old[:50]}...")
        elif c == 0:
            print(f"  ⚠️ 未匹配: {old[:55]}...")
        else:
            print(f"  ⚠️ 匹配 {c} 处（期望 {expect}）: {old[:50]}...")
    if not dry:
        for path, content in cache.items():
            open(path, 'w', encoding='utf-8').write(content)
    return n


def main():
    dry = '--apply' not in sys.argv
    print(f"{'=== DRY-RUN ===' if dry else '=== APPLY ==='}\n")
    print("[1] 补词典条目")
    a = add_dict_entries(dry)
    print("\n[2] 硬编码处包 Locale::get()")
    b = apply_wraps(dry)
    print(f"\n合计：词典 {a} 条 + 包裹 {b} 处")
    if dry:
        print("\n加 --apply 才会写盘")


if __name__ == '__main__':
    main()
