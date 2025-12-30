import os
import re

# 配置路径
base_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(base_dir, "我的题解")
readme_path = os.path.join(base_dir, "README.md")

# 定义标记（注意：必须与 README 中的文本完全一致）
start_marker = "##  --- 我的题解 ---"
end_marker = "## --- 我的题解结束 ---"

def combine_markdowns():
    # 1. 获取所有 .md 文件及其创建时间
    if not os.path.exists(source_dir):
        print(f"错误：找不到目录 {source_dir}")
        return

    md_files = []
    for file in os.listdir(source_dir):
        if file.endswith(".md") and file != "README.md":
            file_path = os.path.join(source_dir, file)
            # 获取创建时间
            ctime = os.path.getctime(file_path)
            md_files.append((file_path, file, ctime))

    # 2. 按创建时间排序 (从旧到新)
    md_files.sort(key=lambda x: x[2])

    combined_content = []
    
    # 3. 读取内容并处理图片路径
    for file_path, file_name, _ in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 替换图片路径：将 ./assets/ 替换为 ./我的题解/assets/
                # 匹配 ![alt](./assets/name.png)
                # 使用 lambda 替换可以避免反斜杠转义问题
                def img_replace(match):
                    alt = match.group(1)
                    img_name = match.group(2)
                    return f"![{alt}](./我的题解/assets/{img_name})"

                new_content = re.sub(r'!\[(.*?)\]\(\./assets/(.*?)\)', img_replace, content)
                
                # 添加文件名作为二级标题，方便阅读
                header = f"\n---\n## 题解：{file_name.replace('.md', '')}\n\n"
                combined_content.append(header + new_content + "\n")
        except Exception as e:
            print(f"读取文件 {file_name} 出错: {e}")

    all_solutions_text = "\n".join(combined_content)

    # 4. 写入 README.md
    if not os.path.exists(readme_path):
        print("错误：未找到 README.md 文件")
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_data = f.read()

    # 5. 安全替换内容
    # 构建正则表达式模式，匹配两个标记位之间的内容
    pattern = re.escape(start_marker) + r"(.*?)" + re.escape(end_marker)
    
    # 定义一个内部函数来返回新内容，这样 re.sub 就不会处理文本里的反斜杠了
    def replacement_func(match):
        return f"{start_marker}\n{all_solutions_text}\n{end_marker}"

    if re.search(pattern, readme_data, re.DOTALL):
        # 使用 replacement_func 避开 "bad escape" 错误
        new_readme = re.sub(pattern, replacement_func, readme_data, flags=re.DOTALL)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_readme)
        print(f"成功完成！已合并 {len(md_files)} 个题解文件到 README.md")
    else:
        print("错误：在 README.md 中未找到指定的标记位，请检查标记是否完整。")

if __name__ == "__main__":
    combine_markdowns()