
txt_0: str = '''
{
	
	"[h]": {
		"editor.formatOnSave": true,
		"editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd"
	},
	"[hpp]": {
		"editor.formatOnSave": true,
		"editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd"
	},
	"[cpp]": {
		"editor.formatOnSave": true,
		"editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd"
	},
	"[c]": {
		"editor.formatOnSave": true,
		"editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd"
	},
	"[cxx]": {
		"editor.formatOnSave": true,
		"editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd"
	},
}
'''

txt_1: str = '''
#ifndef __H_CPPAPPTEMPLATE_H__
#define __H_CPPAPPTEMPLATE_H__

class CppAppTemplate
{
public:
	CppAppTemplate();
	virtual ~CppAppTemplate();

public:
	virtual bool init();
};

#endif //- __H_CPPAPPTEMPLATE_H__

'''

txt_2: str = '''
#- set(CMAKE_CXX_COMPILER /usr/local/bin/g++)
#- set(CMAKE_C_COMPILER /usr/local/bin/gcc)

cmake_minimum_required(VERSION 3.10)

project(cppAppTemplate)

if(DEFINED ENV{MSYSTEM})
    message(STATUS "Detected MSYS2 environment: $ENV{MSYSTEM}")
    set(IS_MSYS2 TRUE)
else()
    set(IS_MSYS2 FALSE)
endif()

if(IS_MSYS2)
    file(WRITE "${CMAKE_BINARY_DIR}/.fix_compile_json.cmake" [=[
        file(READ "${CMAKE_BINARY_DIR}/compile_commands.json" content)
        string(REGEX MATCH "([A-Za-z]):/" DriveMatch "${content}")
        string(REGEX REPLACE "^([A-Za-z]):/.*" "\\\\1" DriveMatch "${DriveMatch}")
        string(TOLOWER "${DriveMatch}" DriveMatch)
        string(REGEX REPLACE "\\"file\\": \\"([A-Z]):/" "\\"file\\": \\"/${DriveMatch}/" content "${content}")
        file(WRITE "${CMAKE_BINARY_DIR}/compile_commands.json" "${content}")
        message("Fix compile_commands.json paths for unix format")
    ]=])
    execute_process(COMMAND ${CMAKE_COMMAND} -P "${CMAKE_BINARY_DIR}/.fix_compile_json.cmake")

    add_custom_target(
        .fix_compile_json_paths ALL
        COMMAND ${CMAKE_COMMAND} -P "${CMAKE_BINARY_DIR}/.fix_compile_json.cmake"
        BYPRODUCTS "${CMAKE_BINARY_DIR}/compile_commands.json"
        COMMENT "Fixing paths in compile_commands.json for MSYS2/Unix format..."
    )
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

message("CMAKE_BUILD_TYPE:=" ${CMAKE_BUILD_TYPE})

set(CMAKE_CXX_FLAGS "-W -Wall")
set(CMAKE_CXX_FLAGS_RELEASE "-O2  -static")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g -ggdb -D__H_DEBUT__")

set(LIB_FILES "")						#- 链接库名称
set(SRC_LISTS "")						#- 源文件路径
set(LIB_FILE_DIRS "")					#- 库文件路径
set(HEAD_FILE_DIRS "")					#- 头文件路径
set(DEFINE_MACROS "")					#- 添加宏
set(ADD_SHARED_DIRS "")					#- 添加共享路径
set(ADD_SUBDIRECTORIES_ "")				#- 添加子项目路径
set(OUT_FILE_NAME ${PROJECT_NAME})

include(CheckCXXCompilerFlag)

CHECK_CXX_COMPILER_FLAG("-std=c++20" COMPILER_SUPPORTS_CXX20)
CHECK_CXX_COMPILER_FLAG("-std=c++20" COMPILER_SUPPORTS_CXX17)
CHECK_CXX_COMPILER_FLAG("-std=c++17" COMPILER_SUPPORTS_CXX17)
CHECK_CXX_COMPILER_FLAG("-std=c++14" COMPILER_SUPPORTS_CXX14)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX20)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++20")
elseif(COMPILER_SUPPORTS_CXX17)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
elseif(COMPILER_SUPPORTS_CXX14)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")
elseif(COMPILER_SUPPORTS_CXX11)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
	message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++0x or C++11 or c++14 or c++17 support. Please use a different C++ compiler.")
endif()

include(src/src.cmake)

set(RELATIVE_SRC_LISTS "")
foreach(path_ IN LISTS SRC_LISTS)
    cmake_path(RELATIVE_PATH path_ BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" OUTPUT_VARIABLE rel)
    list(APPEND RELATIVE_SRC_LISTS "${rel}")
endforeach(path_)
message(STATUS "Building sources: ${RELATIVE_SRC_LISTS}")

foreach(path_ ${ADD_SUBDIRECTORIES_})
	add_subdirectory(${path_})
Endforeach(path_)

foreach(macro ${DEFINE_MACROS})
	add_definitions(-D${macro})
Endforeach(macro)

add_executable(${OUT_FILE_NAME} ${RELATIVE_SRC_LISTS} "main.cpp")

foreach(path ${ADD_SHARED_DIRS})
	target_link_libraries(${OUT_FILE_NAME} "-Wl,-rpath=${path}")
Endforeach(path)

target_link_libraries(${OUT_FILE_NAME} ${LIB_FILES})


'''

