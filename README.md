# 本脚本介绍

这个脚本程序是为了日常学习英语而使用的。针对的是podcast的学习，因为podcast是针对最新的时事新闻进行编写的，具有与众不同的时效性和反应现实生活。

我们选取的目标podcast主要有两类：

- NYT的节目：**the Daily**
- WSJ的节目：**what's news**

## 基本的处理逻辑

1. 找到节目的文本
2. 不管三七二十一，直接下载下来存放成 `md文件`。
3. 针对节目，进行“第一步处理”
4. 然后进行“第二步处理”
5. 选定生词，生成投喂给chatgpt的`md文件`


---

# NYT Daily 的脚本处理
我们这个处理是针对 NYT 的 podcast，叫做 Daily 来进行处理的，这个podcast有它自己的特点：
- 每一期的节目，都会请不同的嘉宾来访谈
- 这些嘉宾的名字，会单独存在一行，然后后面跟的段落是这个人的录音。

具体举例为：

```text
rachel abrams
From “The New York Times,” I’m Rachel Abrams. And this is “The Daily.”

[THEME MUSIC]

For the first time in nearly a decade, President Trump will meet with China’s President Xi Jinping in Beijing. The meeting comes as Trump struggles to extract himself from the war with Iran and must now face off against China, the biggest threat to the US’s dominance on everything from technology to trade. Today, my colleague David Sanger explains what’s likely to come of this meeting and, more pressingly, what will not.

It’s Wednesday, May 13.

david sanger
Hey, guys, can you hear me?
```

整个过程的基本思路：
1. 先下载下来文本，存储在markdown文件中
2. 根据markdown文件的内容，我们记录下嘉宾的名字，以及其他的需要的文本。这些嘉宾的名字和需要的文本，会被python脚本自动处理成 `二级标题`。
3. 调用python脚本 **./scripts/Daily_ promote_standalone_lines.py**。生成新的 `md`文件。这个新的markdown文件，就已经按照给你给出的字符串，修改了内部的结构。这些字符串会按照`##` **大纲二级**显示。
4. 然后你输出的md文件，比如说是 Daily_bold.md
5. 现在我们就可以进一步的处理了！我们可以进行“标记”了。这里要使用的html程序是：**./md_reader_collet.html** 文件进行处理即可。
6. 你在其中进行阅读，然后标记生词，然后这些词会被收集，同时还可以输出md文件。这个文件可以引入到**chatGPT**中进行处理。

> 使用的脚本是：
**./scripts/Daily_promote_standalone_lines.py**:

简单来说就是：

||input files|scripts|notes|
|---|---|---|---|
|1|Daily网站上下载的Daily脚本md格式，`A.md`|Daily_promote_standalone_lines.py|给出人名，python脚本把人名都处理成##二级标题，生成新md文件，`A_bold`.md|
|2|上一步生成的md文件|md_reader_collect.html|在md_reader_collect中进行浏览，选定生词和用法，进行collect，生成`A_bold_collect.md`|


> python脚本`Daily_promote_standalone_lines.py`的调用方法：

对于你需要改动的markdown文件进行处理。处理的方式是：

```python
python3 路径/Daily_promote_standalone_lines.py 路径/podcast_daily.md \
 --term "rachel abrams" \
 --term "david sanger" \
 --term "[advertisements]" \
 --term "[THEME MUSIC]" \
 --output 路径/podcast_daily_bold_md
# 注意，这里要有个空格，在每行的开头！！
```

> 注意上面的处理方式：
- `\` 就是表示命令没有输入完
- 最后一行不加`\`符号
- 你嫌麻烦的话，也可以直接一直写下去，比如：

```python
python3 ./scripts/Daily_promote_standalone_lines.py test.md --term "rachel abrams"  --output test_bold_2.md
# 这样书写也是可以的
```

处理完毕了之后，新的markdown文件已经在嘉宾的人名和需要处理的文本处，变成了`二级标题`。

> **相对路径 vs 绝对路径**
那么提醒你一下，关于<u>相对路径</u>和<u>绝对路径</u>的问题：
上面书写的命令，实在是写起来太麻烦了，可以可以写相对路径。
- `.` 是当前目录
- `./a.txt` 是当前目录里的 `a.txt`
- `..` 是上一级目录
- `../a.txt` 是上一级目录里的 `a.txt`


---

# WJS what's news 脚本处理
你下载下来的transcript是这样字的：

```text
Alex Ossola: The Pentagon says the growing cost of the Iran war is going to leave them short of money for other operations. Plus, why Bitcoin evangelists are hyped for a different coin called Zcash.

