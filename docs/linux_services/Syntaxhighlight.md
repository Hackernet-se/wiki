---
title: Syntaxhighlight
permalink: /Syntaxhighlight/
---

För att highlighta kod måste man använda source editorn och
syntaxhighlight.

``` Python
def hello_world():
  print("Hello Hackernet")

hello_world()
```

Ser ut så här i editorn:

``` Python
<syntaxhighlight lang="Python" line>
def hello_world():
  print("Hello Hackernet")

hello_world()
</syntaxhighlight>
```

### Parametrar

#### line

Gör så att du får siffror till vänster om din kod.

``` Python
def hello_world():
  print("Hello Hackernet")
```

``` Python
<syntaxhighlight lang="Python" line>
def hello_world():
  print("Hello Hackernet")
</syntaxhighlight>
```

#### start

Används tillsammans med `line` för att starta på en annan line än 1.

``` Python
def hello_world():
  print("Hello Hackernet")
```

``` Python
<syntaxhighlight lang="Python" line start="69">
def hello_world():
  print("Hello Hackernet")
</syntaxhighlight>
```

#### highlight

Används för att highlighta en eller flera rader, `hightlight="1,2"`
eller `highlight="5-7"`

``` Python
def hello_world():
  print("Hello Hackernet")
```

``` Python
<syntaxhighlight lang="Python" line highlight=2>
def hello_world():
  print("Hello Hackernet")
</syntaxhighlight>
```

### Supportade Språk

