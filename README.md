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
> 可以选择，针对NYT的Daily，还是针对WSJ的WSN。
> - 针对 NYT的Daily，可以选择：给人名加上##
> - 针对WSJ的WSN，可以选择：段首的人名黑体

> 然后调用 `md_reader_collect.html`脚本进行 collect 生词生句的处理。

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

# podcast的时效问题

> podcast的结构
> **channels** -> **show** -> **episodes**
> show 在podcast的中文界面中叫做“节目”

我们会发现，针对我们选定的两个show，每个都包含很多episode。但是有些episode一开始能听，但是过一段时间之后，有些episode没办法收听了。

举例：

> 对于the Daily
- 工作日，周一到周五：几乎每天一期，都是美东时间早上6点之前。
- 周六Saturday，有时候没有，但是通常也有常规或者特别期。
- 周日Sunday，2026年1月开始增加特别版，侧重文化、健康、生活方式等非突发新闻的深度故事，而非日常头条。

有个概念叫：**订阅者单集**

比如：
the viewer of the war from a Florida Gas Station
当发布出来的时候，我是能够看到的。但是后来就成为了“订阅者单集”，你在podcast上找到这个episode，但是你也不能听了，因为说“仅限订阅者”。

> 对于 what's news - WSJ podcasts
发布的频率更高一些
- 工作日（周一至周五）：每天发布 两次（twice a day），帮助听众快速了解当日重要新闻（商业、金融、全球及政治动态）。
- 周六：发布 What's News **in Markets（市场回顾）**。
- 周日：发布 What's News **Sunday（深度探讨/周日特别版）**。


U.S. Rescues One of Two Crew Members From Jet Downed in Iran

What’s News in Markets: The War Trade, Megadeals and a Sneaker Slowdown

---

# 使用podcast

下载单集：存储到，已下载-show name文件夹下
移除下载

前往节目：回到show的主界面

添加到队列：

存储单集：
取消存储单集：

标记为已播放：
查看听写文本：

在 macOS 的播客软件里，下面这两个选项意思其实是有细微差别的：

1. 下载单集（Download Episode）
    * 功能：把这个 episode 的音频文件从网络拉到本地存储，方便离线播放。
    * 特点：文件通常保存在应用的缓存目录或者指定的下载目录，软件管理，可能会自动删除旧的下载（比如空间不足或自动清理策略）。
    * 场景：你想在没有网络时听这一集。
2. 存储单集（Keep Episode / Mark as Saved）
    * 功能：告诉软件“永久保留这一集”，不受自动清理影响。
    * 特点：即使软件有自动删除旧下载或只保留最近 N 集的策略，这一集会被保留。
    * 场景：你想长期保留一年前的某集，随时回顾，不怕被自动删掉。

总结一句话区别：

* 下载 = 可以离线听，但可能会被自动删除；
* 存储/保留 = 永久保留，不受自动清理影响。

💡技巧：如果你想随时回顾一年前的 episode，最好先下载，再标记存储，这样既能离线听，又不会被系统删掉。

![](./images/download%20and%20save.png)
好像不准头这个图片，傻逼chatgpt


---

播客中只能看到一部分的问题
主要源于 RSS feed 的默认设置（通常限制显示最近 20 期左右）。 WSJ《What's News》的完整历史存档仍然存在，但需通过特定方式访问。
为什么只能看到 20 多期？

大部分播客 App（如 Apple Podcasts、Spotify 等）从 RSS feed 拉取数据，而 WSJ 的 feed 默认仅返回最近约 20 集（?limit=20）。
旧集并未被删除，而是需要手动加载或切换平台才能看到更多内容。

如何访问更早的 episode？

在当前 App 中尝试加载更多
向下滚动 episode 列表，点击“Load More” 或 “更多剧集”（部分平台支持）。
使用 App 内搜索功能，输入具体日期（如“2025 年 5 月”）或关键词，通常可调出旧集。

推荐切换到以下平台（存档更完整）
Podbean：显示更多历史 episode，并有分页加载（“More Episodes”）。
Spotify 或 Amazon Music：部分用户反馈存档显示更全，可尝试搜索节目后向下浏览。
WSJ 官网（wsj.com/podcasts/whats-news）：列出近期集数，并提供“Find them wherever you listen to podcasts”的指引。官网还常附 transcript，便于查找。

其他有效方法
使用 Podcast Addict 或其他高级播客 App：这些 App 支持自定义 RSS 并加载完整存档。
直接搜索特定日期/事件：在任意平台搜索“WSJ What's News [日期]”或新闻关键词，常能直接找到对应 episode。
RSS 完整 feed：尝试在支持自定义 feed 的 App 中添加 WSJ 的 Megaphone RSS（https://feeds.megaphone.fm/WSJ4886593505），部分情况下可加载更多。