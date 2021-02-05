'''
A primitive cross-compiler that compiles Deutsches Java (German Java) into actual real Java.
This is just done via some regular expressions and stuff.
'''
import re
import argparse
from functools import partial

# an array of replacement rules, which determines the Deutsches Java language
replacers = {
    # modifiers
    re.compile(r'\b(öffentlich|oeffentlich)\b'): 'public',
    re.compile(r'\b(privat)\b'): 'private',
    re.compile(r'\b(geschützt|geschuetzt)\b'): 'protected',
    re.compile(r'\b(endgültig|endgueltig)\b'): 'final',
    re.compile(r'\b(fixiert|fest)\b'): 'static',
    re.compile(r'\b(abstrakt)\b'): 'abstract',
    re.compile(r'\b(standard)\b'): 'default',
    re.compile(r'\b(nativ)\b'): 'native',
    re.compile(r'\b(versiegelt)\b'): 'sealed',
    re.compile(r'\b(nicht-versiegelt)\b'): 'non-sealed',
    re.compile(r'\b(strengfk)\b'): 'strictfp',
    re.compile(r'\b(veränderlich|veraenderlich)\b'): 'volatile',
    re.compile(r'\b(temporär|temporaer)\b'): 'transient',

    # data/oop
    re.compile(r'\b(importiere)\b'): 'import',
    re.compile(r'\b(paket)\b'): 'package',

    re.compile(r'\b(klasse)\b'): 'class',
    re.compile(r'\b(aufzähl|aufzaehl)\b'): 'enum',
    re.compile(r'\b(schnittstelle)\b'): 'interface',
    re.compile(r'\b(eintrag)\b'): 'record',

    re.compile(r'\b(erweitert)\b'): 'extends',
    re.compile(r'\b(implementiert)\b'): 'implements',
    re.compile(r'\b(über|ueber)\b'): 'super',
    re.compile(r'\b(dieses)\b'): 'this',

    # primitive types
    re.compile(r'\b(nichts)\b'): 'void',
    re.compile(r'\b(ganz)\b'): 'int',
    re.compile(r'\b(groß|gross)\b'): 'long',
    re.compile(r'\b(kurz)\b'): 'short',
    re.compile(r'\b(fließ|fliess)\b'): 'float',
    re.compile(r'\b(doppel)\b'): 'double',
    re.compile(r'\b(boolesche)\b'): 'boolean',
    re.compile(r'\b(zeichen)\b'): 'char',

    re.compile(r'\b(wahr)\b'): 'true',
    re.compile(r'\b(falsch)\b'): 'false',
    re.compile(r'\b(leer)\b'): 'null',

    re.compile(r'\b(instanzvon)\b'): 'instanceof',

    # control flow
    re.compile(r'\b(prüfe|pruefe)\b'): 'assert',
    re.compile(r'\b(falls)\b'): 'if',
    re.compile(r'\b(ansonsten)\b'): 'else',
    re.compile(r'\b(solange)\b'): 'while',
    re.compile(r'\b(tue)\b'): 'do',
    re.compile(r'\b(für|fuer)\b'): 'for',
    re.compile(r'\b(schalte)\b'): 'switch',
    re.compile(r'\b(fall)\b'): 'case',
    re.compile(r'\b(abbruch)\b'): 'break',
    re.compile(r'\b(fortfahren)\b'): 'continue',
    re.compile(r'\b(rückgabe)\b'): 'return',
    re.compile(r'\b(versuche)\b'): 'try',
    re.compile(r'\b(fange)\b'): 'catch',
    re.compile(r'\b(schließlich|schliesslich)\b'): 'finally',
    re.compile(r'\b(werfe)\b'): 'throw',
    re.compile(r'\b(wirft)\b'): 'throws',
    re.compile(r'\b(synchronisiert)\b'): 'synchronized',

    # selected common JBCL and types
    re.compile(r'\b(Objekt)\b'): 'Object',
    re.compile(r'\b(Textkette)\b'): 'String',
    re.compile(r'\b(Ganzzahl)\b'): 'Integer',
    re.compile(r'\b(Großganzzahl|Grossganzzahl)\b'): 'Long',
    re.compile(r'\b(Kurzganzzahl)\b'): 'Short',
    re.compile(r'\b(Fließkommazahl|Fliesskommazahl)\b'): 'Float',
    re.compile(r'\b(Doppelkommazahl)\b'): 'Double',
    re.compile(r'\b(Boolesche)\b'): 'Boolean',
    re.compile(r'\b(Zeichen)\b'): 'Character',

    re.compile(r'\b(System.aus)\b'): 'System.out',
    re.compile(r'(\.drucke\()'): '.print(',
    re.compile(r'\b(haupt\s*\()'): 'main(',
    re.compile(r'(\.druckezl\()'): '.println(',
}

# replacers only for modul-info.dava
module_replacers = {
    re.compile(r'\b(exportiert)\b'): 'exports',
    re.compile(r'\b(modul)\b'): 'module',
    re.compile(r'\b(offenes)\b'): 'open',
    re.compile(r'\b(öffnet|oeffnet)\b'): 'opens',
    re.compile(r'\b(versorgt)\b'): 'provides',
    re.compile(r'\b(benötigt|benoetigt)\b'): 'requires',
    re.compile(r'\b(benutzt)\b'): 'uses',
    re.compile(r'\b(mit)\b'): 'with',
    re.compile(r'\b(zu)\b'): 'to',
    re.compile(r'\b(transitiv)\b'): 'transitive'
}


def compileToJava(djava: str, module_mode: bool = False) -> str:
    java = djava
    for pattern, replacement in replacers.items():
        java = re.sub(pattern, replacement, java)
    if module_mode:
        for pattern, replacement in module_replacers.items():
            java = re.sub(pattern, replacement, java)
        
    return java


if __name__ == '__main__':
    import sys
    params = argparse.ArgumentParser(description='A cross-compiler for the Deutsches Java programming language. The Deutsches Java (German Java) Programming language is a modified version of the Java programming language that makes Java speak German by replacing almost all keywords.',
                                     epilog='Do not use this for serious business. The project license applies.', allow_abbrev=True)

    params.add_argument('-o', '--output', action='store', dest='output',
                        metavar='OUTPUT FILE', type=partial(open, encoding='utf-8'),
                        help='The output file name. By default, the name of the original file but with an ending of .java instead of .djava is used.')
    params.add_argument('input', action='store',
                        type=partial(open, encoding='utf-8'), help='The input .dava/.djava file to be cross-compiled.')

    args = params.parse_args(sys.argv[1:])

    # generate output file name if necessary
    if not args.output:
        args.output = open(re.sub(r'\.(dava|djava)$', '.java',
                                  re.sub(r'modul-info\.(dava|djava)$', 'module-info.java', args.input.name)), 'w', encoding='utf-8')

    is_module = args.output.name.endswith('module-info.java')

    for line in args.input:
        args.output.write(compileToJava(line, is_module))

    args.output.close()
    args.input.close()