txt_3: str = '''
{
    "version": "0.2.0",
    "configurations": [
        //- GDB Debugger - Beyond
        {
            "name": "beyond",
            "type": "by-gdb",
            "request": "launch",
            "program": "${command:cmake.launchTargetPath}", //- 执行文件由 cmake 提供
            "cwd": "${workspaceRoot}",
            "programArgs": "",
        },
        //- C/C++ Debug (gdb)
        {
            "name": "cppdbg",
            "type": "cppdbg",
            "request": "launch",
            "program": "${command:cmake.launchTargetPath}", //- 执行文件由 cmake 提供
            "args": [],
            "stopAtEntry": true,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        },
        //- //- Native Debug
        //- {
        //-     "name": "Native",
        //-     "type": "gdb",
        //-     "request": "launch",
        //-     "target": "${command:cmake.launchTargetPath}", 
        //-     "cwd": "${workspaceRoot}",
        //-     "valuesFormatting": "parseText",
        //-     
        //-     
        //-     
        //- },
        //- //- CodeLLDB
        //- {
        //-     "name": "CodeLLDB",
        //-     "type": "lldb",
        //-     "request": "launch",
        //-     "program": "${command:cmake.launchTargetPath}", 
        //-     "args": [],
        //-     "cwd": "${workspaceFolder}",
        //-     
        //-     "sourceLanguages": [
        //-         "c",
        //-         "cpp"
        //-     ],
        //-     "console": "integratedTerminal"
        //- }
    ]
}
'''

txt_4: str = '''
build/
.cache/


'''

txt_5: str = '''

#- include(${CMAKE_CURRENT_LIST_DIR}/<目录名/*.cmake>)

file(GLOB_RECURSE HEAD_H_FILES "${CMAKE_CURRENT_LIST_DIR}/*.h")
file(GLOB_RECURSE HEAD__HPP_FILES "${CMAKE_CURRENT_LIST_DIR}/*.hpp")
file(GLOB_RECURSE SOURCE_C_FILES "${CMAKE_CURRENT_LIST_DIR}/*.c")
file(GLOB_RECURSE SOURCE_CC_FILES "${CMAKE_CURRENT_LIST_DIR}/*.cc")
file(GLOB_RECURSE SOURCE_CPP_FILES "${CMAKE_CURRENT_LIST_DIR}/*.cpp")
file(GLOB_RECURSE SOURCE_CXX_FILES "${CMAKE_CURRENT_LIST_DIR}/*.cxx")

set(SRC_LISTS
	${SRC_LISTS}
	${HEAD_H_FILES}
	${HEAD__HPP_FILES}
	${SOURCE_C_FILES}
	${SOURCE_CC_FILES}
	${SOURCE_CPP_FILES}
	${SOURCE_CXX_FILES}
	#- 添加源文件，文件路径名字或变量
	)

set(LIB_FILES
	${LIB_FILES}
	#- 添加lib库
	)

set(LIB_FILE_DIRS
	${LIB_FILE_DIRS}
	#- 添加lib库搜索路径
	)

set(HEAD_FILE_DIRS
	${HEAD_FILE_DIRS}
	#- 添加头文件搜索路径
	)

set(DEFINE_MACROS
	${DEFINE_MACROS}
	#- 为程序定义全局宏，
	#- 只定义宏：__H_DEBUT__
	#- 定义宏且给值 __H_DEBUT__="aa"(字符串) __H_DEBUT__=1(数字)
	#-
	#- 项目
	__APP_NAME__="${PROJECT_NAME}"
	)	

set(ADD_SHARED_DIRS
	${ADD_SHARED_DIRS}
	#- 添加共享库路径
	)

set(ADD_SUBDIRECTORIES_
	${ADD_SUBDIRECTORIES_}
	#- 添加子项目路径
	)

#- 设置编译器参数(在引号中添加)
set(CMAKE_CXX_FLAGS
	"${CMAKE_CXX_FLAGS} -Wall -W"
	)
set(CMAKE_CXX_FLAGS_DEBUG
	"${CMAKE_CXX_FLAGS_DEBUG} -O0 -g -D__H_DEBUT__"
	)
set(CMAKE_CXX_FLAGS_RELEASE
	"${CMAKE_CXX_FLAGS_RELEASE} -O2"
	)
'''