| Code           | Language                                                                                |
|----------------|-----------------------------------------------------------------------------------------|
| `abap`         | [ABAP](:en:ABAP)                                                            |
| `actionscript` | [ActionScript](:en:ActionScript)                                            |
| `ada`          | [Ada](:en:Ada_(programming_language) "wikilink")                                       |
| `apache`       | [Apache Configuration](:en:Apache_HTTP_Server)                              |
| `applescript`  | [AppleScript](:en:AppleScript)                                              |
| `asm`          | [Assembly](:en:Assembly_language)                                           |
| `asp`          | [Active Server Pages (ASP)](:en:Active_Server_Pages)                        |
| `autoit`       | [AutoIt](:en:AutoIt)                                                        |
| `bash`         | [Bash](:en:Bash_(Unix_shell) "wikilink")                                               |
| `basic4gl`     | [Basic4GL](:en:Basic4GL)                                                    |
| `bf`           | [Brainfuck](:en:Brainfuck)                                                  |
| `blitzbasic`   | [Blitz BASIC](:en:Blitz_BASIC)                                              |
| `bnf`          | [Backus-Naur Form](:en:Backus-Naur_Form)                                    |
| `c`            | [C](:en:C_(programming_language) "wikilink")                                           |
| `c_mac`        | C (Mac)                                                                                 |
| `caddcl`       | [AutoCAD DCL](:en:Dialog_Control_Language)                                  |
| `cadlisp`      | [AutoLISP](:en:AutoLISP)                                                    |
| `cfdg`         | CFDG                                                                                    |
| `cfm`          | [ColdFusion Markup Language](:en:ColdFusion_Markup_Language)                |
| `cil`          | [Common Intermediate Language (CIL)](:en:Common_Intermediate_Language)      |
| `cobol`        | [COBOL](:en:COBOL)                                                          |
| `cpp-qt`       | [C++ (Qt toolkit)](:en:Qt_(toolkit) "wikilink")                                        |
| `cpp`          | [C++](:en:C++)                                                              |
| `csharp`       | [C\#](:en:C_Sharp_(programming_language) "wikilink")                                   |
| `css`          | [Cascading Style Sheets (CSS)](:en:Cascading_Style_Sheets)                  |
| `d`            | [D](:en:D_(programming_language) "wikilink")                                           |
| `delphi`       | [Delphi](:en:Delphi_programming_language)                                   |
| `diff`         | [Diff](:en:diff)                                                            |
| `div`          | DIV                                                                                     |
| `dos`          | [DOS batch file](:en:DOS_batch_file)                                        |
| `dot`          | [DOT](:en:DOT_language)                                                     |
| `eiffel`       | [Eiffel](:en:Eiffel_(programming_language) "wikilink")                                 |
| `fortran`      | [Fortran](:en:Fortran)                                                      |
| `freebasic`    | [FreeBASIC](:en:FreeBASIC)                                                  |
| `gambas`       | [Gambas](:en:Gambas_programming_language)                                   |
| `genero`       | Genero                                                                                  |
| `gettext`      | [GNU internationalization (i18n) library](:en:GNU_gettext)                  |
| `glsl`         | [OpenGL Shading Language (GLSL)](:en:GLSL)                                  |
| `gml`          | [Game Maker Language (GML)](:en:Game_Maker_Language)                        |
| `gnuplot`      | [gnuplot](:en:Gnuplot)                                                      |
| `groovy`       | [Groovy](:en:Groovy_(programming_language) "wikilink")                                 |
| `haskell`      | [Haskell](:en:Haskell_(programming_language) "wikilink")                               |
| `Haxe`         | [Haxe](:en:Haxe)                                                            |
| `hq9plus`      | HQ9+                                                                                    |
| `html4strict`  | [HTML](:en:HTML)                                                            |
| `html5`        | [HTML5](:en:HTML5)                                                          |
| `idl`          | [Uno IDL](:en:Universal_Network_Objects)                                    |
| `ini`          | [INI](:en:INI_file)                                                         |
| `inno`         | [Inno](:en:Inno_Setup)                                                      |
| `intercal`     | [INTERCAL](:en:INTERCAL)                                                    |
| `io`           | [Io](:en:Io_(programming_language) "wikilink")                                         |
| `java`         | [Java](:en:Java_(programming_language) "wikilink")                                     |
| `java5`        | [Java(TM) 2 Platform Standard Edition 5.0](:en:Java_(programming_language) "wikilink") |
| `javascript`   | [JavaScript](:en:JavaScript)                                                |
| `kixtart`      | [KiXtart](:en:KiXtart)                                                      |
| `klonec`       | Klone C                                                                                 |
| `klonecpp`     | Klone C++                                                                               |
| `latex`        | [LaTeX](:en:LaTeX)                                                          |
| `lisp`         | [Lisp](:en:Lisp_(programming_language) "wikilink")                                     |
| `lolcode`      | [LOLCODE](:en:LOLCODE)                                                      |
| `lotusscript`  | [LotusScript](:en:LotusScript)                                              |
| `lua`          | [Lua](:en:Lua_(programming_language) "wikilink")                                       |

| Code           | Language                                                                                        |
|----------------|-------------------------------------------------------------------------------------------------|
| `m68k`         | [Motorola 68000 Assembler](:en:Motorola_68000)                                      |
| `make`         | [make](:en:Make_(software) "wikilink")                                                         |
| `matlab`       | [MATLAB M](:en:MATLAB)                                                              |
| `mirc`         | [mIRC scripting language](:en:mIRC_scripting_language)                              |
| `mxml`         | [MXML](:en:MXML)                                                                    |
| `mpasm`        | [Microchip Assembler](:en:PIC_microcontroller)                                      |
| `mysql`        | [MySQL](:en:MySQL)                                                                  |
| `nsis`         | [Nullsoft Scriptable Install System (NSIS)](:en:Nullsoft_Scriptable_Install_System) |
| `objc`         | [Objective-C](:en:Objective-C)                                                      |
| `ocaml-brief`  | [OCaml](:en:Objective_Caml)                                                         |
| `ocaml`        | [OCaml](:en:Objective_Caml)                                                         |
| `oobas`        | [OpenOffice.org Basic](:en:StarOffice_Basic)                                        |
| `oracle8`      | [Oracle 8 SQL](:en:PL/SQL)                                                          |
| `oracle11`     | [Oracle 11 SQL](:en:PL/SQL)                                                         |
| `pascal`       | [Pascal](:en:Pascal_(programming_language) "wikilink")                                         |
| `per`          | per                                                                                             |
| `perl`         | [Perl](:en:Perl)                                                                    |
| `php-brief`    | [PHP](:en:PHP)                                                                      |
| `php`          | [PHP](:en:PHP)                                                                      |
| `pixelbender`  | [Pixel Bender](:en:Adobe_Pixel_Bender)                                              |
| `plsql`        | [PL/SQL](:en:PL/SQL)                                                                |
| `povray`       | [Persistence of Vision Raytracer](:en:POV-Ray)                                      |
| `powershell`   | [Windows PowerShell](:en:Windows_PowerShell)                                        |
| `progress`     | [OpenEdge Advanced Business Language](:en:OpenEdge_Advanced_Business_Language)      |
| `prolog`       | [Prolog](:en:Prolog)                                                                |
| `providex`     | [ProvideX](:en:ProvideX)                                                            |
| `python`       | [Python](:en:Python_(programming_language) "wikilink")                                         |
| `qbasic`       | [QBasic/QuickBASIC](:en:QBasic)                                                     |
| `rails`        | [Rails](:en:Ruby_on_Rails)                                                          |
| `reg`          | [Windows Registry](:en:Windows_Registry)                                            |
| `robots`       | [robots.txt](:en:Robots_Exclusion_Standard)                                         |
| `rsplus`       | [R](:en:R_(programming_language) "wikilink")                                                   |
| `ruby`         | [Ruby](:en:Ruby_(programming_language) "wikilink")                                             |
| `sas`          | [SAS](:en:SAS_System)                                                               |
| `scala`        | [Scala](:en:Scala_(programming_language) "wikilink")                                           |
| `scheme`       | [Scheme](:en:Scheme_(programming_language) "wikilink")                                         |
| `scilab`       | [Scilab](:en:Scilab)                                                                |
| `sdlbasic`     | [SdlBasic](:en:SdlBasic)                                                            |
| `smalltalk`    | [Smalltalk](:en:Smalltalk)                                                          |
| `smarty`       | [Smarty](:en:Smarty)                                                                |
| `sql`          | [SQL](:en:SQL)                                                                      |
| `tcl`          | [Tcl](:en:Tcl)                                                                      |
| `teraterm`     | [Tera Term](:en:TeraTerm)                                                           |
| `text`         | [Plain text](:en:Plain_text)                                                        |
| `thinbasic`    | [thinBasic](:en:thinBasic)                                                          |
| `tsql`         | [Transact-SQL](:en:Transact-SQL)                                                    |
| `typoscript`   | [TypoScript](:en:TYPO3)                                                             |
| `vala`         | [Vala](:en:Vala_(programming_language) "wikilink")                                             |
| `vb`           | [Visual Basic](:en:Visual_Basic)                                                    |
| `vbnet`        | [Visual Basic .NET](:en:Visual_Basic_.NET)                                          |
| `verilog`      | [Verilog](:en:Verilog)                                                              |
| `vhdl`         | [VHDL](:en:VHSIC_Hardware_Description_Language)                                     |
| `vim`          | [Vimscript](:en:Vimscript)                                                          |
| `visualfoxpro` | [Visual FoxPro](:en:Visual_FoxPro)                                                  |
| `visualprolog` | [Visual Prolog](:en:Visual_Prolog)                                                  |
| `whitespace`   | [Whitespace](:en:Whitespace_(programming_language) "wikilink")                                 |
| `winbatch`     | [Winbatch](:en:Winbatch)                                                            |
| `xml`          | [XML](:en:XML)                                                                      |
| `xorg_conf`    | [Xorg.conf](:en:Xorg.conf)                                                          |
| `xpp`          | [X++](:en:Microsoft_Dynamics_AX)                                                    |
| `yaml`         | [YAML](:en:YAML)                                                                    |
| `z80`          | [ZiLOG Z80 Assembler](:en:Zilog_Z80)                                                |

<div style="clear:both">