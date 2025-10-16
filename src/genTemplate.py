
import codecs, os, re


appTemplateRoot: str = "../../cpp/cppAppTemplate/"

listFile: list[str] = {
	os.path.join(appTemplateRoot, ".vscode/launch.json"),
	os.path.join(appTemplateRoot, ".vscode/settings.json"),
	os.path.join(appTemplateRoot, "src/cppAppTemplate.cpp"),
	os.path.join(appTemplateRoot, "src/cppAppTemplate.h"),
	os.path.join(appTemplateRoot, "src/src.cmake"),
	os.path.join(appTemplateRoot, ".clang-format"),
	os.path.join(appTemplateRoot, ".clangd"),
	os.path.join(appTemplateRoot, ".gitignore"),
	os.path.join(appTemplateRoot, "CMakeLists.txt"),
	os.path.join(appTemplateRoot, "main.cpp"),
}

strFormat = """
{}: str = '''
{}
'''
"""

listFormat: str = """
{}: list[str] = [{}]
"""

strFileInfoFormat: str = """
{}: dict[str, str] = {{
{}
}}
"""

# "路径": ""
strFileInfo: str = ""
# "文件夹名称": ""
dictDirInfo: dict[str: str] = {}
with codecs.open('src/res.py', 'w', 'utf-8') as fw:

	i: int = 0
	for n in listFile:
		v: str = f"txt_{i}"
		i += 1
		with codecs.open(n, "r", 'utf-8') as f:
			s = f.read()
			s = s.replace('\\', "\\\\")
			if os.path.splitext(n)[1] in [".h", ".hpp", ".cpp", ".c", ".cxx", ".json"]:
				s = re.sub(r'//[^-].*', '', s)
			else:
				s = re.sub(r'#[^-].*', '', s)
			s = re.sub(r'^ +$\n', '', s, flags=re.MULTILINE)
			s = re.sub(r'\n{3,}', '\n\n', s, flags=re.MULTILINE)
			fw.write(strFormat.format(v, s))
		
		strFileInfo += f"""\t"{n[len(appTemplateRoot):]}": {v},\n"""
		dirName = os.path.dirname(n[len(appTemplateRoot):])
		if "" != dirName:
			dictDirInfo[dirName] = ""


	fw.write(listFormat.format("listDirs", ', '.join([f'"{n}"' for n in dictDirInfo.keys()])))
	fw.write(strFileInfoFormat.format("fileInfo", strFileInfo))
