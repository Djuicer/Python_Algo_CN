# Project Euler 中文化进度

更新日期：2026-09-27

统计口径：`project_euler/` 下全部 322 个 Python 文件。空 `__init__.py` 与测试源码不作为自然语言本地化对象。

当前汇总：DONE 181，PARTIAL 0，PENDING 0，NO_TRANSLATION_NEEDED 141，NEEDS_REVIEW 0。

| 文件/题目 | 状态 | 测试 | 备注 |
|---|---|---|---|
| `project_euler/problem_001` 至 `problem_129` 中当前已修改、且未在下方单列的源码（116 个） | DONE | NOT_RUN | 已确认代码 token 未变化；保留 URL、公式、doctest、异常文本及固定字符串 |
| `project_euler/problem_005/sol2.py` | DONE | ENVIRONMENT_DEPENDENCY | 中文化完成且编译通过；doctest 被依赖文件的既有 Python 2 异常语法阻断 |
| `project_euler/problem_008/sol2.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_009/sol2.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_010/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_010/sol2.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_015/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_020/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_027/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_029/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_031/sol2.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_035/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_037/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_041/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_042/solution42.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_046/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_047/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_049/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_051/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_053/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_054/sol1.py` | DONE | PASS | doctest 通过；pytest 测试因环境缺少 pytest 未运行 |
| `project_euler/problem_056/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_060/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_063/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_068/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_070/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_072/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_074/sol2.py` | DONE | PASS | doctest 通过；异常文本保持英文 |
| `project_euler/problem_079/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_082/sol1.py` | DONE | PASS | doctest 通过；URL 与界面命令保持原文 |
| `project_euler/problem_085/sol1.py` | DONE | PASS | doctest 通过；参考资料保持原文 |
| `project_euler/problem_092/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_101/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_104/sol1.py` | DONE | LONG_RUNNING_TEST | check/check1 doctest 通过；solution() 百万级大整数循环未运行 |
| `project_euler/problem_107/sol1.py` | DONE | PASS | doctest 通过；参考资料保持原文 |
| `project_euler/problem_111/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_123/sol1.py` | DONE | PASS | doctest 通过；公式保持不变 |
| `project_euler/problem_109/sol1.py` | DONE | PASS | doctest 通过；示例组合保持不变 |
| `project_euler/problem_131/sol1.py` | DONE | PASS | doctest 通过；公式保持不变 |
| `project_euler/problem_135/sol1.py` | DONE | PASS | doctest 通过；公式与数字保持不变 |
| `project_euler/problem_136/sol1.py` | DONE | PASS | doctest 通过；公式与数字保持不变 |
| `project_euler/problem_137/sol1.py` | DONE | PASS | doctest 通过；公式、数字与参考资料保持不变 |
| `project_euler/problem_138/sol1.py` | DONE | PASS | doctest 通过；公式、数字与参考资料保持不变 |
| `project_euler/problem_142/sol1.py` | DONE | PASS | doctest 通过；公式与数字保持不变 |
| `project_euler/problem_144/sol1.py` | DONE | PASS | doctest 通过；公式与数字保持不变 |
| `project_euler/problem_145/sol1.py` | DONE | PASS | doctest 通过；作者信息与运行时字符串保持不变 |
| `project_euler/problem_164/sol1.py` | DONE | PASS | doctest 通过；参数名保持不变 |
| `project_euler/problem_173/sol1.py` | DONE | PASS | doctest 通过 |
| `project_euler/problem_174/sol1.py` | DONE | PASS | doctest 通过；公式与数字保持不变 |
| `project_euler/problem_180/sol1.py` | DONE | PASS | doctest 通过；题号、公式、数字与参考资料保持不变 |
| `project_euler/problem_187/sol1.py` | DONE | PASS | doctest 通过；数列、公式、参考资料与运行时字符串保持不变 |
| `project_euler/problem_188/sol1.py` | DONE | PASS | doctest 通过；公式、数字与参考资料保持不变 |
| `project_euler/problem_190/sol1.py` | DONE | PASS | doctest 通过；公式与数字保持不变 |
| `project_euler/problem_191/sol1.py` | DONE | PASS | doctest 通过；字符串数据与参考资料保持不变 |
| `project_euler/problem_203/sol1.py` | DONE | PASS | doctest 通过；数表、公式、数字与参考资料保持不变 |
| `project_euler/problem_205/sol1.py` | DONE | PASS | doctest 通过；数列与输出格式保持不变 |
| `project_euler/problem_206/sol1.py` | DONE | PASS | doctest 通过；数字模式与公式保持不变 |
| `project_euler/problem_207/sol1.py` | DONE | PASS | doctest 通过；公式、表格与数字保持不变 |
| `project_euler/problem_234/sol1.py` | DONE | PASS | doctest 通过；数列、公式、数字与 URL 保持不变 |
| `project_euler/problem_301/sol1.py` | DONE | PASS | doctest 通过；局面序列与公式保持不变 |
| `project_euler/problem_345/sol1.py` | DONE | PASS | doctest 通过；矩阵数据与运行时字符串保持不变 |
| `project_euler/problem_493/sol1.py` | DONE | PASS | 已完成中文化；doctest 通过 |
| `project_euler/problem_551/sol1.py` | DONE | PASS | 已完成中文化；doctest 通过 |
| `project_euler/problem_587/sol1.py` | DONE | PASS | 已完成中文化；doctest 通过 |
| `project_euler/problem_686/sol1.py` | DONE | PASS | 已完成中文化；doctest 通过 |
| `project_euler/problem_800/sol1.py` | DONE | PASS | 已完成中文化；doctest 通过 |
| `project_euler/**/__init__.py`（140 个） | NO_TRANSLATION_NEEDED | NOT_RUN | 空初始化文件 |
| `project_euler/problem_054/test_poker_hand.py` | NO_TRANSLATION_NEEDED | NOT_RUN | 测试源码；测试输入输出保持原文 |

## 有意保留英文

- Project Euler 标题、题号与原始 URL。
- doctest 代码、输出、异常消息和内联示例注释。
- 固定输入输出字符串、牌型/API 返回字符串、标识符、变量名与参数名。
- 数学公式、数据表、协议/格式示例、作者及来源信息。