txt_6: str = '''
#include "cppAppTemplate.h"

#include <iostream>

CppAppTemplate::CppAppTemplate()
{}

CppAppTemplate::~CppAppTemplate()
{}

bool CppAppTemplate::init()
{
	std::cout << __PRETTY_FUNCTION__ << '\\n';

	return true;
}

'''

txt_7: str = '''


BasedOnStyle: LLVM

UseTab: Always

IndentWidth: 4

TabWidth: 4

IndentAccessModifiers: false

AccessModifierOffset: -4

AlignAfterOpenBracket: DontAlign

MaxEmptyLinesToKeep: 2

BreakBeforeBraces: Custom
BraceWrapping:
  AfterClass: true
  AfterStruct: true
  AfterEnum: true
  AfterNamespace: true
  AfterFunction: true
  AfterControlStatement: false
  AfterExternBlock: true
  BeforeCatch: false
  BeforeElse: false
  SplitEmptyFunction: false

AlignConsecutiveDeclarations: true

AlignConsecutiveAssignments: true

AllowShortFunctionsOnASingleLine: None

SortIncludes: true

IncludeIsMainRegex: '([-_](test|unittest))?$'

IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^<[^/]+.h>'
    Priority: 1
    SortPriority: 0
  - Regex: '^<[^>]+[^.h]{2}>$'
    Priority: 2
    SortPriority: 0
  - Regex: '^<[^>]+/+.+>'
    Priority: 3
    SortPriority: 0
  - Regex: '^"'
    Priority: 4
    SortPriority: 0

'''

txt_8: str = '''
#include <iostream>
#include <memory>

#include "src/cppAppTemplate.h"

int main()
{
#if __H_DEBUT__
	std::cout << "run debug version"
			  << std::endl; 
#endif

	auto ptr = std::make_shared<CppAppTemplate>();
	if (!ptr->init()) {
		return -1;
	}

	std::cout << "create " << __APP_NAME__ << " success" << '\\n';

	return 0;
}

'''

txt_9: str = '''
Diagnostics:
  UnusedIncludes: Strict
  ClangTidy: 
    Add:  
      - modernize-*
      - performance-*
      - bugprone-*
      - cppcoreguidelines-*
      - cert-*
      - readability-identifier-naming
      - readability-braces-around-statements

    Remove: 
      - modernize-use-trailing-return-type
      - bugprone-easily-swappable-parameters
      - cppcoreguidelines-special-member-functions
      - cppcoreguidelines-avoid-magic-numbers
      - cppcoreguidelines-owning-memory
    CheckOptions:
      WarnOnFloatingPointNarrowingConversion: false
      readability-identifier-naming.VariableCase: camelCase
      readability-identifier-naming.ClassMemberCase: camelBack
      readability-identifier-naming.ClassMemberPrefix: m_
      cppcoreguidelines-non-private-member-variables-in-classes.AllowedClasses: ".*Base$"

CompileFlags:
  Add: [
    #- 明确指定 C++ 标准版本为 C++20
    -std=c++20,
    #- -Wno-documentation,
    #- -Wno-missing-prototypes,
  ]

'''

listDirs: list[str] = [".vscode", "src"]

fileInfo: dict[str, str] = {
	".vscode/settings.json": txt_0,
	"src/cppAppTemplate.h": txt_1,
	"CMakeLists.txt": txt_2,
	".vscode/launch.json": txt_3,
	".gitignore": txt_4,
	"src/src.cmake": txt_5,
	"src/cppAppTemplate.cpp": txt_6,
	".clang-format": txt_7,
	"main.cpp": txt_8,
	".clangd": txt_9,

}
