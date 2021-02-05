# Dava: Deutsches Java Cross-compiler

The Deutsches Java (German Java) programming language is a modified Java programming language where all keywords and a couple of standard types are replaced by German equivalents, so that Deutsches Java is essentially Java speaking German. This is achieved through a really primitive Python script that replaces all Deutsches Java keywords in its input file by the Java equivalent.

Deutsches Java has equivalents for all Java keywords that do something (so no `const` or `goto` ), including proposed / incubator keywords like `record`. `module-info.java` and its specialized keywords are also supported.

## How to run

This is a runnable python module. Invoke `python dava` in this folder. Tested with CPython 3.8.3 but any 3.x should work (only uses standard library re, argparse, functools). Get help output with `-h`. If you do not specify an output file, the same filename but an ending of `.java` is used (this will only work for endings `.dava` and `.djava`). Exception: `modul-info.dava`/`modul-info.djava` becomes `module-info.java`. The "module mode" mentioned above is triggered if your implicit or explicit output file is `module-info.java`.

## Credits

Created by kleines Filmröllchen 2021 in two hours. Do not take this seriously. The project license MIT applies.