Greg Zuckerman: Bitcoin is just an object of speculation. It's digital gold at this point, and the argument for Zcash is it's digital gold plus because you've got this ability to shield yourself from the government.
```

脚本的特点是:

1. what's 的文本和 Dialy的文本格式不一样，每个md文件中，也是嘉宾的对话。但是人名是在段首，而不是“单独成一行”。
2. 我们依然是引入外部的输入，给出transcript中的人名
3. 然后对于markdown文件中的人名处理是：`**Imam Moise**` 这样的处理方式，将人名变成黑体
3. 生成新的markdown文件，由用户指定。


> 使用的脚本是：
**./scripts/WSJ_bold_leading_speakers.py**:

具体的使用格式就是：
```python
python3 scripts/WSJ_bold_leading_speakers.py podcast_WSN.md \
  --speaker "Imani Mosise" \
  --speaker "David Sanger" \
  --output podcast_WSN_bold.md
```

简单来说就是：

||input files|scripts|notes|
|---|---|---|---|
|1|WSJ网站上下载的Daily脚本md格式，`B.md`|WSJ_bold_leading_speakers.py|给出人名，python脚本把人名都处理成**黑体**，生成新md文件，`B_bold`.md|
|2|上一步生成的md文件|md_reader_collect.html|在md_reader_collect中进行浏览，选定生词和用法，进行collect，生成`B_bold_collect.md`|


---

# 更加牛逼的、一步到位的做法

> 你也可以使用我们独家秘制的html程序

1. 使用程序 <font color=blue>AAA_Daily_WSJ_transcript_tool.html</font> 程序。
1.1 当你选择 **WSJ:段首 Name:加粗** ：你就可以输入人名，让在段首的这些人名变成粗体。
1.2 当你选择 **Daily:独立行提升为##标题** ：你就可以选择独立成行的人民，提升其为2级标题。

2. 获得的结构已经更清晰的markdown文件，可以引入到html程序 <font color=blue>md_reader_collect.html</font> 中进行处理，处理完毕就形成了可以投喂给 chatGPT的md文件了。

3. chatGPT的提示词，请参见：<font color=blue>提示词-ChatGPT.md</font>

---

# chatgpt提示词

现在就需要有提示词了，我们进入到 chatGPT 环节了，因为之前我们通过脚本和html文件已经完善了我们的markdown文件，所以现在可以进入到和 chatGPT 交互的环节了。
那么就要有提示词。

> 提示词Version01

我在通过podcast的方式学习英文，现在我要处理podcast的transcript，在读这些 transcript过程中，总会有不明白的单词和不明白的表达，所以需要你帮我批量处理。我已经整理好了，这些 transcript是以 markdownd文件的形式存在的。这些markdown文件的格式都是很简单的，顶多有标题和正文。在每个正文段落之后，所出现的以[COLLECTED]开始的那个段落，就是需要你帮我处理的。你需要做的是：

- 根据本 transcript 的上下文语境 context 进行处理
- 对于[COLLECTED]段落中出现的单词，先给出这个词的 merriam-webster音标，然后根据上下文的context，给出这个词在这里的中文意思，不要贪图全面，仅针对此处的这个词的用法说明。
    - 如果是动词的某个形式，给出动词原形，并且给出动词原形的 merriam-webster音标。
    - 如果是名词复数形式，给出名词的原形，并且给出名词原形的 merriam-webster音标。
- 对于[COLLECTED]段落中出现的表达（而非是单独的单词），直接根据上下文context告诉我在此处的意思。
- 所有你给我的解释都仅针对上下文，而不应该贪图全面。
- 你给出的解释，新起一段，以`[notes]` 作为开头。对`[COLLECTED]`中的单词和表达，分条进行解释。

---
