/* CS101 代码编辑器（Playground 用）。
 *
 * 为什么不引 CodeMirror / Monaco：红线 6「零第三方依赖」，引入要先由人拍板。
 * 结构沿用提交页 —— 透明 textarea 叠在高亮层上，光标、选区、输入法、滚动都交给浏览器。
 * 在这之上补的是 Playground 真正缺的几件事：
 *   - 按语言切 token（9 种语言各有关键字、内置类型、字符串 / 注释 / 预处理规则）
 *   - 行号栏诊断标记：本地即时检查（括号、未结束的字符串）标黄，服务端编译错误标红
 *   - 括号匹配、自动补全、自动缩进、Ctrl+/ 注释、Tab / Shift+Tab 整块缩进
 *   - 编辑一律走 execCommand("insertText")，浏览器撤销栈不断：自动补的括号 Ctrl+Z 撤得回来
 *
 * 纯函数（scan / highlight / lint / indentFor / pairAction / …）不碰 DOM，
 * 测试在 node 里直接 require 这个文件跑。
 */
(function (root) {
"use strict";

const INDENT = "    ";
const OPEN = "([{", CLOSE = ")]}";
const PAIRS = { "(": ")", "[": "]", "{": "}", '"': '"', "'": "'" };
const words = text => new Set(text.split(/\s+/).filter(Boolean));
const IDENT = /[A-Za-z_$][\w$]*/y;
const NUM = ["num", /0[xXbBoO][\da-fA-F_']+[uUlL]*|\d[\d_']*(?:\.\d[\d_']*)?(?:[eE][+-]?\d+)?[uUlLfFdDmMjJ]*|\.\d+(?:[eE][+-]?\d+)?[fFdDmM]*/y];

// ---- 语言规则 ------------------------------------------------------------
// rules 按顺序在每个位置尝试，先命中先得；标识符在规则之后统一处理，再按集合分成
// 关键字 / 内置类型 / 函数调用（后面紧跟 "("）。第三项 "lineStart" 表示只在行首（前面只有空白）生效。
const C_COMMENT = ["com", /\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$)/y];
const C_PRE = ["pre", /#[ \t]*(?:include|import)[ \t]*(?:<[^>\n]*>)?|#[ \t]*[A-Za-z_]\w*/y, "lineStart"];
const C_STR = ["str", /(?:u8|[uUL])?R"([^()\\\s"]{0,16})\([\s\S]*?(?:\)\1"|$)|(?:u8|[uUL])?"(?:\\[\s\S]|[^"\\\n])*"?|(?:u8|[uUL])?'(?:\\[\s\S]|[^'\\\n])*'?/y];

const C_KW = words(`alignas alignof auto bool break case catch char char8_t char16_t char32_t class concept const
  constexpr const_cast continue co_await co_return decltype default delete do double dynamic_cast else enum explicit
  export extern false final float for friend goto if inline int long mutable namespace new noexcept nullptr operator
  override private protected public register reinterpret_cast requires restrict return short signed sizeof static
  static_assert static_cast struct switch template this thread_local throw true try typedef typeid typename union
  unsigned using virtual void volatile wchar_t while _Bool NULL`);
const C_TYPES = words(`std string vector map set multiset multimap unordered_map unordered_set pair tuple queue stack
  deque priority_queue list array bitset size_t int8_t int16_t int32_t int64_t uint8_t uint16_t uint32_t uint64_t
  cin cout cerr endl FILE`);
const PY_KW = words(`False None True and as assert async await break class continue def del elif else except finally
  for from global if import in is lambda nonlocal not or pass raise return try while with yield`);
const PY_TYPES = words(`self cls int float str list dict set tuple bool bytes bytearray complex object type range
  frozenset Exception BaseException ValueError TypeError KeyError IndexError ZeroDivisionError RuntimeError
  StopIteration AttributeError NameError EOFError RecursionError AssertionError NotImplementedError OverflowError
  MemoryError`);
const CS_KW = words(`abstract as async await base bool break byte case catch char checked class const continue decimal
  default delegate do double else enum event explicit extern false finally fixed float for foreach get goto if implicit
  in init int interface internal is lock long namespace new null object operator out override params private protected
  public readonly record ref return sbyte sealed set short sizeof stackalloc static string struct switch this throw true
  try typeof uint ulong unchecked unsafe ushort using var virtual void volatile when where while yield nameof`);
const CS_TYPES = words(`Console Math String Int32 Int64 Double Array List Dictionary HashSet Queue Stack SortedSet
  SortedDictionary StringBuilder Enumerable System Collections Generic Linq Text IO Tuple LinkedList PriorityQueue
  BigInteger`);
const FS_KW = words(`abstract and as assert base begin class default delegate do done downcast downto elif else end
  exception extern false finally fixed for fun function global if in inherit inline interface internal lazy let match
  member module mutable namespace new not null of open or override private public rec return static struct then to true
  try type upcast use val void when while with yield`);
const FS_TYPES = words(`int int64 float double decimal string bool char byte unit list array seq option Some None
  Result Ok Error printfn printf sprintf failwith stdin stdout Console Math List Array Seq Map Set String`);
const VB_KW = words(`addhandler addressof alias and andalso as boolean byref byte byval call case catch cbool cbyte
  cchar cdate cdbl cdec char cint class clng cobj const continue csbyte cshort csng cstr ctype cuint culng cushort date
  decimal declare default delegate dim directcast do double each else elseif end enum erase error event exit false
  finally for friend function get gettype global goto handles if implements imports in inherits integer interface is
  isnot let lib like long loop me mod module mustinherit mustoverride mybase myclass namespace narrowing new next not
  nothing notinheritable notoverridable object of on operator option optional or orelse overloads overridable overrides
  paramarray partial private property protected public raiseevent readonly redim removehandler resume return sbyte
  select set shadows shared short single static step stop string structure sub synclock then throw to true try trycast
  typeof uinteger ulong ushort using when while widening with withevents writeonly xor`);
const VB_TYPES = words(`console math list dictionary array stringbuilder system`);
const SWIFT_KW = words(`actor any as associatedtype async await break case catch class continue convenience default
  defer deinit do dynamic else enum extension fallthrough false fileprivate final for func guard if import in indirect
  infix init inout internal is lazy let mutating nil nonmutating open operator optional override postfix
  precedencegroup prefix private protocol public repeat required rethrows return self Self some static struct subscript
  super switch throw throws true try typealias unowned var weak where while`);
const SWIFT_TYPES = words(`Int Int8 Int16 Int32 Int64 UInt UInt64 Double Float String Character Bool Array Dictionary
  Set Optional Any AnyObject Void Range ClosedRange Substring`);
const OBJC_KW = new Set([...C_KW, ...words("id self super nil Nil YES NO BOOL SEL IMP instancetype")]);
const OBJC_TYPES = new Set([...C_TYPES, ...words(`NSString NSMutableString NSArray NSMutableArray NSDictionary
  NSMutableDictionary NSNumber NSObject NSInteger NSUInteger CGFloat NSLog`)]);

const C_OPENS = /[([{]$/;
const LANGS = {
  python: {
    comment: "#", kw: PY_KW, types: PY_TYPES, strPrefix: /^[rRbBuUfF]{1,2}$/,
    rules: [
      ["com", /#[^\n]*/y],
      ["str", /(?:[rRbBuUfF]{1,2})?(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\[\s\S]|[^"\\\n])*"?|'(?:\\[\s\S]|[^'\\\n])*'?)/y],
      NUM,
      ["pre", /@[A-Za-z_][\w.]*/y, "lineStart"],
    ],
    opens: /(?::|[([{])$/,
    dedents: /^\s*(?:return|pass|break|continue|raise)\b/,
  },
  c: { comment: "//", kw: C_KW, types: C_TYPES, strPrefix: /^(?:u8|[uUL])?R?$/, rules: [C_COMMENT, C_PRE, C_STR, NUM], opens: C_OPENS },
  csharp: {
    comment: "//", kw: CS_KW, types: CS_TYPES, doubledAfterAt: true,
    rules: [
      C_COMMENT,
      ["pre", /#[ \t]*[A-Za-z]+/y, "lineStart"],
      ["str", /(?:\$@|@\$|@)"(?:""|[^"])*"?|\$?"""[\s\S]*?(?:"""|$)|\$?"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?/y],
      NUM,
    ],
    opens: C_OPENS,
  },
  fsharp: {
    comment: "//", kw: FS_KW, types: FS_TYPES, noSingleQuote: true,
    rules: [
      ["com", /\/\/[^\n]*|\(\*(?!\))[\s\S]*?(?:\*\)|$)/y],
      ["pre", /#[ \t]*[A-Za-z]+/y, "lineStart"],
      // 'a' 是字符；'T 是泛型参数，不是字符串 —— 所以单引号必须当场闭合才算字符。
      ["str", /\$?"""[\s\S]*?(?:"""|$)|[$@]?"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])'/y],
      NUM,
    ],
    opens: /(?:=|->|<-|\b(?:then|else|do|with|try|finally|begin)|[([{]|\[\|)$/,
  },
  vbnet: {
    comment: "'", kw: VB_KW, types: VB_TYPES, nocase: true, noSingleQuote: true, doubledQuotes: true,
    rules: [
      ["com", /'[^\n]*/y],
      ["str", /\$?"(?:""|[^"\n])*"?[cC]?/y],
      ["pre", /#[ \t]*[A-Za-z]+/y, "lineStart"],
      NUM,
    ],
    opens: /(?:\bthen$|^(?:(?:public|private|friend|protected|shared|overrides|overloads|static|partial)\s+)*(?:sub|function|module|class|structure|namespace|property|select|using|try|catch|finally|for|while|do|else|elseif|with|case|get|set)\b)/i,
  },
  swift: {
    comment: "//", kw: SWIFT_KW, types: SWIFT_TYPES, noSingleQuote: true,
    rules: [C_COMMENT, ["str", /#*"""[\s\S]*?(?:"""#*|$)|#?"(?:\\.|[^"\\\n])*"?#?/y], ["pre", /[@#][A-Za-z_]\w*/y], NUM],
    opens: C_OPENS,
  },
  objc: {
    comment: "//", kw: OBJC_KW, types: OBJC_TYPES,
    rules: [C_COMMENT, C_PRE, ["str", /@?"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?/y], ["pre", /@[A-Za-z_]\w*/y], NUM],
    opens: C_OPENS,
  },
};
LANGS.pypy3 = LANGS.python;
LANGS.cpp = LANGS.c;
const spec = lang => LANGS[lang] || LANGS.python;

// ---- 切 token ------------------------------------------------------------
// 一次扫描出所有 token 区间 [kind, start, end]；高亮、括号匹配、检查都基于同一份切分，
// 保证「字符串里的括号不参与匹配」在三处一致。
function scan(code, lang) {
  const L = spec(lang), tokens = [], n = code.length;
  let i = 0;
  while (i < n) {
    const ch = code[i];
    if (ch === " " || ch === "\t" || ch === "\n" || ch === "\r") { i++; continue; }
    let hit = null;
    for (const rule of L.rules) {
      if (rule[2] === "lineStart" && !atLineStart(code, i)) continue;
      rule[1].lastIndex = i;
      const m = rule[1].exec(code);
      if (m && m[0]) { hit = [rule[0], m[0].length]; break; }
    }
    if (hit) { tokens.push([hit[0], i, i + hit[1]]); i += hit[1]; continue; }
    IDENT.lastIndex = i;
    const m = IDENT.exec(code);
    if (m) {
      const word = m[0], key = L.nocase ? word.toLowerCase() : word;
      let kind = L.kw.has(key) ? "kw" : L.types.has(key) ? "type" : null;
      if (!kind) {
        let j = i + word.length;
        while (code[j] === " ") j++;
        if (code[j] === "(") kind = "fn";
      }
      if (kind) tokens.push([kind, i, i + word.length]);
      i += word.length;
      continue;
    }
    i++;
  }
  return tokens;
}

function atLineStart(code, i) {
  for (let k = i - 1; k >= 0; k--) {
    if (code[k] === "\n") return true;
    if (code[k] !== " " && code[k] !== "\t") return false;
  }
  return true;
}

// 字符串 / 块注释是否已闭合。只给检查和「引号要不要自动补一个」用。
function tokenClosed(kind, text, lang) {
  if (kind === "com") return !/^(?:\/\*|\(\*)/.test(text) || (text.length >= 4 && /(?:\*\/|\*\))$/.test(text));
  if (kind !== "str") return true;
  const m = /^[A-Za-z0-9@$#]*?("""|'''|"|')/.exec(text);
  if (!m) return true;
  const quote = m[1], prefix = text.slice(0, m[0].length - quote.length);
  let body = text.slice(m[0].length);
  if (prefix.includes("#")) body = body.replace(/#+$/, "");
  if (lang === "vbnet") body = body.replace(/"[cC]$/, '"');
  if (/R$/.test(prefix) && quote === '"') return /\)[^()\\\s"]{0,16}"$/.test(body);
  if (quote.length === 3) return body.length >= 3 && body.endsWith(quote);
  if (spec(lang).doubledQuotes || (spec(lang).doubledAfterAt && prefix.includes("@"))) return /^(?:""|[^"])*"$/.test(body);
  if (!body.endsWith(quote)) return false;
  return (body.slice(0, -1).match(/\\*$/)[0].length % 2) === 0;
}

function lineStarts(code) {
  const starts = [0];
  for (let i = code.indexOf("\n"); i >= 0; i = code.indexOf("\n", i + 1)) starts.push(i + 1);
  return starts;
}

// 位置 → [行, 列]，都从 1 开始（与编译器报错一致）。
function lineCol(starts, pos) {
  let lo = 0, hi = starts.length - 1;
  while (lo < hi) {
    const mid = (lo + hi + 1) >> 1;
    if (starts[mid] <= pos) lo = mid; else hi = mid - 1;
  }
  return [lo + 1, pos - starts[lo] + 1];
}

// 字符串和注释覆盖的位置标 1：括号匹配与检查都要跳过它们。
function codeMask(code, tokens) {
  const mask = new Uint8Array(code.length);
  for (const t of tokens) if (t[0] === "str" || t[0] === "com") mask.fill(1, t[1], t[2]);
  return mask;
}

const escapeHtml = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function highlight(code, lang, marks, tokens) {
  tokens = tokens || scan(code, lang);
  const mark = marks || [];
  let out = "", i = 0, ti = 0;
  const wrap = (text, cls) => '<span class="' + cls + '">' + escapeHtml(text) + "</span>";
  while (i < code.length) {
    while (ti < tokens.length && tokens[ti][2] <= i) ti++;
    if (ti < tokens.length && tokens[ti][1] === i) {
      const t = tokens[ti++];
      out += wrap(code.slice(t[1], t[2]), "t-" + t[0]);
      i = t[2];
      continue;
    }
    if (mark.indexOf(i) >= 0) { out += wrap(code[i], "t-match"); i++; continue; }
    let j = i;
    while (j < code.length && !(ti < tokens.length && tokens[ti][1] === j) && mark.indexOf(j) < 0) j++;
    out += escapeHtml(code.slice(i, j));
    i = j;
  }
  return out;
}

// 光标处（或其左侧）若是括号，返回它与配对括号的下标。字符串 / 注释里的括号一律不参与。
function bracketMatch(code, pos, lang, tokens) {
  const mask = codeMask(code, tokens || scan(code, lang));
  for (const at of [pos, pos - 1]) {
    if (at < 0 || at >= code.length || mask[at]) continue;
    const ch = code[at], o = OPEN.indexOf(ch), c = CLOSE.indexOf(ch);
    if (o < 0 && c < 0) continue;
    const step = o >= 0 ? 1 : -1, want = o >= 0 ? CLOSE[o] : OPEN[c];
    let depth = 0;
    for (let k = at; k >= 0 && k < code.length; k += step) {
      if (mask[k]) continue;
      if (code[k] === ch) depth++;
      else if (code[k] === want && !--depth) return [at, k].sort((x, y) => x - y);
    }
    return null;
  }
  return null;
}

// ---- 即时检查 ------------------------------------------------------------
// 不替代编译器：只抓打字时最常见、又最容易肉眼漏掉的几类问题，结果标黄。
// 真正的语法错误以「语法检查 / 运行」时服务端编译器的报告为准（标红）。
function lint(code, lang, tokens) {
  tokens = tokens || scan(code, lang);
  const out = [], starts = lineStarts(code);
  const report = (pos, message) => {
    const [line, column] = lineCol(starts, pos);
    out.push({ line, column, severity: "warning", message });
  };
  for (const t of tokens) {
    if (!tokenClosed(t[0], code.slice(t[1], t[2]), lang)) report(t[1], t[0] === "str" ? "字符串没有结束" : "注释没有结束");
  }
  const mask = codeMask(code, tokens), stack = [];
  for (let i = 0; i < code.length; i++) {
    if (mask[i]) continue;
    const ch = code[i];
    if (OPEN.includes(ch)) stack.push(i);
    else if (CLOSE.includes(ch)) {
      // 右括号往栈里找配对的左括号：夹在中间没配上的，才是真正漏写右括号的地方。
      // 直接和栈顶比会把错报在后面的 "}" 上，而漏掉的其实是前面某行的 "("。
      const want = OPEN[CLOSE.indexOf(ch)];
      let k = stack.length - 1;
      while (k >= 0 && code[stack[k]] !== want) k--;
      if (k < 0) { report(i, "多余的 '" + ch + "'"); continue; }
      for (const o of stack.splice(k)) if (code[o] !== want) report(o, "'" + code[o] + "' 没有闭合");
    }
  }
  for (const o of stack) report(o, "'" + code[o] + "' 没有闭合");
  if (spec(lang) === LANGS.python) {
    starts.forEach((s, k) => {
      if (/^(?: +\t|\t+ )/.test(code.slice(s, s + 64))) report(s, "缩进混用了 Tab 和空格");
    });
  }
  out.sort((a, b) => a.line - b.line || a.column - b.column);
  return out.slice(0, 50);
}

// ---- 编辑动作（纯函数）----------------------------------------------------
// 都返回 {from, to, insert, selStart, selEnd}（或 caret），null 表示走浏览器默认行为。

// 回车后新行的缩进：沿用本行；行尾是「开块」记号就多缩一级；Python 的 return/pass 之后退一级。
function indentFor(code, pos, lang) {
  const L = spec(lang);
  const lineStart = code.lastIndexOf("\n", pos - 1) + 1;
  const line = code.slice(lineStart, pos);
  const base = (line.match(/^[ \t]*/) || [""])[0];
  const comment = scan(line, lang).find(t => t[0] === "com");
  const trimmed = (comment ? line.slice(0, comment[1]) : line).trim();
  if (trimmed && L.opens.test(trimmed)) return base + INDENT;
  if (L.dedents && L.dedents.test(line)) return base.slice(0, Math.max(0, base.length - INDENT.length));
  return base;
}

function enterAction(value, start, end, lang) {
  const lineStart = value.lastIndexOf("\n", start - 1) + 1;
  const before = value.slice(lineStart, start);
  const base = (before.match(/^[ \t]*/) || [""])[0];
  const o = OPEN.indexOf(before.trimEnd().slice(-1));
  if (o >= 0 && value[end] === CLOSE[o]) {        // {|} 回车：展开成三行，光标落在中间
    const inner = "\n" + base + INDENT;
    return { from: start, to: end, insert: inner + "\n" + base, caret: start + inner.length };
  }
  const indent = indentFor(value, start, lang);
  return { from: start, to: end, insert: "\n" + indent, caret: start + 1 + indent.length };
}

function insideStringOrComment(value, pos, lang) {
  for (const t of scan(value, lang)) {
    if (t[1] >= pos) break;
    if (t[0] !== "str" && t[0] !== "com") continue;
    if (pos < t[2]) return true;
    if (pos === t[2] && !tokenClosed(t[0], value.slice(t[1], t[2]), lang)) return true;
    if (pos === t[2] && t[0] === "com" && !/(?:\*\/|\*\))$/.test(value.slice(t[1], t[2]))) return true;
  }
  return false;
}

// 右侧是这些时才自动补全：行尾、空白、右括号、分隔符。避免把 f|oo 变成 f(|)oo。
const closeOk = next => next === undefined || /[\s)\]},;:]/.test(next);

function pairAction(value, start, end, key, lang) {
  const L = spec(lang), next = value[start], quote = key === '"' || key === "'";
  if (key === "Backspace") {
    if (start !== end || start === 0) return null;
    const left = value[start - 1];
    return PAIRS[left] && PAIRS[left] === next ? { from: start - 1, to: start + 1, insert: "", caret: start - 1 } : null;
  }
  if (!PAIRS[key] && !CLOSE.includes(key)) return null;
  if (key === "'" && L.noSingleQuote) return null;      // VB 注释、F# 泛型、Swift 不用单引号
  if (start !== end) {                                  // 有选区：用这对把它裹起来，选区保留
    if (!PAIRS[key]) return null;
    return { from: start, to: end, insert: key + value.slice(start, end) + PAIRS[key], selStart: start + 1, selEnd: end + 1 };
  }
  if ((CLOSE.includes(key) || quote) && next === key) { // 右边正好是它：跳过去，不再插一个
    return { from: start, to: start, insert: "", caret: start + 1 };
  }
  if (!closeOk(next) || insideStringOrComment(value, start, lang)) return null;
  if (quote) {
    // 紧跟在标识符后面的引号多半是 don't 这种；字符串前缀（f"…"、u8"…"）除外
    const word = (/[A-Za-z_][\w]*$/.exec(value.slice(Math.max(0, start - 32), start)) || [""])[0];
    if (word && !(L.strPrefix && L.strPrefix.test(word))) return null;
  }
  return { from: start, to: start, insert: key + PAIRS[key], caret: start + 1 };
}

// 在行首空白里退格：一次退到上一个 4 的倍数。
function softBackspace(value, start, end) {
  if (start !== end) return null;
  const before = value.slice(value.lastIndexOf("\n", start - 1) + 1, start);
  if (before.length < 2 || /[^ ]/.test(before)) return null;
  const width = before.length % INDENT.length || INDENT.length;
  return { from: start - width, to: start, insert: "", caret: start - width };
}

// 在只有缩进的行上敲 "}"：先退一级再插入。
function closerOutdent(value, start, end, key) {
  if (key !== "}" || start !== end || value[start] === key) return null;
  const before = value.slice(value.lastIndexOf("\n", start - 1) + 1, start);
  if (before.length < INDENT.length || /[^ ]/.test(before)) return null;
  return { from: start - INDENT.length, to: start, insert: key, caret: start - INDENT.length + 1 };
}

function lineRange(value, start, end) {
  const from = value.lastIndexOf("\n", start - 1) + 1;
  const stop = end > start && value[end - 1] === "\n" ? end - 1 : end;
  const to = value.indexOf("\n", stop);
  return [from, to < 0 ? value.length : to];
}

function toggleComment(value, start, end, lang) {
  const prefix = spec(lang).comment, [from, to] = lineRange(value, start, end);
  const lines = value.slice(from, to).split("\n"), body = lines.filter(l => l.trim());
  if (!body.length) return null;
  const commented = body.every(l => l.trimStart().startsWith(prefix));
  const col = Math.min(...body.map(l => l.match(/^[ \t]*/)[0].length));
  const out = lines.map(l => {
    if (!l.trim()) return l;
    if (!commented) return l.slice(0, col) + prefix + " " + l.slice(col);
    const at = l.indexOf(prefix), cut = at + prefix.length + (l[at + prefix.length] === " " ? 1 : 0);
    return l.slice(0, at) + l.slice(cut);
  });
  const insert = out.join("\n");
  if (start === end) {
    const caret = start - from >= col ? Math.max(from, start + out[0].length - lines[0].length) : start;
    return { from, to, insert, selStart: caret, selEnd: caret };
  }
  return { from, to, insert, selStart: from, selEnd: from + insert.length };
}

function shiftLines(value, start, end, outdent) {
  const [from, to] = lineRange(value, start, end);
  const lines = value.slice(from, to).split("\n"), multi = lines.length > 1;
  const out = lines.map(l => outdent ? l.replace(/^(?: {1,4}|\t)/, "") : (!multi || l.trim() ? INDENT + l : l));
  const insert = out.join("\n");
  if (insert === value.slice(from, to)) return null;
  const shift = out[0].length - lines[0].length;
  if (start === end) {
    const caret = Math.max(from, start + shift);
    return { from, to, insert, selStart: caret, selEnd: caret };
  }
  const selStart = Math.max(from, start + shift);
  return { from, to, insert, selStart, selEnd: Math.max(selStart, end + insert.length - (to - from)) };
}

// ---- 编辑器组件 ------------------------------------------------------------
class Editor {
  constructor(host, options = {}) {
    this.options = options;
    this.language = options.language || "python";
    host.classList.add("ce");
    host.innerHTML = '<div class="ce-gutter"><div class="ce-gutter-inner"></div></div>'
      + '<div class="ce-body"><div class="ce-lines" aria-hidden="true"><div class="ce-lines-inner"></div></div>'
      + '<pre class="ce-hl" aria-hidden="true"></pre>'
      + '<textarea class="ce-input" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off"'
      + ' wrap="off" aria-label="代码编辑器"></textarea></div>';
    this.gutter = host.querySelector(".ce-gutter-inner");
    this.layer = host.querySelector(".ce-lines-inner");
    this.hl = host.querySelector(".ce-hl");
    this.input = host.querySelector(".ce-input");
    if (options.placeholder) this.input.placeholder = options.placeholder;
    this.server = []; this.warnings = []; this.tokens = []; this.marks = null;
    this.lines = 0; this.serverLines = 0; this.active = 1; this.signature = ""; this.tabEscape = false;
    const ta = this.input;
    ta.addEventListener("input", () => this.changed());
    ta.addEventListener("scroll", () => this.syncScroll());
    ta.addEventListener("keydown", event => this.keydown(event));
    ta.addEventListener("focus", () => this.cursorMoved());
    ta.addEventListener("blur", () => this.cursorMoved());
    document.addEventListener("selectionchange", () => { if (document.activeElement === ta) this.cursorMoved(); });
    // 点行号：光标跳到那一行（标了诊断的行，悬停能看到原因）
    this.gutter.addEventListener("mousedown", event => {
      const row = event.target.closest(".ce-ln");
      if (row) { event.preventDefault(); this.goto(Number(row.dataset.line), 1, false); }
    });
    this.changed(true);
  }

  get value() { return this.input.value; }
  set value(text) {
    this.input.value = text;
    this.input.setSelectionRange(0, 0);
    this.input.scrollTop = 0; this.input.scrollLeft = 0;
    this.server = [];
    this.changed(true);
  }

  setLanguage(language) { this.language = language; this.server = []; this.changed(true); }
  focus() { this.input.focus(); }
  replaceAll(text) { this.edit(0, this.input.value.length, text, 0, 0); this.input.scrollTop = 0; }
  setDiagnostics(list) {
    this.server = (list || []).filter(d => d && d.line >= 1);
    this.serverLines = this.lines;
    this.renderMarkers();
  }
  remeasure() { this.signature = ""; this.renderMarkers(); this.syncScroll(); }

  goto(line, column, center = true) {
    const ta = this.input, text = ta.value, starts = lineStarts(text);
    const row = Math.max(1, Math.min(line || 1, starts.length));
    const stop = row < starts.length ? starts[row] - 1 : text.length;
    const pos = Math.min(stop, starts[row - 1] + Math.max(0, (column || 1) - 1));
    ta.focus();
    ta.setSelectionRange(pos, pos);
    if (center) ta.scrollTop = Math.max(0, (row - 1) * this.lineHeight() - ta.clientHeight / 2);
    this.cursorMoved();
  }

  lineHeight() { return parseFloat(getComputedStyle(this.input).lineHeight) || 19.5; }

  // 所有程序化修改都从这里走：execCommand 让浏览器把它记进撤销栈。
  // 不支持（或结果不对）时退回直接赋值 —— 文本一定正确，只是那一步撤销不了。
  edit(from, to, insert, selStart, selEnd) {
    const ta = this.input, before = ta.value;
    const expected = before.slice(0, from) + insert + before.slice(to);
    ta.focus();
    if (expected !== before) {
      ta.setSelectionRange(from, to);
      let done = false;
      this.muted = true;
      try { done = document.execCommand(insert ? "insertText" : "delete", false, insert); } catch (err) { done = false; }
      this.muted = false;
      if (!done || ta.value !== expected) ta.value = expected;
    }
    const a = selStart === undefined ? from + insert.length : selStart;
    ta.setSelectionRange(a, selEnd === undefined ? a : selEnd);
    this.changed();
  }

  changed(silent) {
    if (this.muted) return;
    const code = this.input.value;
    this.tokens = scan(code, this.language);
    this.warnings = lint(code, this.language, this.tokens);
    this.lines = lineStarts(code).length;
    // 行数变了，服务端报的行号就对不上了：宁可清掉，也不在错的行上标红
    if (this.server.length && this.serverLines !== this.lines) this.server = [];
    this.marks = this.bracketMarks();
    this.paint();
    this.renderMarkers();
    this.cursorMoved(true);
    if (this.options.onLint) this.options.onLint(this.warnings);
    if (!silent && this.options.onChange) this.options.onChange(code);
  }

  bracketMarks() {
    const ta = this.input;
    if (document.activeElement !== ta || ta.selectionStart !== ta.selectionEnd) return null;
    return bracketMatch(ta.value, ta.selectionStart, this.language, this.tokens);
  }

  paint() {
    // 末尾补一个换行：最后一行为空时高亮层会比 textarea 少一行高度，滚动就对不齐
    this.hl.innerHTML = highlight(this.input.value + "\n", this.language, this.marks, this.tokens);
    this.syncScroll();
  }

  cursorMoved(painted) {
    const ta = this.input;
    if (!painted) {
      const marks = this.bracketMarks();
      if (String(marks) !== String(this.marks)) { this.marks = marks; this.paint(); }
    }
    const [line, column] = lineCol(lineStarts(ta.value.slice(0, ta.selectionStart)), ta.selectionStart);
    this.active = line;
    this.renderActive();
    if (this.options.onCursor) this.options.onCursor(line, column, Math.abs(ta.selectionEnd - ta.selectionStart));
  }

  renderMarkers() {
    const byLine = new Map();
    for (const d of this.warnings) {
      const row = byLine.get(d.line) || { cls: "warn", notes: [] };
      row.notes.push(d.message); byLine.set(d.line, row);
    }
    for (const d of this.server) {
      const row = byLine.get(d.line) || { cls: "err", notes: [] };
      if (d.severity !== "warning") row.cls = "err";
      row.notes.push(d.message); byLine.set(d.line, row);
    }
    const lh = this.lineHeight();
    const signature = this.lines + "|" + lh + "|" + [...byLine].map(([l, r]) => l + r.cls + r.notes.join("")).join("");
    if (signature === this.signature) return;
    this.signature = signature;
    const rows = [];
    for (let n = 1; n <= this.lines; n++) {
      const r = byLine.get(n);
      rows.push('<div class="ce-ln' + (r ? " " + r.cls : "") + '" data-line="' + n + '"'
        + (r ? ' title="' + escapeHtml(r.notes.join("\n")) + '"' : "") + ">" + n + "</div>");
    }
    this.gutter.innerHTML = rows.join("");
    const top = parseFloat(getComputedStyle(this.input).paddingTop) || 0;
    this.layer.innerHTML = [...byLine].map(([l, r]) =>
      '<div class="ce-line ' + r.cls + '" style="top:' + (top + (l - 1) * lh) + "px;height:" + lh + 'px"></div>').join("")
      + '<div class="ce-line on" style="height:' + lh + 'px"></div>';
    this.activeBar = this.layer.lastElementChild;
    this.renderActive();
  }

  renderActive() {
    const old = this.gutter.querySelector(".ce-ln.on");
    const cur = this.gutter.children[this.active - 1];
    if (old && old !== cur) old.classList.remove("on");
    if (cur) cur.classList.add("on");
    if (this.activeBar) {
      const top = parseFloat(getComputedStyle(this.input).paddingTop) || 0;
      this.activeBar.style.top = (top + (this.active - 1) * this.lineHeight()) + "px";
      this.activeBar.hidden = document.activeElement !== this.input;
    }
  }

  syncScroll() {
    const { scrollTop, scrollLeft } = this.input;
    this.hl.scrollTop = scrollTop; this.hl.scrollLeft = scrollLeft;
    this.gutter.style.transform = "translateY(" + (-scrollTop) + "px)";
    this.layer.style.transform = "translateY(" + (-scrollTop) + "px)";
  }

  keydown(event) {
    if (event.isComposing || event.keyCode === 229) return;   // 输入法选词中，别插手
    const ta = this.input, value = ta.value, start = ta.selectionStart, end = ta.selectionEnd;
    const mod = event.ctrlKey || event.metaKey, lang = this.language, o = this.options;
    const apply = act => {
      if (!act) return false;
      event.preventDefault();
      this.edit(act.from, act.to, act.insert, act.selStart === undefined ? act.caret : act.selStart,
                act.selEnd === undefined ? act.caret : act.selEnd);
      return true;
    };
    // Esc 之后的一次 Tab 交还给浏览器移焦点：键盘用户不会被困在编辑器里
    if (event.key === "Escape") { this.tabEscape = true; return; }
    if (event.key !== "Tab") this.tabEscape = false;
    if (mod && event.key === "Enter") { event.preventDefault(); if (o.onRun) o.onRun(); return; }
    if (mod && !event.shiftKey && !event.altKey && event.key.toLowerCase() === "s") {
      event.preventDefault(); if (o.onSave) o.onSave(); return;
    }
    if (mod && event.key === "/") { event.preventDefault(); apply(toggleComment(value, start, end, lang)); return; }
    if (event.key === "Tab" && !mod && !event.altKey) {
      if (this.tabEscape) { this.tabEscape = false; return; }
      event.preventDefault();
      if (event.shiftKey || (start !== end && value.slice(start, end).includes("\n"))) {
        apply(shiftLines(value, start, end, event.shiftKey));
      } else {
        const column = start - (value.lastIndexOf("\n", start - 1) + 1);
        this.edit(start, end, " ".repeat(INDENT.length - (column % INDENT.length)));
      }
      return;
    }
    if (mod || event.altKey) return;
    if (event.key === "Enter") { apply(enterAction(value, start, end, lang)); return; }
    if (event.key === "Backspace") { apply(pairAction(value, start, end, "Backspace", lang) || softBackspace(value, start, end)); return; }
    if (event.key.length === 1) apply(pairAction(value, start, end, event.key, lang) || closerOutdent(value, start, end, event.key));
  }
}

const api = {
  Editor, scan, highlight, bracketMatch, lint, indentFor, enterAction, pairAction, softBackspace, closerOutdent,
  toggleComment, shiftLines, tokenClosed, languages: Object.keys(LANGS),
};
if (typeof module === "object" && module.exports) module.exports = api;
else root.CodeEditor = api;
})(typeof window !== "undefined" ? window : globalThis);
