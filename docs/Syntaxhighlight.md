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
| `abap`         | [ABAP](/:en:ABAP "wikilink")                                                            |
| `actionscript` | [ActionScript](/:en:ActionScript "wikilink")                                            |
| `ada`          | [Ada](/:en:Ada_(programming_language) "wikilink")                                       |
| `apache`       | [Apache Configuration](/:en:Apache_HTTP_Server "wikilink")                              |
| `applescript`  | [AppleScript](/:en:AppleScript "wikilink")                                              |
| `asm`          | [Assembly](/:en:Assembly_language "wikilink")                                           |
| `asp`          | [Active Server Pages (ASP)](/:en:Active_Server_Pages "wikilink")                        |
| `autoit`       | [AutoIt](/:en:AutoIt "wikilink")                                                        |
| `bash`         | [Bash](/:en:Bash_(Unix_shell) "wikilink")                                               |
| `basic4gl`     | [Basic4GL](/:en:Basic4GL "wikilink")                                                    |
| `bf`           | [Brainfuck](/:en:Brainfuck "wikilink")                                                  |
| `blitzbasic`   | [Blitz BASIC](/:en:Blitz_BASIC "wikilink")                                              |
| `bnf`          | [Backus-Naur Form](/:en:Backus-Naur_Form "wikilink")                                    |
| `c`            | [C](/:en:C_(programming_language) "wikilink")                                           |
| `c_mac`        | C (Mac)                                                                                 |
| `caddcl`       | [AutoCAD DCL](/:en:Dialog_Control_Language "wikilink")                                  |
| `cadlisp`      | [AutoLISP](/:en:AutoLISP "wikilink")                                                    |
| `cfdg`         | CFDG                                                                                    |
| `cfm`          | [ColdFusion Markup Language](/:en:ColdFusion_Markup_Language "wikilink")                |
| `cil`          | [Common Intermediate Language (CIL)](/:en:Common_Intermediate_Language "wikilink")      |
| `cobol`        | [COBOL](/:en:COBOL "wikilink")                                                          |
| `cpp-qt`       | [C++ (Qt toolkit)](/:en:Qt_(toolkit) "wikilink")                                        |
| `cpp`          | [C++](/:en:C++ "wikilink")                                                              |
| `csharp`       | [C\#](/:en:C_Sharp_(programming_language) "wikilink")                                   |
| `css`          | [Cascading Style Sheets (CSS)](/:en:Cascading_Style_Sheets "wikilink")                  |
| `d`            | [D](/:en:D_(programming_language) "wikilink")                                           |
| `delphi`       | [Delphi](/:en:Delphi_programming_language "wikilink")                                   |
| `diff`         | [Diff](/:en:diff "wikilink")                                                            |
| `div`          | DIV                                                                                     |
| `dos`          | [DOS batch file](/:en:DOS_batch_file "wikilink")                                        |
| `dot`          | [DOT](/:en:DOT_language "wikilink")                                                     |
| `eiffel`       | [Eiffel](/:en:Eiffel_(programming_language) "wikilink")                                 |
| `fortran`      | [Fortran](/:en:Fortran "wikilink")                                                      |
| `freebasic`    | [FreeBASIC](/:en:FreeBASIC "wikilink")                                                  |
| `gambas`       | [Gambas](/:en:Gambas_programming_language "wikilink")                                   |
| `genero`       | Genero                                                                                  |
| `gettext`      | [GNU internationalization (i18n) library](/:en:GNU_gettext "wikilink")                  |
| `glsl`         | [OpenGL Shading Language (GLSL)](/:en:GLSL "wikilink")                                  |
| `gml`          | [Game Maker Language (GML)](/:en:Game_Maker_Language "wikilink")                        |
| `gnuplot`      | [gnuplot](/:en:Gnuplot "wikilink")                                                      |
| `groovy`       | [Groovy](/:en:Groovy_(programming_language) "wikilink")                                 |
| `haskell`      | [Haskell](/:en:Haskell_(programming_language) "wikilink")                               |
| `Haxe`         | [Haxe](/:en:Haxe "wikilink")                                                            |
| `hq9plus`      | HQ9+                                                                                    |
| `html4strict`  | [HTML](/:en:HTML "wikilink")                                                            |
| `html5`        | [HTML5](/:en:HTML5 "wikilink")                                                          |
| `idl`          | [Uno IDL](/:en:Universal_Network_Objects "wikilink")                                    |
| `ini`          | [INI](/:en:INI_file "wikilink")                                                         |
| `inno`         | [Inno](/:en:Inno_Setup "wikilink")                                                      |
| `intercal`     | [INTERCAL](/:en:INTERCAL "wikilink")                                                    |
| `io`           | [Io](/:en:Io_(programming_language) "wikilink")                                         |
| `java`         | [Java](/:en:Java_(programming_language) "wikilink")                                     |
| `java5`        | [Java(TM) 2 Platform Standard Edition 5.0](/:en:Java_(programming_language) "wikilink") |
| `javascript`   | [JavaScript](/:en:JavaScript "wikilink")                                                |
| `kixtart`      | [KiXtart](/:en:KiXtart "wikilink")                                                      |
| `klonec`       | Klone C                                                                                 |
| `klonecpp`     | Klone C++                                                                               |
| `latex`        | [LaTeX](/:en:LaTeX "wikilink")                                                          |
| `lisp`         | [Lisp](/:en:Lisp_(programming_language) "wikilink")                                     |
| `lolcode`      | [LOLCODE](/:en:LOLCODE "wikilink")                                                      |
| `lotusscript`  | [LotusScript](/:en:LotusScript "wikilink")                                              |
| `lua`          | [Lua](/:en:Lua_(programming_language) "wikilink")                                       |

| Code           | Language                                                                                        |
|----------------|-------------------------------------------------------------------------------------------------|
| `m68k`         | [Motorola 68000 Assembler](/:en:Motorola_68000 "wikilink")                                      |
| `make`         | [make](/:en:Make_(software) "wikilink")                                                         |
| `matlab`       | [MATLAB M](/:en:MATLAB "wikilink")                                                              |
| `mirc`         | [mIRC scripting language](/:en:mIRC_scripting_language "wikilink")                              |
| `mxml`         | [MXML](/:en:MXML "wikilink")                                                                    |
| `mpasm`        | [Microchip Assembler](/:en:PIC_microcontroller "wikilink")                                      |
| `mysql`        | [MySQL](/:en:MySQL "wikilink")                                                                  |
| `nsis`         | [Nullsoft Scriptable Install System (NSIS)](/:en:Nullsoft_Scriptable_Install_System "wikilink") |
| `objc`         | [Objective-C](/:en:Objective-C "wikilink")                                                      |
| `ocaml-brief`  | [OCaml](/:en:Objective_Caml "wikilink")                                                         |
| `ocaml`        | [OCaml](/:en:Objective_Caml "wikilink")                                                         |
| `oobas`        | [OpenOffice.org Basic](/:en:StarOffice_Basic "wikilink")                                        |
| `oracle8`      | [Oracle 8 SQL](/:en:PL/SQL "wikilink")                                                          |
| `oracle11`     | [Oracle 11 SQL](/:en:PL/SQL "wikilink")                                                         |
| `pascal`       | [Pascal](/:en:Pascal_(programming_language) "wikilink")                                         |
| `per`          | per                                                                                             |
| `perl`         | [Perl](/:en:Perl "wikilink")                                                                    |
| `php-brief`    | [PHP](/:en:PHP "wikilink")                                                                      |
| `php`          | [PHP](/:en:PHP "wikilink")                                                                      |
| `pixelbender`  | [Pixel Bender](/:en:Adobe_Pixel_Bender "wikilink")                                              |
| `plsql`        | [PL/SQL](/:en:PL/SQL "wikilink")                                                                |
| `povray`       | [Persistence of Vision Raytracer](/:en:POV-Ray "wikilink")                                      |
| `powershell`   | [Windows PowerShell](/:en:Windows_PowerShell "wikilink")                                        |
| `progress`     | [OpenEdge Advanced Business Language](/:en:OpenEdge_Advanced_Business_Language "wikilink")      |
| `prolog`       | [Prolog](/:en:Prolog "wikilink")                                                                |
| `providex`     | [ProvideX](/:en:ProvideX "wikilink")                                                            |
| `python`       | [Python](/:en:Python_(programming_language) "wikilink")                                         |
| `qbasic`       | [QBasic/QuickBASIC](/:en:QBasic "wikilink")                                                     |
| `rails`        | [Rails](/:en:Ruby_on_Rails "wikilink")                                                          |
| `reg`          | [Windows Registry](/:en:Windows_Registry "wikilink")                                            |
| `robots`       | [robots.txt](/:en:Robots_Exclusion_Standard "wikilink")                                         |
| `rsplus`       | [R](/:en:R_(programming_language) "wikilink")                                                   |
| `ruby`         | [Ruby](/:en:Ruby_(programming_language) "wikilink")                                             |
| `sas`          | [SAS](/:en:SAS_System "wikilink")                                                               |
| `scala`        | [Scala](/:en:Scala_(programming_language) "wikilink")                                           |
| `scheme`       | [Scheme](/:en:Scheme_(programming_language) "wikilink")                                         |
| `scilab`       | [Scilab](/:en:Scilab "wikilink")                                                                |
| `sdlbasic`     | [SdlBasic](/:en:SdlBasic "wikilink")                                                            |
| `smalltalk`    | [Smalltalk](/:en:Smalltalk "wikilink")                                                          |
| `smarty`       | [Smarty](/:en:Smarty "wikilink")                                                                |
| `sql`          | [SQL](/:en:SQL "wikilink")                                                                      |
| `tcl`          | [Tcl](/:en:Tcl "wikilink")                                                                      |
| `teraterm`     | [Tera Term](/:en:TeraTerm "wikilink")                                                           |
| `text`         | [Plain text](/:en:Plain_text "wikilink")                                                        |
| `thinbasic`    | [thinBasic](/:en:thinBasic "wikilink")                                                          |
| `tsql`         | [Transact-SQL](/:en:Transact-SQL "wikilink")                                                    |
| `typoscript`   | [TypoScript](/:en:TYPO3 "wikilink")                                                             |
| `vala`         | [Vala](/:en:Vala_(programming_language) "wikilink")                                             |
| `vb`           | [Visual Basic](/:en:Visual_Basic "wikilink")                                                    |
| `vbnet`        | [Visual Basic .NET](/:en:Visual_Basic_.NET "wikilink")                                          |
| `verilog`      | [Verilog](/:en:Verilog "wikilink")                                                              |
| `vhdl`         | [VHDL](/:en:VHSIC_Hardware_Description_Language "wikilink")                                     |
| `vim`          | [Vimscript](/:en:Vimscript "wikilink")                                                          |
| `visualfoxpro` | [Visual FoxPro](/:en:Visual_FoxPro "wikilink")                                                  |
| `visualprolog` | [Visual Prolog](/:en:Visual_Prolog "wikilink")                                                  |
| `whitespace`   | [Whitespace](/:en:Whitespace_(programming_language) "wikilink")                                 |
| `winbatch`     | [Winbatch](/:en:Winbatch "wikilink")                                                            |
| `xml`          | [XML](/:en:XML "wikilink")                                                                      |
| `xorg_conf`    | [Xorg.conf](/:en:Xorg.conf "wikilink")                                                          |
| `xpp`          | [X++](/:en:Microsoft_Dynamics_AX "wikilink")                                                    |
| `yaml`         | [YAML](/:en:YAML "wikilink")                                                                    |
| `z80`          | [ZiLOG Z80 Assembler](/:en:Zilog_Z80 "wikilink")                                                |

<div style="clear:both">
</div>